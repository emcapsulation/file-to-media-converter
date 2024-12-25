from midiutil.MidiFile import MIDIFile
import sys

f = open(sys.argv[1], "rb");

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
time = 0

byte = f.read(1)
while byte:
    duration = default_duration

    # Do stuff with byte
    note = int.from_bytes(byte, byteorder="big")

    if note >= 128:    
        duration = default_duration*2
        note = note%128

    mf.addNote(track, channel, note, time, duration, volume)
    time += duration;

    byte = f.read(1)    

f.close()

# Write it to disk
with open(sys.argv[1] + "-midi.mid", 'wb') as outf:
    mf.writeFile(outf)