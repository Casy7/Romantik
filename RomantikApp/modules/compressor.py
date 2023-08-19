from PIL import Image
import os


class ImageCompressor:
	def __init__(self, image_path):
		self.image_path = image_path
		self.optimize_max_compression_cycles = 2
		self.max_allowed_size = [3000, 3000]

	def compress(self):
		# print("DEF_SIZE", os.stat(self.image_path).st_size)
		self.downsize()
		self.optimize()
		# print("RES_SIZE", os.stat(self.image_path).st_size)
	

	def downsize(self):
		foo = Image.open(self.image_path)
		if foo.size[0] > self.max_allowed_size[0]:
			k_scale = foo.size[0]/self.max_allowed_size[0]
			foo = foo.resize((int(self.max_allowed_size[0]), int(
				foo.size[1]/k_scale)), Image.LANCZOS)
			foo.save(self.image_path, quality=95)
			
		if foo.size[1] > self.max_allowed_size[1]:
			k_scale = foo.size[1]/self.max_allowed_size[1]
			foo = foo.resize((int(foo.size[0]/k_scale), int(self.max_allowed_size[1]), ), Image.LANCZOS)
			foo.save(self.image_path, quality=95)

	def optimize(self):
		current_cycle = 0

		while os.stat(self.image_path).st_size > 1024*1024 and current_cycle < self.optimize_max_compression_cycles:
			foo = Image.open(self.image_path)
			foo.save(self.image_path, optimize=True, quality=50)            
			current_cycle += 1
