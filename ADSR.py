import numpy as np
sampling_rate = 48000

def getadsr(sound, envelope):
    """
    Linear ADSR envelope.
    Parameters
    ----------
    sound : audio data.
    a : "Attack" time, in seconds.
    d : "Decay" time, in seconds.
    s : "Sustain" amplitude level
    r : "Release" time, in seconds.

    Returns
    -------
    ADSR Envelope
    """
    a, d, s, r = envelope

    duration = len(sound)

    len_a = int(a * duration)
    len_d = int(d * duration)
    len_r = int(r * duration)
    len_s = int(duration) - len_a - len_d - len_r

    attack = np.linspace(0,1, num=len_a)
    decay = np.linspace(1,s, num=len_d)
    sustain = np.ones(len_s) * s
    release = np.linspace(s, 0, num=len_r)

    return list(np.hstack((attack, decay, sustain, release)))
