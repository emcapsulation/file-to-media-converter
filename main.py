from file_to_midi import file_to_midi
from file_to_image import file_to_image
from midi_to_file import midi_to_file
import os
import sys



def main():
	filename, file_extension = os.path.splitext(sys.argv[1])
	target_extension = ""

	if len(sys.argv) >= 3:
		target_extension = sys.argv[2]

	if target_extension == "":
		if file_extension == ".mid":
			# Convert from midi
			midi_to_file(filename, file_extension)

	elif target_extension == "mid":
		# Convert to midi
		file_to_midi(filename, file_extension)

	elif target_extension == "png":
		# Convert to png
		file_to_image(filename, file_extension)
		


if __name__ == "__main__":
	main()