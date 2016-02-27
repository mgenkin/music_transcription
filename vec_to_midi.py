import midi
import sys
import numpy as np

data = np.load(sys.argv[1])
bpm, e_ticks, vectors = data['arr_0'], data['arr_1'], data['arr_2']
bpm, e_ticks = int(bpm), int(e_ticks)

Tick_length = 100

# Instantiate a MIDI Pattern (contains a list of tracks)
pattern = midi.Pattern()
pattern.resolution = e_ticks*8
# Instantiate a MIDI Track (contains a list of MIDI events)
track = midi.Track()
# Append the track to the pattern
pattern.append(track)
track.append(midi.SetTempoEvent(tick=0, bpm=bpm))
pattern.make_ticks_abs()

current_notes = np.zeros((88))
current_tick = 0
for i in range(vectors.shape[0]):
	changing_vector = vectors[i]-current_notes
	off_notes = np.where(changing_vector<0)[0]+22
	on_notes = np.where(changing_vector>0)[0]+22
	for note in on_notes:
		track.append(midi.NoteOnEvent(tick=current_tick, velocity=100, pitch=note))
	for note in off_notes:
		track.append(midi.NoteOnEvent(tick=current_tick, velocity=0, pitch=note))
	current_notes = vectors[i]
	current_tick += e_ticks

pattern.make_ticks_rel()
track.append(midi.EndOfTrackEvent(tick=1))
midi.write_midifile("{}.mid".format(sys.argv[1][8:-4]), pattern)
print pattern
