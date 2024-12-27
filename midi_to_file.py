import sys
import os
from mido import MidiFile



class MidiTrack:
	TICK_LENGTH = 240
	NUM_NOTES = 128

	def __init__(self, track):
		self.track = track
		self.track_len = len(track)
		self.index = 0
		self.elapsed = 0


	def get_byte_from_note(self, note, duration):
		val = self.NUM_NOTES*(int(duration/self.TICK_LENGTH)-1) + note
		return val.to_bytes(1, "big")


	def get_msg(self, start_time):
		msg = self.track[self.index]
		self.elapsed += msg.time
		byte = None

		if msg.type == "note_on":
			start_time = self.elapsed

		elif msg.type == "note_off":
			byte = self.get_byte_from_note(msg.note, self.elapsed-start_time)

		self.index += 1

		return start_time, byte


	def read_n_notes(self, n):
		i = 0
		start_time = 0
		res = ""

		while i < n:
			msg = self.track[self.index]
			start_time, byte = self.get_msg(start_time)

			if byte != None:
				res += byte.decode('utf-8')
				i += 1

		return res


	def write_n_notes(self, f, n):
		i = 0
		start_time = 0

		while i < n and self.index < self.track_len:
			msg = self.track[self.index]
			start_time, byte = self.get_msg(start_time)

			if byte != None:
				f.write(byte)
				i += 1


def midi_to_file(filename, midi_extension):
	midi = MidiFile(filename+midi_extension)
	track = MidiTrack(midi.tracks[1])

	# Get the file extension
	ext_len = track.read_n_notes(1)
	file_extension = track.read_n_notes(int(ext_len))

	f = open(filename + file_extension, "wb")
	track.write_n_notes(f, track.track_len-track.index-1)
	f.close()