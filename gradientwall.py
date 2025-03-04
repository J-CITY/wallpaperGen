from random import randint
from PIL import Image, ImageDraw, ImageFont
import argparse
import math
import sys

class Config:
	def __init__(self):
		self.TYPE = "horizontal"
		self.NAME = 'wall.png'
		
		self.WIDTH = 1920
		self.HEIGHT = 1080
		
		#color
		self.COLORS = []

		self.GEN_COLOR = 0

class Wall:
	def __init__(self, config):
		self.config = config

	def GenColor(self):
		for i in range(self.config.GEN_COLOR):
			r = randint(0, 255)
			g = randint(0, 255)
			b = randint(0, 255)
			self.config.COLORS.append((r,g,b))

	def interpolate(self, f_co, t_co, interval):
		det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
		for i in range(interval):
			yield [round(f + det * i) for f, det in zip(f_co, det_co)]
			
	def GenWall(self):
		if self.config.GEN_COLOR > 0:
			self.GenColor()
		
		self.img = Image.new('RGB', (self.config.WIDTH, self.config.HEIGHT))
		draw = ImageDraw.Draw(self.img)
		if self.config.TYPE == "horizontal":
			step = int(math.ceil(self.config.WIDTH / (len(self.config.COLORS)-1)))
			for c in range(len(self.config.COLORS)-1):
				for i, color in enumerate(self.interpolate(self.config.COLORS[c], \
					self.config.COLORS[c+1], step)):
					draw.line([(i+step*c, 0), (i+step*c, self.config.HEIGHT)], tuple(color), width=1)
		elif self.config.TYPE == "vertical":
			step = int(math.ceil(self.config.HEIGHT / (len(self.config.COLORS)-1)))
			for c in range(len(self.config.COLORS)-1):
				for i, color in enumerate(self.interpolate(self.config.COLORS[c], \
					self.config.COLORS[c+1], step)):
					draw.line([(0, i+step*c), (self.config.WIDTH, i+step*c)], tuple(color), width=1)
		else:
			step = int(math.ceil(math.sqrt(self.config.HEIGHT*self.config.HEIGHT+self.config.WIDTH*self.config.WIDTH) /\
				(len(self.config.COLORS)-1)))*2
			for c in range(len(self.config.COLORS)-1):
				for i, color in enumerate(self.interpolate(self.config.COLORS[c], \
					self.config.COLORS[c+1], step)):
					draw.line([(i+step*c, 0), (0, i+step*c)], tuple(color), width=1)
		self.img.save(self.config.NAME)
		
config = Config()

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", type=str, default='wall.png', help="Name of output file")
	parser.add_argument("--width", type=int, default=1920, help="Image width")
	parser.add_argument("--height", type=int, default=1080, help="Image height")
					
	parser.add_argument("--colors", type=str, default="", help="Wallpaper color (Format: R1-G1-B1:R2-G2-B2)...")

	parser.add_argument("--genColors", type=int, default=0, help="Gen colors for gradient (set colors count)")
	
	parser.add_argument("--type", type=str, default="horizontal", help="Gradient type(horizontal, vertical, obliquely)")

	args = parser.parse_args()
	config.NAME = args.name
	
	config.TYPE = args.type
	
	config.WIDTH = args.width
	config.HEIGHT = args.height
	
	if args.colors != "":
		colors = []
		cs = args.colors.split(":")
		if len(cs) < 2:
			sys.exit()
		else:
			for _c in cs:
				c = _c.split("-")
				if len(c) == 3:
					r=g=b=0
					if (int(c[0]) < 256):
						r = int(c[0])
					if (int(c[1]) < 256):
						g = int(c[1])
					if (int(c[2]) < 256):
						b = int(c[2])
					colors.append((r,g,b))
		config.COLORS = colors
	config.GEN_COLOR = args.genColors
	if config.GEN_COLOR < 2:
		sys.exit()

parseArgs()
wall = Wall(config)
wall.GenWall()

