# 32tones
Simple tool for creating music with 32 tones per "octave"

Most music makes use of 12 distinct tones per doubling of frequency; this tool allows you to experiment with an alternate music system with more possible notes.

You can write music in `score.txt` in the same directory as the `32tones.py` script, or create a new text file. Running `python3 32tones.py` will generate a .wav file based on the instructions in `score.txt`. You can also run `python3 32tones.py [your_file.txt]` to generate music from another text file.

## The notation

The 32 tones are denoted by the digits (0-9) followed by the letters a-v. This is defined in the `NOTE_NAMES` dictionary in `32tones.py`. (You can, of course edit that to use your own names.)

You can use the `+` or `-` symbols after a note name to double or halve, respectively, the frequency of that note. You can use `.` after a note to indicate that it should be held for half as long. The `+`, `-`, and `.` symbols can be chained and combined arbitrarily.

To add a rest (no note), use the underscore (`_`) character.

To indicate that two tones should be played at the same time, put them inside parentheses. Only note names (not the length modifier `.`) should go inside parentheses.

Whitespace is ignored during parsing, so you can just use it to help with readability.


## Examples

Below are some simple examples of instructions and descriptions of what they do.

```
0123456789abcdefghijklmnopqrstuv
```
This will simply play each of the 32 tones in ascending order.

```
00+(00+)
```
This plays the base frequency (440 Hz by default), the same note doubled in frequency (one "octave" higher), then a chord with both of them together.

```
0.j.0+.j+.0++.j+.0+.j.0.
```
This plays a simple arpeggio (`j` is at about 1.5 times the frequency of `0`, corresponding to a fifth in traditional music) at double the default time rate.

Note that the base frequency, time rate, and other parameters can be modified inside `32tones.py`.
