from PIL import Image
import os

class ImageCompressor:
	def __init__(self):
		self.max_compression_cycles = 2
		self.max_resolution = [3000, 3000]
		self.max_file_size = 1024 ** 2 # 2 MiB

	def __check_file_size(self, path):
		return os.stat(path).st_size > self.max_file_size

	def process(self, image_path):
		if (self.__check_file_size(image_path)):
			self.downscale(image_path)
			self.compress(image_path)
	
	def downscale(self, image_path):
		img = Image.open(image_path)
		img.thumbnail(self.max_resolution)
		img.save(image_path)

	def compress(self, image_path):
		current_cycle = 0

		while self.__check_file_size(image_path) and current_cycle < self.max_compression_cycles:
			foo = Image.open(image_path)
			foo.save(image_path, optimize=True, quality=50)
			current_cycle += 1
