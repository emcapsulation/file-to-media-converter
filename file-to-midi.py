from midiutil.MidiFile import MIDIFile
import sys
import os


f = open(sys.argv[1], "rb");
filename, file_extension = os.path.splitext(sys.argv[1])

# Create MIDI object with one track
mf = MIDIFile(1)

# The first track
track = 0
time = 0
mf.addTrackName(track, time, sys.argv[1] + "-midi")
mf.addTempo(track, time, 1440)

channel = 0
volume = 100
default_duration = 0.125
duration = default_duration
time = 0


def getNote(note):
    duration = default_duration

    if note >= 128:    
        duration = default_duration*2
        note = note%128

    return note, duration


def writeIntToMidi(c, time):
    note, duration = getNote(c)
    mf.addNote(track, channel, note, time, duration, volume)
    time += duration

    return time



# Write the file extension length
ext_length = str(len(file_extension))
time = writeIntToMidi(ord(ext_length), time)

# Write the file extension
for c in file_extension:
    time = writeIntToMidi(ord(c), time)


byte = f.read(1)
while byte:
    duration = default_duration

    note = int.from_bytes(byte, byteorder="big")
    time = writeIntToMidi(note, time)

    byte = f.read(1)    

f.close()

# Write it to disk
with open(filename + ".mid", 'wb') as outf:
    mf.writeFile(outf)