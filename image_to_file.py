from PIL import Image

class ImageOpen:
	def __init__(self, filename):
		self.im = Image.open(filename)

		self.pixels = self.im.load()
		self.width, self.height = self.im.size

		self.pixels = list(self.im.getdata())
		self.num_pixels = len(self.pixels)
		self.position = 0
		self.pix_ind = 0


	def get_byte(self):
		if self.position >= self.num_pixels:
			return b'\x00'

		val = self.pixels[self.position][self.pix_ind]

		self.pix_ind += 1
		if self.pix_ind > 2:
			self.pix_ind = 0
			self.position += 1

		byte = val.to_bytes(1, "big")
		return byte


	def read_n_bytes(self, n):
		res = ""
		for i in range(0, n):
			byte = self.get_byte()
			res += byte.decode('utf-8')

		return res


	def write_bytes(self, f):
		byte = self.get_byte()

		while byte != b'\x00' and byte != None:
			f.write(byte)
			byte = self.get_byte()


def image_to_file(filename, file_extension):
	im = ImageOpen(filename+file_extension)

	# Get the file extension
	ext_len = im.read_n_bytes(1)
	file_extension = im.read_n_bytes(int(ext_len))

	f = open(filename + file_extension, "wb")
	im.write_bytes(f)
	f.close()