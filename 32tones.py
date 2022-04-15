import numpy as np
from scipy.io.wavfile import write

SAMPLE_RATE = 44100
AMPLITUDE = np.iinfo(np.int16).max
TIME_RATE = 0.5
DEFAULT_BASE_FREQ = 440.0
DEFAULT_FADE = TIME_RATE / 32

NOTE_NAMES = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'a': 10,
    'b': 11,
    'c': 12,
    'd': 13,
    'e': 14,
    'f': 15,
    'g': 16,
    'h': 17,
    'i': 18,
    'j': 19,
    'k': 20,
    'l': 21,
    'm': 22,
    'n': 23,
    'o': 24,
    'p': 25,
    'q': 26,
    'r': 27,
    's': 28,
    't': 29,
    'u': 30,
    'v': 31
}


def timespace(length: float):
    return np.linspace(0.0, TIME_RATE*length, int(TIME_RATE*SAMPLE_RATE*length))


def gen_sinewave(freq: float, length: float, amp: float=1.0, fade=DEFAULT_FADE):
    tone = amp * AMPLITUDE * np.sin(2.0 * np.pi * freq * timespace(length))
    if fade:
        fade_frames = int(TIME_RATE*SAMPLE_RATE*fade)
        fadespace = np.linspace(0, 1.0, fade_frames)
        tone[:fade_frames] *= fadespace
        tone[-fade_frames:] *= np.flip(fadespace)
    return tone.astype(np.int16)




def create_silence(length: float):
    return np.zeros(int(TIME_RATE*SAMPLE_RATE*length), dtype=np.int16)


def tone_from_text(tone_str: str, length: float, base_freq: float=DEFAULT_BASE_FREQ, amp: float=0.5):
    # assert(not tone_str.startswith('+'), 'tone_str must start with a note name, not +')
    tones = []
    for x in tone_str:
        if x == '+':
            tones[-1] += 32
        elif x == '-':
            tones[-1] -= 32
        elif x == '_':
            tones.append(None)
        else:
            tones.append(NOTE_NAMES[x])
    return np.sum([
        gen_sinewave(
            base_freq * 2**(tone / 32),
            length,
            amp / len(tones)
        )
        if tone is not None
        else create_silence(length)
        for tone in tones
    ], axis=0, dtype=np.int16)


def read_composition(comp_str: str):
    tones = []
    in_parentheses = False
    current_note = ''
    length = 1.0
    for x in comp_str:
        if not in_parentheses:
            if x not in '(.+-':
                if current_note:
                    tones.append(
                        tone_from_text(current_note, length)
                    )
                length = 1.0
                current_note = x
            elif x == '-':
                current_note += '-'
            elif x == '+':
                current_note += '+'
            elif x == '.':
                length /= 2
            elif x == '(':
                in_parentheses = True
                if current_note:
                    tones.append(
                        tone_from_text(current_note, length)
                    )
                length = 1.0
                current_note = ''
        elif x == ')':
            in_parentheses = False
        else:
            current_note += x
    if current_note:
        tones.append(
            tone_from_text(current_note, length)
        )
    return np.concatenate(tones)
        


if __name__ == '__main__':
    import sys
    import re
    if len(sys.argv) > 1:
        score_file = sys.argv[1]
    else:
        score_file = 'score.txt'
    if len(sys.argv) > 2:
        out_file = sys.argv[2]
    else:
        out_file = 'music.wav'
    with open(score_file, 'r') as fh:
        comp = re.sub(r'\s', '', fh.read())
    signal = read_composition(comp)
    write(out_file, SAMPLE_RATE, signal)
