"""Genera la música del video (60 s, 120 BPM) de forma determinística.

Estructura (1 compás = 2 s):
  0–4 s   intro: pad + arpegio filtrado + subida      → golpe a los 4 s
  4–16 s  entra la batería
  16–30 s tema completo con palmas                    (preguntas)
  30–32 s quiebre + subida                            → golpe a los 32 s
  32–44 s tema completo                               (cómo trabajamos)
  44–52 s tema completo + platillos abiertos          (beneficios)
  52–56 s quiebre: solo pad                           (pregunta final)
  56–60 s golpe final + cierre

Uso: python3 tools/generar_musica.py assets/audio/musica.wav
"""

import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 44100
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
DUR = 60.0
N = int(SR * DUR)
rng = np.random.default_rng(7)

GOLPES = [4, 8, 16, 32, 44, 52, 56]


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def lp(x, f):
    return sosfilt(butter(2, f, "low", fs=SR, output="sos"), x)


def hp(x, f):
    return sosfilt(butter(2, f, "high", fs=SR, output="sos"), x)


def bp(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def put(buf, sig, t, gain=1.0):
    i = int(t * SR)
    if i >= len(buf):
        return
    sig = sig[: len(buf) - i]
    buf[i : i + len(sig)] += gain * sig


def saw(f, n, detune=0.0):
    t = np.arange(n) / SR
    out = np.zeros(n)
    for d in (-detune, 0.0, detune):
        ph = (t * f * (1 + d)) % 1.0
        out += 2 * ph - 1
    return out / 3


def env_adsr(n, a=0.01, r=0.1):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na)
    if nr:
        e[-nr:] *= np.linspace(1, 0, nr)
    return e


# --- instrumentos ---
def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7) + 0.3 * np.exp(-t * 200) * rng.standard_normal(n) * 0.2


def clap():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    noise = bp(rng.standard_normal(n), 900, 3500)
    e = np.exp(-t * 18)
    for off in (0.008, 0.016):
        k = int(off * SR)
        e[:k] += 0.5 * np.exp(-np.arange(k) / SR * 400)
    return noise * e * 0.8


def hat(open_=False):
    n = int((0.35 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 7000) * np.exp(-t * (9 if open_ else 70)) * 0.5


def impacto():
    n = int(2.2 * SR)
    t = np.arange(n) / SR
    f = 30 + 70 * np.exp(-t * 8)
    boom = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 2.5)
    crash = hp(rng.standard_normal(n), 3000) * np.exp(-t * 2.2) * 0.35
    return boom * 0.9 + crash


def subida(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = n // 16
    for i in range(16):
        a, b = i * seg, (i + 1) * seg if i < 15 else n
        fc = 400 + (i / 15) ** 2 * 7000
        out[a:b] = bp(x[a:b], fc * 0.7, min(fc * 1.4, 18000))
    return out * (t / dur) ** 2 * 0.5


# Progresión I–V–vi–IV en Do mayor (un acorde por compás)
ACORDES = [
    [60, 64, 67],  # C
    [55, 59, 62, 67],  # G
    [57, 60, 64],  # Am
    [53, 57, 60, 65],  # F
]
BAJOS = [36, 31, 33, 29]


def acorde_en(t):
    return int(t // BAR) % 4


# --- pistas ---
drums = np.zeros(N)
bass = np.zeros(N)
pad = np.zeros(N)
arp = np.zeros(N)
fx = np.zeros(N)
side = np.ones(N)  # envolvente de "bombeo" en cada bombo

K, C, H, HO = kick(), clap(), hat(), hat(True)


def seccion(t):
    if t < 4:
        return "intro"
    if t < 16:
        return "a"
    if 30 <= t < 32:
        return "quiebre"
    if 52 <= t < 56:
        return "quiebre"
    if t >= 56:
        return "final"
    if 44 <= t < 52:
        return "c"
    return "b"


n_beats = int(DUR / BEAT)
for b in range(n_beats):
    t = b * BEAT
    s = seccion(t)
    if s in ("a", "b", "c", "final") and not (s == "final" and t >= 58):
        put(drums, K, t, 1.0)
        k = int(t * SR)
        m = int(0.25 * SR)
        side[k : k + m] = np.minimum(side[k : k + m], 0.35 + 0.65 * np.linspace(0, 1, m) ** 0.6)
    if s in ("b", "c") and b % 2 == 1:
        put(drums, C, t, 0.55)
    if s in ("a", "b", "c"):
        put(drums, HO if s == "c" else H, t + BEAT / 2, 0.35 if s == "c" else 0.4)
        if s != "a":
            put(drums, H, t + BEAT / 4, 0.15)
            put(drums, H, t + 3 * BEAT / 4, 0.15)

# bajo en corcheas
eighth = BEAT / 2
for i in range(int(DUR / eighth)):
    t = i * eighth
    s = seccion(t)
    if s in ("a", "b", "c", "final") and t < 58:
        n = int(eighth * SR)
        nota = BAJOS[acorde_en(t)] + (12 if i % 2 else 0)
        sig = lp(saw(midi(nota), n, 0.004), 600 if s != "a" else 380) * env_adsr(n, 0.004, 0.05)
        put(bass, sig, t, 0.55)

# pad por compás
for bar in range(int(DUR / BAR)):
    t = bar * BAR
    n = int(BAR * SR) + int(0.3 * SR)
    sig = np.zeros(n)
    for nota in ACORDES[bar % 4]:
        sig += saw(midi(nota), n, 0.006)
    fc = 1400 if seccion(t) in ("intro", "quiebre") else 2600
    sig = lp(sig, fc) * env_adsr(n, 0.25, 0.4)
    put(pad, sig, t, 0.16)

# arpegio en semicorcheas
sixteenth = BEAT / 4
for i in range(int(DUR / sixteenth)):
    t = i * sixteenth
    s = seccion(t)
    if s == "final" and t >= 58:
        continue
    notas = ACORDES[acorde_en(t)]
    nota = notas[[0, 1, 2, 1, 2, 0, 2, 1][i % 8] % len(notas)] + 12
    n = int(0.22 * SR)
    tt = np.arange(n) / SR
    f = midi(nota)
    sig = (np.sin(2 * np.pi * f * tt) + 0.35 * np.sin(4 * np.pi * f * tt) + 0.12 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 18)
    g = 0.1 if s in ("intro", "quiebre") else 0.16
    if s == "intro":
        g *= 0.4 + 0.6 * t / 4
    put(arp, sig, t, g * (1.0 if i % 4 == 0 else 0.75))

# efectos
for g in GOLPES:
    put(fx, impacto(), g, 0.9 if g in (4, 32, 56) else 0.55)
put(fx, subida(4.0), 0.0, 0.8)
put(fx, subida(2.0), 30.0, 0.9)
put(fx, subida(4.0), 52.0, 0.7)
put(fx, subida(1.0), 15.0, 0.5)
put(fx, subida(1.0), 43.0, 0.5)

# acorde final que queda sonando
n = int(4 * SR)
tt = np.arange(n) / SR
fin = np.zeros(n)
for nota in [48, 60, 64, 67, 72]:
    fin += saw(midi(nota), n, 0.006)
put(pad, lp(fin, 2200) * np.exp(-tt * 0.9), 56.0, 0.18)

mix = drums * 0.9 + bass * side + pad * side + arp * (0.6 + 0.4 * side) + fx
mix = hp(mix, 30)

# estéreo simple: arpegio y platillos levemente abiertos
delay = int(0.012 * SR)
left = mix + 0.15 * np.concatenate([np.zeros(delay), arp[:-delay]])
right = mix + 0.15 * arp

st = np.stack([left, right], axis=1)
st = np.tanh(st * 1.2) / np.tanh(1.2)  # saturación suave
fade = int(1.5 * SR)
st[-fade:] *= np.linspace(1, 0, fade)[:, None]
st /= np.abs(st).max() / 0.89

out = sys.argv[1] if len(sys.argv) > 1 else "musica.wav"
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((st * 32767).astype("<i2").tobytes())
print("ok", out)
