import numpy as np


sampling_rate = 48000


def adsr(sound, a, d, s, r):
    """
  Linear ADSR envelope.
  Parameters
  ----------
  sound : audio data.
  a :"Attack" time, in seconds.
  d : "Decay" time, in seconds.
  s : "Sustain" amplitude level
  r : "Release" time, in seconds.

  Returns
  -------
    ADSR Envelop

  """
    attack = a * sampling_rate
    decay = d * sampling_rate
    sustain = s
    release = r * sampling_rate
    duration = len(sound)

    m_a = 1. / attack
    m_d = (sustain - 1.) / decay
    m_r = - sustain * 1. / release
    len_a = int(attack + .5)
    len_d = int(decay + .5)
    len_r = int(release + .5)
    len_s = int(duration + .5) - len_a - len_d - len_r

    for sample in range(len_a):
        yield sample * m_a
    for sample in range(len_d):
        yield 1. + sample * m_d
    for sample in range(len_s):
        yield sustain
    for sample in range(len_r):
        yield sustain + sample * m_r


def getadsr(sound, a=.2, d=.1, s=.7, r=.3):
    env = []
    for value in adsr(sound, a, d, s, r):
        env.append(value)
    env = np.array(env)
    return env
