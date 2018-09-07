import webcolors
from random import randint
from PIL import Image, ImageDraw, ImageFont
import argparse

class Config:
	def __init__(self):
		self.IS_GRADIENT = False
		self.IS_GRADIENT_VERTICAL = False
		self.IS_GRADIENT_FILLING = True
		self.NAME = 'wall.png'
		
		self.WIDTH = 1920
		self.HEIGHT = 1080
		
		#color
		self.R1 = 0
		self.G1 = 0
		self.B1 = 0
		
		self.R2 = 0
		self.G2 = 0
		self.B2 = 0
		
		#border
		self.IS_BORDER = True
		self.B_WIDTH = 400
		self.B_HEIGHT = 400
		self.B_POS_X = 0.5 #0..1 like percent
		self.B_POS_Y = 0.5 #0..1 like percent
		self.B_COLOR = (255,255,255)
		self.B_DEPTH = 5
		
		#strings
		self.COLOR_NAME_1 = ''
		self.COLOR_RGB_NAME_1 = ''
		self.COLOR_HEX_NAME_1 = ''
		
		self.COLOR_NAME_2 = ''
		self.COLOR_RGB_NAME_2 = ''
		self.COLOR_HEX_NAME_2 = ''
		
		self.OFFSET_X_1 = 5
		self.OFFSET_Y_1 = 5
		
		self.OFFSET_X_2 = 5
		self.OFFSET_Y_2 = 5
		
		#font
		self.IS_TEXT = True
		self.FONT = 'C:/Users/333da/Desktop/genwall/fonts/slkscr.ttf'
		self.FONT_SIZE = 24
		self.FONT_COLOR_1 = (255,255,255)
		self.FONT_COLOR_2 = (255,255,255)
		
		self.GEN_COLOR = True

class Wall:
	def __init__(self, config):
		self.config = config
	
	def ClosestColour(self, requested_colour):
		min_colours = {}
		for key, name in webcolors.css3_hex_to_names.items():
			r_c, g_c, b_c = webcolors.hex_to_rgb(key)
			rd = (r_c - requested_colour[0]) ** 2
			gd = (g_c - requested_colour[1]) ** 2
			bd = (b_c - requested_colour[2]) ** 2
			min_colours[(rd + gd + bd)] = name
		return min_colours[min(min_colours.keys())]

	def GetColourName(self, requested_colour):
		try:
			closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
		except ValueError:
			closest_name = self.ClosestColour(requested_colour)
			actual_name = None
		if actual_name is None:
			return closest_name
		else:
			return actual_name
	
	def GenColor(self):
		self.config.R1 = randint(0, 255)
		self.config.G1 = randint(0, 255)
		self.config.B1 = randint(0, 255)
		c = (self.config.R1,self.config.G1,self.config.B1)
		name = self.GetColourName(c)
		self.config.COLOR_NAME_1 = name[0].upper()+name[1:]
		self.config.COLOR_HEX_NAME_1 = 'HEX ' + "{:02x}{:02x}{:02x}".format(self.config.R1,self.config.G1,self.config.B1)
		self.config.COLOR_RGB_NAME_1 = 'RGB '+str(self.config.R1)+' '+str(self.config.G1)+' '+str(self.config.B1)
		if self.config.IS_GRADIENT:
			self.config.R2 = randint(0, 255)
			self.config.G2 = randint(0, 255)
			self.config.B2 = randint(0, 255)
			c = (self.config.R2,self.config.G2,self.config.B2)
			name = self.GetColourName(c)
			self.config.COLOR_NAME_2 = name[0].upper()+name[1:]
			self.config.COLOR_HEX_NAME_2 = 'HEX ' + "{:02x}{:02x}{:02x}".format(self.config.R2,self.config.G2,self.config.B2)
			self.config.COLOR_RGB_NAME_2 = 'RGB '+str(self.config.R2)+' '+str(self.config.G2)+' '+str(self.config.B2)
	
	def singleBorder(self):
		#border
		#pixels = self.img.load()
		
		startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH/2 - self.config.B_DEPTH/2)
		starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT/2 - self.config.B_DEPTH/2)
		
		if self.config.IS_BORDER:
			draw = ImageDraw.Draw(self.img)
			
			draw.line([(startx, starty), 
					(startx + self.config.B_DEPTH/2+config.B_WIDTH, starty)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
			draw.line([(startx, starty - self.config.B_DEPTH/4), 
					(startx, starty + self.config.B_DEPTH/2+self.config.B_HEIGHT)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
			draw.line([(startx, starty+self.config.B_HEIGHT), 
					(startx + self.config.B_DEPTH/2+config.B_WIDTH, starty+self.config.B_HEIGHT)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
			draw.line([(startx+config.B_WIDTH, starty + self.config.B_DEPTH/4+self.config.B_HEIGHT), 
					(startx+config.B_WIDTH, starty)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
	
	def doubleBorder(self):
		#border
		
		if self.config.IS_BORDER:
			draw = ImageDraw.Draw(self.img)
			if self.config.IS_GRADIENT_VERTICAL:
				startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH/2 - self.config.B_DEPTH/2)
				starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT - self.config.B_DEPTH/2)
				
				if self.config.IS_GRADIENT_FILLING:
					_len = 0.8*(self.config.B_HEIGHT)
					for i in range(starty, starty+self.config.B_HEIGHT):
						if i-starty > _len:
							_x = startx+self.config.B_WIDTH*0.8+(i-starty-self.config.B_HEIGHT)/(self.config.B_HEIGHT*0.8-self.config.B_HEIGHT) * (self.config.B_WIDTH-self.config.B_WIDTH*0.8)
						else:
							_x = startx+config.B_WIDTH
						draw.line([(startx, i), 
							(_x, i)], (self.config.R1,self.config.G1,self.config.B1), width=1)
					_len = 0.2*(self.config.B_HEIGHT)
					for i in range(starty+self.config.B_HEIGHT, starty+self.config.B_HEIGHT*2):
						if i-starty-self.config.B_HEIGHT < _len:
							_x = startx+(i-starty-self.config.B_HEIGHT-self.config.B_HEIGHT*0.2)/\
								(self.config.B_HEIGHT-self.config.B_HEIGHT-self.config.B_HEIGHT*0.2) * (self.config.B_WIDTH*0.2)
						else:
							_x = startx
						draw.line([(_x, i), 
							(startx+self.config.B_WIDTH, i)], (self.config.R2,self.config.G2,self.config.B2), width=1)
					
					
				draw.line([(startx+config.B_WIDTH, starty - self.config.B_DEPTH/4), 
					(startx+config.B_WIDTH, starty+int(config.B_HEIGHT*0.8))], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
				
				draw.line([(startx+config.B_WIDTH, starty), 
					(startx - self.config.B_DEPTH/4, starty)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
				
				draw.line([(startx, starty), 
					(startx, starty+config.B_HEIGHT + self.config.B_DEPTH/2)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx, starty+config.B_HEIGHT), 
					(startx+config.B_WIDTH + self.config.B_DEPTH/2, starty+config.B_HEIGHT)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH, starty+config.B_HEIGHT), 
					(startx+config.B_WIDTH, starty+self.config.B_HEIGHT*2 + self.config.B_DEPTH/2)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH, starty+config.B_HEIGHT*2), 
					(startx - self.config.B_DEPTH/4, starty+config.B_HEIGHT*2)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx, starty+config.B_HEIGHT*2), 
					(startx, starty+config.B_HEIGHT*2 - int(config.B_HEIGHT*0.8))], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)

			else:
				startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH - self.config.B_DEPTH/2)
				starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT/2 - self.config.B_DEPTH/2)
				if self.config.IS_GRADIENT_FILLING:
					_len = 0.8*(self.config.B_HEIGHT)
					for i in range(starty, starty+self.config.B_HEIGHT):
						if i-starty > _len:
							_x = startx+self.config.B_WIDTH*0.8+(i-starty-self.config.B_HEIGHT)/(self.config.B_HEIGHT*0.8-self.config.B_HEIGHT) * (self.config.B_WIDTH-self.config.B_WIDTH*0.8)
						else:
							_x = startx+config.B_WIDTH
						draw.line([(startx, i), 
							(_x, i)], (self.config.R1,self.config.G1,self.config.B1), width=1)
					_len = 0.2*(self.config.B_HEIGHT)
					for i in range(starty, starty+self.config.B_HEIGHT):
						if i-starty < _len:
							_x = startx+config.B_WIDTH+(i-starty-self.config.B_HEIGHT*0.2)/\
								(0-self.config.B_HEIGHT*0.2) * (self.config.B_WIDTH*0.2)
						else:
							_x = startx+config.B_WIDTH
						draw.line([(_x, i), 
							(startx+self.config.B_WIDTH*2, i)], (self.config.R2,self.config.G2,self.config.B2), width=1)
					
					
				
				draw.line([(startx - self.config.B_DEPTH/4, starty+config.B_HEIGHT), 
					(startx+int(config.B_WIDTH*0.8), starty+config.B_HEIGHT)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
				
				draw.line([(startx, starty+config.B_HEIGHT), 
					(startx, starty - self.config.B_DEPTH/4)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
				
				draw.line([(startx, starty), 
					(startx+config.B_WIDTH + self.config.B_DEPTH/2, starty)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH, starty), 
					(startx+config.B_WIDTH, starty+config.B_HEIGHT + self.config.B_DEPTH/2)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH, starty+config.B_HEIGHT), 
					(startx+config.B_WIDTH*2 + self.config.B_DEPTH/2, starty+config.B_HEIGHT)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH*2, starty+config.B_HEIGHT), 
					(startx+config.B_WIDTH*2, starty - self.config.B_DEPTH/4)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
					
				draw.line([(startx+config.B_WIDTH*2, starty), 
					(startx+config.B_WIDTH+int(config.B_WIDTH*0.2), starty)], tuple(self.config.B_COLOR), width=self.config.B_DEPTH)
	
	def doubleFont(self):
		c = (self.config.R1,self.config.G1,self.config.B1)
		name = self.GetColourName(c)
		if self.config.COLOR_NAME_1 == "":
			self.config.COLOR_NAME_1 = name[0].upper()+name[1:]
		if self.config.COLOR_HEX_NAME_1 == "":
			self.config.COLOR_HEX_NAME_1 = 'HEX ' + "{:02x}{:02x}{:02x}".format(self.config.R1,self.config.G1,self.config.B1)
		if self.config.COLOR_RGB_NAME_1 == "":
			self.config.COLOR_RGB_NAME_1 = 'RGB '+str(self.config.R1)+' '+str(self.config.G1)+' '+str(self.config.B1)
		if self.config.IS_GRADIENT:
			c = (self.config.R2,self.config.G2,self.config.B2)
			name = self.GetColourName(c)
			if self.config.COLOR_NAME_2 == "":
				self.config.COLOR_NAME_2 = name[0].upper()+name[1:]
			if self.config.COLOR_HEX_NAME_2 == "":
				self.config.COLOR_HEX_NAME_2 = 'HEX ' + "{:02x}{:02x}{:02x}".format(self.config.R2,self.config.G2,self.config.B2)
			if self.config.COLOR_RGB_NAME_2 == "":
				self.config.COLOR_RGB_NAME_2 = 'RGB '+str(self.config.R2)+' '+str(self.config.G2)+' '+str(self.config.B2)
			
		#text
		if self.config.IS_TEXT:
			if self.config.IS_GRADIENT_VERTICAL:
				startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH/2 - self.config.B_DEPTH/2)
				starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT - self.config.B_DEPTH/2)
			else:
				startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH - self.config.B_DEPTH/2)
				starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT/2 - self.config.B_DEPTH/2)
			fnt = ImageFont.truetype(self.config.FONT, self.config.FONT_SIZE)
			d = ImageDraw.Draw(self.img)
			
			_x1 = startx+self.config.B_DEPTH+self.config.OFFSET_X_1
			_y1 = starty+self.config.B_DEPTH+self.config.OFFSET_Y_1
			if (not(_x1 >=0 and _x1 < self.config.WIDTH and _y1 >= 0 and _y1 < self.config.HEIGHT)):
				_x1 = 0
				_y1 = 0
			d.text((_x1, _y1), 
				self.config.COLOR_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
			
			_y1 += (self.config.FONT_SIZE+2)
			if (not(_x1 >=0 and _x1 < self.config.WIDTH and _y1 >= 0 and _y1 < self.config.HEIGHT)):
				_x1 = 0
				_y1 = self.config.FONT_SIZE+2
			d.text((_x1, _y1), 
				self.config.COLOR_HEX_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
			
			_y1 += (self.config.FONT_SIZE+2)
			if (not(_x1 >=0 and _x1 < self.config.WIDTH and _y1 >= 0 and _y1 < self.config.HEIGHT)):
				_x1 = 0
				_y1 = (self.config.FONT_SIZE+2)*2
			d.text((_x1, _y1), 
				self.config.COLOR_RGB_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
			
			###
			if self.config.IS_GRADIENT_VERTICAL:
				_x2 = startx+self.config.B_DEPTH+self.config.OFFSET_X_2
				_y2 = starty+self.config.B_DEPTH*2+self.config.OFFSET_Y_2 + self.config.B_HEIGHT
			else:
				_x2 = startx+self.config.B_DEPTH*2+self.config.OFFSET_X_2 + self.config.B_WIDTH
				_y2 = starty+self.config.B_DEPTH+self.config.OFFSET_Y_2
			if (not(_x2 >=0 and _x2 < self.config.WIDTH and _y2 >= 0 and _y2 < self.config.HEIGHT)):
				_x2 = 0
				_y2 = 0
			d.text((_x2, _y2), 
				self.config.COLOR_NAME_2, font=fnt, fill=self.config.FONT_COLOR_1)
			
			_y2 += (self.config.FONT_SIZE+2)
			if (not(_x2 >=0 and _x2 < self.config.WIDTH and _y2 >= 0 and _y2 < self.config.HEIGHT)):
				_x2 = 0
				_y2 = self.config.FONT_SIZE+2
			d.text((_x2, _y2), 
				self.config.COLOR_HEX_NAME_2, font=fnt, fill=self.config.FONT_COLOR_1)
			
			_y2 += (self.config.FONT_SIZE+2)
			if (not(_x2 >=0 and _x2 < self.config.WIDTH and _y2 >= 0 and _y2 < self.config.HEIGHT)):
				_x2 = 0
				_y2 = (self.config.FONT_SIZE+2)*2
			d.text((_x2, _y2), 
				self.config.COLOR_RGB_NAME_2, font=fnt, fill=self.config.FONT_COLOR_1)
	
	def singleFont(self):
		c = (self.config.R1,self.config.G1,self.config.B1)
		name = self.GetColourName(c)
		if self.config.COLOR_NAME_1 == "":
			self.config.COLOR_NAME_1 = name[0].upper()+name[1:]
		if self.config.COLOR_HEX_NAME_1 == "":
			self.config.COLOR_HEX_NAME_1 = 'HEX ' + "{:02x}{:02x}{:02x}".format(self.config.R1,self.config.G1,self.config.B1)
		if self.config.COLOR_RGB_NAME_1 == "":
			self.config.COLOR_RGB_NAME_1 = 'RGB '+str(self.config.R1)+' '+str(self.config.G1)+' '+str(self.config.B1)
		#text
		if self.config.IS_TEXT:
			startx = int(self.config.WIDTH*self.config.B_POS_X - self.config.B_WIDTH/2 - self.config.B_DEPTH/2)
			starty = int(self.config.HEIGHT*self.config.B_POS_Y - self.config.B_HEIGHT/2 - self.config.B_DEPTH/2)
			fnt = ImageFont.truetype(self.config.FONT, self.config.FONT_SIZE)
			d = ImageDraw.Draw(self.img)
			_x = startx+self.config.B_DEPTH+self.config.OFFSET_X_1
			_y = starty+self.config.B_DEPTH+self.config.OFFSET_Y_1
			if (not(_x >=0 and _x < self.config.WIDTH and _y >= 0 and _y < self.config.HEIGHT)):
				_x = 0
				_y = 0
			d.text((_x, _y), 
				self.config.COLOR_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
			_x = startx+self.config.B_DEPTH+self.config.OFFSET_X_1
			_y = starty+self.config.B_DEPTH+self.config.OFFSET_Y_1+(self.config.FONT_SIZE+2)
			if (not(_x >=0 and _x < self.config.WIDTH and _y >= 0 and _y < self.config.HEIGHT)):
				_x = 0
				_y = self.config.FONT_SIZE+2
			d.text((_x, _y), 
				self.config.COLOR_HEX_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
			_x = startx+self.config.B_DEPTH+self.config.OFFSET_X_1
			_y = starty+self.config.B_DEPTH+self.config.OFFSET_Y_1+2*(self.config.FONT_SIZE+2)
			if (not(_x >=0 and _x < self.config.WIDTH and _y >= 0 and _y < self.config.HEIGHT)):
				_x = 0
				_y = (self.config.FONT_SIZE+2)*2
			d.text((_x, _y), 
				self.config.COLOR_RGB_NAME_1, font=fnt, fill=self.config.FONT_COLOR_1)
	
	
	import struct

	def hex2rgb(self, rgb):
		return struct.unpack('BBB', rgb.decode('hex'))

	def rgb2hex(self, rgb):
		return struct.pack('BBB',*rgb).encode('hex')
	def interpolate(self, f_co, t_co, interval):
		det_co =[(t - f) / interval for f , t in zip(f_co, t_co)]
		for i in range(interval):
			yield [round(f + det * i) for f, det in zip(f_co, det_co)]
			
	def GenWall(self):
		if self.config.GEN_COLOR:
			self.GenColor()
		
		if self.config.IS_GRADIENT:
			self.img = Image.new('RGB', (self.config.WIDTH, self.config.HEIGHT))
			if self.config.IS_GRADIENT_VERTICAL:
				draw = ImageDraw.Draw(self.img)
				for i, color in enumerate(self.interpolate((self.config.R1,self.config.G1,self.config.B1), \
					(self.config.R2,self.config.G2,self.config.B2), int(self.img.height))):
					draw.line([(0, i), (self.img.width, i)], tuple(color), width=1)
			else:
				draw = ImageDraw.Draw(self.img)
				for i, color in enumerate(self.interpolate((self.config.R1,self.config.G1,self.config.B1), \
					(self.config.R2,self.config.G2,self.config.B2), int(self.img.width))):
					draw.line([(i, 0), (i, self.img.height)], tuple(color), width=1)
					#(i, 0), (0, i)
				
		else:
			self.img = Image.new('RGB', (self.config.WIDTH, self.config.HEIGHT), 
				color = (self.config.R1, self.config.G1, self.config.B1))
		if self.config.IS_GRADIENT:
			self.doubleBorder()
			self.doubleFont()
		else:
			#border
			self.singleBorder()
			#text
			self.singleFont()
		
		#seve
		self.img.save(self.config.NAME)
		
config = Config()

def parseArgs():
	#colorwall.py --isGradient --colors 255-195-33:10-81-132 --borderWidth 300 --borderHeight 300 --offsetsTextX 5:90 --offsetsTextY 5:207
	#colorwall.py --isGradient --colors 255-195-33:10-81-132 --borderWidth 300 --borderHeight 300 --offsetsTextX 5:90 --offsetsTextY 5:207 --isGradientVertical
	
	parser = argparse.ArgumentParser()
	parser.add_argument("--name", type=str, default='wall.png', help="Name of output file")
	parser.add_argument("--width", type=int, default=1920, help="Image width")
	parser.add_argument("--height", type=int, default=1080, help="Image height")
					
	parser.add_argument("--color", type=str, default="0-0-0", help="Wallpaper color (Format: R-G-B)")
	parser.add_argument("--colors", type=str, default="0-0-0:255-255-255", help="Wallpaper color (Format: R1-G1-B1:R2-G2-B2)")
					
	parser.add_argument("--setBorder", action="store_true", help="Set border", default=True)
	parser.add_argument("--borderWidth", type=int, default=400, help="Border width")
	parser.add_argument("--borderHeight", type=int, default=400, help="Border height")
	parser.add_argument("--borderPosX", type=float, default=0.5, help="Border position X from 0 to 1 (like percent)")
	parser.add_argument("--borderPosY", type=float, default=0.5, help="Border position Y from 0 to 1 (like percent)")
	parser.add_argument("--borderColor", type=str, default="255-255-255", help="Border color (Format: R-G-B)")
	parser.add_argument("--borderDepth", type=int, default=5, help="Border depth")
	
	parser.add_argument("--colorName", type=str, default="", help="Set color name")
	parser.add_argument("--colorRGBName", type=str, default="", help="Set color RGB name")
	parser.add_argument("--colorHEXName", type=str, default="", help="Set color HEX name")
	
	parser.add_argument("--colorsName", type=str, default="", help="Set color name (color1:color2)")
	parser.add_argument("--colorsRGBName", type=str, default="", help="Set color RGB name (color1:color2)")
	parser.add_argument("--colorsHEXName", type=str, default="", help="Set color HEX name (color1:color2)")
	
	parser.add_argument("--offsetTextX", type=int, default=5, help="Set offset from border")
	parser.add_argument("--offsetTextY", type=int, default=5, help="Set offset from border")
	
	parser.add_argument("--offsetsTextX", type=str, default="5:5", help="Set offsets from border (color1:color2)")
	parser.add_argument("--offsetsTextY", type=str, default="5:5", help="Set offsets from border (color1:color2)")
	
	parser.add_argument("--setText", action="store_true", help="Set text", default=True)
	parser.add_argument("--font", type=str, default='C:/Users/333da/Desktop/genwall/fonts/slkscr.ttf', help="Path to ttf font")
	parser.add_argument("--fontSize", type=int, default=24, help="Font size")
	
	parser.add_argument("--fontColor", type=str, default="255-255-255", help="Font color (Format: R-G-B)")
	parser.add_argument("--fontColors", type=str, default="255-255-255:255-255-255", help="Font color (Format: R1-G1-B1:R2:B2:G2)")
	
	
	parser.add_argument("--genColor", action="store_true", help="Gen color", default=False)
	parser.add_argument("--genColors", action="store_true", help="Gen color", default=False)
	
	parser.add_argument("--isGradient", action="store_true", help="Gradient", default=False)
	parser.add_argument("--isGradientVertical", action="store_true", help="Vertical or horizontal", default=False)
	parser.add_argument("--isGradientFilling", action="store_true", help="Vertical or horizontal", default=True)

	args = parser.parse_args()
	config.NAME = args.name
	
	config.IS_GRADIENT = args.isGradient
	config.IS_GRADIENT_VERTICAL = args.isGradientVertical
	config.IS_GRADIENT_FILLING = args.isGradientFilling
	
	config.WIDTH = args.width
	config.HEIGHT = args.height
	if config.IS_GRADIENT:
		cs = args.colors.split(":")
		if len(cs) != 2:
			sys.exit()
		else:
			c = cs[0].split("-")
			if len(c) == 3:
				if (int(c[0]) < 256):
					config.R1 = int(c[0])
				if (int(c[1]) < 256):
					config.G1 = int(c[1])
				if (int(c[2]) < 256):
					config.B1 = int(c[2])
			c = cs[1].split("-")
			if len(c) == 3:
				if (int(c[0]) < 256):
					config.R2 = int(c[0])
				if (int(c[1]) < 256):
					config.G2 = int(c[1])
				if (int(c[2]) < 256):
					config.B2 = int(c[2])
	else:
		c = args.color.split("-")
		if len(c) == 3:
			if (int(c[0]) < 256):
				config.R1 = int(c[0])
			if (int(c[1]) < 256):
				config.G1 = int(c[1])
			if (int(c[2]) < 256):
				config.B1 = int(c[2])

	config.IS_BORDER = args.setBorder
	config.B_WIDTH = args.borderWidth
	config.B_HEIGHT = args.borderHeight
	if args.borderPosX >=0 and args.borderPosX <= 1:
		config.B_POS_X = args.borderPosX
	if args.borderPosY >=0 and args.borderPosY <= 1:
		config.B_POS_Y = args.borderPosY
		
	c = args.borderColor.split("-")
	if len(c) == 3:
		if int(c[0]) < 256 and int(c[1]) < 256 and int(c[2]) < 256:
			config.B_COLOR = (int(c[0]),int(c[1]),int(c[2]))
	config.B_DEPTH = args.borderDepth
	
	if config.IS_GRADIENT and args.colorsName!="":
		ns = args.colorsName.split(":")
		rgbs = args.colorsRGBName.split(":")
		hexs = args.colorsHEXName.split(":")
		config.COLOR_NAME_1 = ns[0]
		config.COLOR_RGB_NAME_1 = rgbs[0]
		config.COLOR_HEX_NAME_1 = hexs[0]
		config.COLOR_NAME_2 = ns[1]
		config.COLOR_RGB_NAME_2 = rgbs[1]
		config.COLOR_HEX_NAME_2 = hexs[1]
	if config.IS_GRADIENT and args.offsetsTextX!="":
		offXs = args.offsetsTextX.split(":")
		config.OFFSET_X_1 = int(offXs[0])
		config.OFFSET_X_2 = int(offXs[1])
	if config.IS_GRADIENT and args.offsetsTextY!="":
		offYs = args.offsetsTextY.split(":")
		config.OFFSET_Y_1 = int(offYs[0])
		config.OFFSET_Y_2 = int(offYs[1])
	if config.IS_GRADIENT and args.fontColors!="":
		cs = args.fontColors.split(":")
		c = cs[0].split("-")
		if len(c) == 3:
			if int(c[0]) < 256 and int(c[1]) < 256 and int(c[2]) < 256:
				config.FONT_COLOR_1 = (int(c[0]),int(c[1]),int(c[2]))
		c = cs[1].split("-")
		if len(c) == 3:
			if int(c[0]) < 256 and int(c[1]) < 256 and int(c[2]) < 256:
				config.FONT_COLOR_2 = (int(c[0]),int(c[1]),int(c[2]))
	else:
		config.COLOR_NAME_1 = args.colorName
		config.COLOR_RGB_NAME_1 = args.colorRGBName
		config.COLOR_HEX_NAME_1 =  args.colorHEXName
	
		config.OFFSET_X_1 = args.offsetTextX
		config.OFFSET_Y_1 =  args.offsetTextY
		c = args.fontColor.split("-")
		if len(c) == 3:
			if int(c[0]) < 256 and int(c[1]) < 256 and int(c[2]) < 256:
				config.FONT_COLOR_1 = (int(c[0]),int(c[1]),int(c[2]))
	config.IS_TEXT = args.setText
	config.FONT = args.font
	config.FONT_SIZE = args.fontSize
	
	
	
	config.GEN_COLOR = args.genColor


parseArgs()
wall = Wall(config)
wall.GenWall()

