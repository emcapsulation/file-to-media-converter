from PIL import Image



class ImageFile:
	def __init__(self, filename, dimensions):
		self.filename = filename
		self.dimensions = dimensions

		self.im = Image.new("RGB", (dimensions[0], dimensions[1]))

		self.position = [0, 0]
		self.pixel = [0, 0, 0]
		self.pixInd = 0


	def incrementPosition(self):
		self.position[0] += 1
		if self.position[0] >= self.dimensions[0]:
			self.position[0] = 0
			self.position[1] += 1

		if self.position[1] >= self.dimensions[1]:
			# Save the image, we ran out of space
			self.completeImage()


	def drawCompletedPixel(self):
		if self.pixInd > 2:
			self.im.putpixel(tuple(self.position), tuple(self.pixel))

			self.pixInd = 0
			self.pixel = [0, 0, 0]
			self.incrementPosition()


	def writeiByteToImage(self, i):
		self.pixel[self.pixInd] = i
		self.pixInd += 1
		self.drawCompletedPixel()


	def writebByteToImage(self, b):
		i = int.from_bytes(b, byteorder="big")
		self.writeiByteToImage(i)


	def writeWordToImage(self, word):
		for c in word:
			self.writeiByteToImage(ord(c))
		

	def completeImage(self):
		self.im.putpixel(tuple(self.position), tuple(self.pixel))
		self.im.save(self.filename + ".png")



def writeFileExtension(file_extension, im):
	# Write the file extension length
    ext_length = str(len(file_extension))
    im.writeiByteToImage(ord(ext_length))

    # Write the file extension
    im.writeWordToImage(file_extension)



def file_to_image(filename, file_extension):
	dimensions = [1280, 720]
	im = ImageFile(filename, dimensions)

	writeFileExtension(file_extension, im)

	# Write the file as a MIDI
	f = open(filename+file_extension, "rb")
	byte = f.read(1)
	while byte:
		im.writebByteToImage(byte)
		byte = f.read(1)

	f.close()

	# Write it to disk
	im.completeImage()
