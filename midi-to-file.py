import sys
import os
from mido import MidiFile


TICK_LENGTH = 120
NUM_NOTES = 128


filename, midi_ext = os.path.splitext(sys.argv[1])


def getByteFromNote(note, duration):
	val = NUM_NOTES*(int(duration/TICK_LENGTH)-1) + note
	return val.to_bytes(1, "big")


midi = MidiFile(sys.argv[1])

track = midi.tracks[1]
elapsed, start_time, end_time = 0, 0, 0


# Get the file extension
file_extension = ""
if track[2].type == "note_off":
	elapsed += track[2].time
	b_ext_len = getByteFromNote(track[2].note, track[2].time)
	ext_len = int.from_bytes(b_ext_len, byteorder="big")-48

	for i in range(0, ext_len*2):
		msg = track[2+i+1]
		elapsed += msg.time

		if msg.type == "note_on":
			start_time = elapsed

		elif msg.type == "note_off":
			end_time = elapsed
			byte = getByteFromNote(msg.note, end_time-start_time)
			file_extension += byte.decode('utf-8')

f = open(filename + file_extension, "wb")


for i in range(ext_len*2 + 3, len(track)):
	msg = track[i]
	elapsed += msg.time

	if msg.type == "note_on":
		start_time = elapsed

	elif msg.type == "note_off":
		end_time = elapsed
		byte = getByteFromNote(msg.note, end_time-start_time)
		f.write(byte)

f.close()