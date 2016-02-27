import sys
import midi
import numpy as np

midifile = sys.argv[1]
pattern = midi.read_midifile(midifile)
pattern.make_ticks_abs()
resolution = pattern.resolution

for event in pattern[0]:
	if event.name == 'Set Tempo':
		bpm = event.bpm
		break
if bpm == None:
	print "no bpm"

e_ticks = resolution/8.0
vector_list = []
current_vector = np.zeros((88))
pattern_index = [0]*len(pattern)
current_tick = e_ticks
event = [pattern[t][0] for t in range(len(pattern))]
exit_loop=False
tracks = range(len(pattern))
while True:
	for track in tracks:
		try:
			while event[track].tick < current_tick:
				if event[track].name == "Note On":
					if event[track].velocity == 0:
						current_vector[event[track].pitch-22] = 0
					else:
						current_vector[event[track].pitch-22] = 1
				pattern_index[track] += 1
				event[track] = pattern[track][pattern_index[track]]
		except IndexError:
			tracks.remove(track)
			if tracks == []:
				exit_loop = True
				break
	vector_list.append(current_vector.copy())
	current_tick += e_ticks
	if exit_loop:
		break

print "{} has bpm {} with {} ticks to an eighth and {} notes".format(midifile[5:-4], bpm, e_ticks, len(vector_list))
np.savez('vectors/{}.npz'.format(midifile[5:-4]), bpm, e_ticks, np.array(vector_list))
