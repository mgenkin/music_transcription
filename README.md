# music_transcription

you will need numpy, scipy, librosa, scikit-learn to mess around with this.

vec_to_midi.py takes a midi file to vector representation

midi_to_vec.py reconstructs midi file from vector representation (discards anything smaller than eighth note)

First Attempts ipynb tries a logistic regression example on vs1-4prs, a bach piece whose vector, audio, and midi representation is in the folder.

I used Fluidsynth with a basic free soundfont I found to synthesize the midi files.
