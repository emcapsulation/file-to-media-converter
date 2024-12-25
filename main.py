from file_to_midi import file_to_midi
import os
import sys

def main():
	filename, file_extension = os.path.splitext(sys.argv[1])

	if file_extension == "midi":
		# Convert from midi
		#midi_to_file(filename)
		pass

	else:
		# Convert to midi
		file_to_midi(filename, file_extension)


if __name__ == "__main__":
	main()