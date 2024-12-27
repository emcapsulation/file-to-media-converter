from midiutil.MidiFile import MIDIFile
import sys
import os



class MidiFile:
    def __init__(self, filename, track, channel, volume, tempo, default_duration):
        self.filename = filename
        self.track = track
        self.channel = channel
        self.volume = volume
        self.tempo = tempo
        self.default_duration = default_duration

        # Create MIDI object with one track
        self.mf = MIDIFile(1)

        # The first track
        self.time = 0
        self.mf.addTrackName(self.track, self.time, self.filename)
        self.mf.addTempo(self.track, self.time, self.tempo)


    def i_byte_to_note(self, i):
        duration = self.default_duration

        if i >= 128:    
            duration = self.default_duration*2
            i = i%128

        return i, duration


    def write_i_byte_to_midi(self, i):
        note, duration = self.i_byte_to_note(i)
        self.mf.addNote(self.track, self.channel, note, self.time, duration, self.volume)
        self.time += duration


    def write_b_byte_to_midi(self, b):
        note, duration = self.i_byte_to_note(int.from_bytes(b, byteorder="big"))
        self.mf.addNote(self.track, self.channel, note, self.time, duration, self.volume)
        self.time += duration


    def write_word_to_midi(self, word):
        for c in word:
            self.write_i_byte_to_midi(ord(c))


    def write_file(self, outf):
        self.mf.writeFile(outf)




def write_file_extension(file_extension, mf):
    # Write the file extension length
    ext_length = str(len(file_extension))
    mf.write_i_byte_to_midi(ord(ext_length))

    # Write the file extension
    mf.write_word_to_midi(file_extension)



def file_to_midi(filename, file_extension):
    # Default settings
    track = 0
    channel = 0
    volume = 100
    tempo = 60
    default_duration = 0.25

    # Create MIDI and encode file extension
    mf = MidiFile(filename, track, channel, volume, tempo, default_duration)
    write_file_extension(file_extension, mf)

    # Write the file as a MIDI
    f = open(filename+file_extension, "rb")
    byte = f.read(1)
    while byte:
        mf.write_b_byte_to_midi(byte)
        byte = f.read(1)

    f.close()

    # Write it to disk
    with open(filename + ".mid", 'wb') as outf:
        mf.write_file(outf)
