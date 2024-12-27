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


	def getByteFromNote(self, note, duration):
		val = self.NUM_NOTES*(int(duration/self.TICK_LENGTH)-1) + note
		return val.to_bytes(1, "big")


	def getMsg(self, start_time):
		msg = self.track[self.index]
		self.elapsed += msg.time
		byte = None

		if msg.type == "note_on":
			start_time = self.elapsed

		elif msg.type == "note_off":
			byte = self.getByteFromNote(msg.note, self.elapsed-start_time)

		self.index += 1

		return start_time, byte


	def readnNotes(self, n):
		i = 0
		start_time = 0
		res = ""

		while i < n:
			msg = self.track[self.index]
			start_time, byte = self.getMsg(start_time)

			if byte != None:
				res += byte.decode('utf-8')
				i += 1

		return res


	def writenNotes(self, f, n):
		i = 0
		start_time = 0

		while i < n and self.index < self.track_len:
			msg = self.track[self.index]
			start_time, byte = self.getMsg(start_time)

			if byte != None:
				f.write(byte)
				i += 1


def midi_to_file(filename, midi_extension):
	midi = MidiFile(filename+midi_extension)
	track = MidiTrack(midi.tracks[1])

	# Get the file extension
	ext_len = track.readnNotes(1)
	file_extension = track.readnNotes(int(ext_len))

	f = open(filename + file_extension, "wb")
	track.writenNotes(f, track.track_len-track.index-1)
	f.close()