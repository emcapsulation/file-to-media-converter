import sys
from mido import MidiFile


TICK_LENGTH = 120
NUM_NOTES = 128


def getByte(note, duration):
	val = NUM_NOTES*(int(duration/TICK_LENGTH)-1) + note
	return val.to_bytes(1, "big");


midi = MidiFile(sys.argv[1])
f = open("midi-to-file.txt", "wb")

for track in midi.tracks:
	elapsed, start_time, end_time = 0, 0, 0

	for msg in track:
		elapsed += msg.time

		if msg.type == "note_on":
			start_time = elapsed

		elif msg.type == "note_off":
			end_time = elapsed
			byte = getByte(msg.note, end_time-start_time)
			f.write(byte)

f.close()