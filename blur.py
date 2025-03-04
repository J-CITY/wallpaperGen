from random import randint
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import argparse
import math

class Wall:
	def __init__(self):
		self.inPath = "w.Jpeg"
		self.outPath = "wres.Jpeg"

		self.inv = False
		self.invText = False
		self.isGray = False
		
		self.R = 100
		self.A = 0
		self.B = 0
		self.isCircle = False
		
		self.isPolygon = False
		self.X = []
		self.Y = []
		
		self.isText = False
		self.text = ''
		self.textFont = 'C:/Users/333da/Desktop/genwall/fonts/slkscr.ttf'
		self.textX = 0
		self.textY = 0
		
		self.isBPoly = False
		self.polyX = []
		self.polyY = []
		self.polyColor = (0,0,0)
		self.polyColor = 1
		
		
		self.isRing = False
		self.ringR1 = 0
		self.ringR2 = 0
		self.ringX = 0
		self.ringY = 0
		self.ringColor = (0,0,0)
		
	def GenWall(self):
		img = Image.open(self.inPath).convert("RGBA")
		self.width, self.height = img.size
		
		self.x0 = self.width/2
		self.y0 = self.height/2
		self.L = len(self.X)
		for i in range(0, len(self.X)):
			self.X[i] += int(self.x0)
			self.Y[i] += int(self.y0)
		
		#imgres = img.filter(ImageFilter.BLUR)
		#imgres = img.filter(ImageFilter.BoxBlur(10))
		self.imgres = img.filter(ImageFilter.GaussianBlur(10)).convert("RGBA")
		self.bufImg = img.filter(ImageFilter.GaussianBlur(10)).convert("RGBA")
		self.pixels = img.load()
		self.pixelsres = self.imgres.load()
		
		if self.isCircle:
			if self.inv:
				self.CircleInv()
			else:
				self.Circle()
		if self.isPolygon:
			if self.inv:
				self.PolygonInv()
			else:
				self.Polygon()
		
		if self.isText:
			self.drawText()
		
		
			
		if self.isGray:
			self.drawGray()
		if self.isRing:
			self.drawRing()
		if self.isBPoly:
			self.drawBPoly()
		self.imgres.save(self.outPath)
		
	def CircleInv(self):
		for x in range(0,self.width):
			for y in range(0,self.height):
				if not((x-self.x0+self.A)**2+(y-self.y0+self.B)**2 < self.R*self.R):
					self.pixelsres[x,y] = self.pixels[x,y]
					
	def Circle(self):
		for x in range(0,self.width):
			for y in range(0,self.height):
				if ((x-self.x0+self.A)**2+(y-self.y0+self.B)**2 < self.R*self.R):
					self.pixelsres[x,y] = self.pixels[x,y]

	def Polygon(self):
		for x in range(0,self.width):
			for y in range(0,self.height):
				if self.inPolygon(x, y, self.X, self.Y):
					self.pixelsres[x,y] = self.pixels[x,y]
	
	def PolygonInv(self):
		for x in range(0,self.width):
			for y in range(0,self.height):
				if not self.inPolygon(x, y, self.X, self.Y):
					self.pixelsres[x,y] = self.pixels[x,y]
	
	def inPolygon(self, x, y, xp, yp):
		c=0
		for i in range(len(xp)):
			if (((yp[i]<=y and y<yp[i-1]) or (yp[i-1]<=y and y<yp[i])) and \
				(x > (xp[i-1] - xp[i]) * (y - yp[i]) / (yp[i-1] - yp[i]) + xp[i])): c = 1 - c    
		return c

	def GetKB(self, x1, y1, x2, y2):
		k = (y2-y1)/(x2-x1)
		return k, y1-k*x1
	def Line(self, k, b, x):
		return k*x+b
	def Rotate(self, x, y, a, b):
		return x*math.cos(a) + y*math.sin(b)+self.x0*2, -x*math.sin(a) + y*math.cos(b)+self.y0*2
	def Transpose(self, x, y, a, b):
		return x - a, y - b
	def Scale(self, x, y, a, b):
		return x*a, y*b
	
	def drawRing(self):
		ringImg = Image.new('RGB', (self.width, self.height), 
				color = (1, 255, 1))
		_x = self.x0+self.ringX
		_y = self.y0+self.ringY
		d = ImageDraw.Draw(ringImg)
		r = self.ringR1
		d.ellipse((_x-r, _y-r, _x+r, _y+r), fill=self.ringColor, outline=self.ringColor)
		r -= self.ringR2
		d.ellipse((_x-r, _y-r, _x+r, _y+r), fill='red')
		_pixelsres = ringImg.load()
		for x in range(0,self.width):
			for y in range(0,self.height):
				if _pixelsres[x,y] == self.ringColor:
					self.pixelsres[x,y] = self.ringColor
			
	def drawBPoly(self):
		polyImg = Image.new('RGBA', (self.width, self.height), 
				color = (1, 1, 1))
		d = ImageDraw.Draw(polyImg)
		for i, x in enumerate(self.polyX):
			d.line((self.x0+self.polyX[i], self.y0+self.polyY[i], 
				self.x0+self.polyX[(i+1 if i != len(self.polyX)-1 else 0)], 
				self.y0+self.polyY[(i+1 if i != len(self.polyX)-1 else 0)]), self.polyColor, width=self.polyWidth)
	
	def drawText(self):
		fontImg = Image.new('RGB', (self.width, self.height), color = (1, 255, 1))
		
		fnt = ImageFont.truetype(self.textFont, self.textSize)
		dd = ImageDraw.Draw(fontImg)
		
		(width, baseline), (offset_x, offset_y) = fnt.font.getsize(self.text)
		ascent, descent = fnt.getmetrics()
		_x = self.x0+self.textX - width/2
		_y = self.y0+self.textY - (ascent+descent)/2
		dd.text((int(_x), int(_y)), self.text, font=fnt, fill=(0, 0, 0))
		textPixelsres = fontImg.load()
		buf = self.bufImg.load()
		for x in range(0,self.width):
			for y in range(0,self.height):
				if not self.invText:
					if textPixelsres[x,y] == (0,0,0):
						self.pixelsres[x,y] = buf[x,y]
				else:
					if textPixelsres[x,y] == (0,0,0):
						self.pixelsres[x,y] = self.pixels[x,y]
	
	def drawGray(self):
		self.imgres = self.imgres.convert("L")

wall = Wall()

def parseArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("-in", "--input_file", type=str, default='in.png', help="Name of input file")
	parser.add_argument("-out", "--output_file", type=str, default='out.png', help="Name of output file")
	
	parser.add_argument("--text", type=str, default='', help="Text")
	parser.add_argument("--text_size", type=int, default=20, help="Text size")
	parser.add_argument("--text_pos", nargs='*', help="Text position")
	parser.add_argument("--text_font", type=str, default='C:/Users/333da/Desktop/genwall/fonts/slkscr.ttf', help="Text font")
	
	parser.add_argument("--ring_color", type=str, default='0:0:0', help="Ring color (r:g:b)")
	parser.add_argument("--ring_pos", nargs='*', help="Ring radius and position (r1 w x y)")
	
	parser.add_argument("--polygon_color", type=str, default='0:0:0', help="Polygon color (r:g:b)")
	parser.add_argument("--polygon_width", type=int, default=1, help="Polygon width")
	parser.add_argument("--polygon_points", nargs='*', help="Polygon points (x1 y1 x2 y2 ...)")
	
	parser.add_argument('--R', nargs='*', help='Set radius x y of blured circle', type=int)
	parser.add_argument('--P', nargs='*', help='Polygon coords of blured polygon', type=int)
	
	parser.add_argument("--inv", action="store_true", help="Inv blur", default=False)
	parser.add_argument("--inv_text", action="store_true", help="Inv text blur", default=False)
	parser.add_argument("--g", action="store_true", help="Gray mode", default=False)
					
	args = parser.parse_args()
	wall.inPath = args.input_file
	wall.outPath = args.output_file
	wall.inv = args.inv
	wall.isGray = args.g
	
	if args.R != None and len(args.R) == 3:
		wall.R = args.R[0]
		wall.A = args.R[1]
		wall.B = args.R[2]
		wall.isCircle = True
	if args.P != None and len(args.P) != 0 and len(args.P) % 2 == 0:
		for i in range(0, len(args.P), 2):
			wall.X.append(args.P[i])
			wall.Y.append(args.P[i+1])
		wall.isPolygon = True
		
	if args.text != '':
		wall.text = args.text
		wall.textFont = args.text_font
		wall.textSize = args.text_size
		wall.textX = 0
		wall.textY = 0
		if args.text_pos != None and len(args.text_pos) == 2:
			wall.textX = int(args.text_pos[0])
			wall.textY = int(args.text_pos[1])
		wall.isText = True
		
	if args.ring_pos != None and len(args.ring_pos) == 4:
		wall.ringR1 = int(args.ring_pos[0])
		wall.ringR2 = int(args.ring_pos[1])
		wall.ringX = int(args.ring_pos[2])
		wall.ringY = int(args.ring_pos[3])
		wall.ringColor = tuple( list(map(int, args.ring_color.split(':'))))
		wall.isRing = True
		
	if args.polygon_points != None and len(args.polygon_points) != 0 and len(args.polygon_points) % 2 == 0:
		for i in range(0, len(args.polygon_points), 2):
			wall.polyX.append(int(args.P[i]))
			wall.polyY.append(int(args.P[i+1]))
		wall.polyWidth = args.polygon_width
		wall.polyColor = tuple(list(map(int, args.polygon_color.split(':'))))
		wall.isBPoly = True
	wall.invText = args.inv_text

parseArgs()
wall.GenWall()

#colorwall.py -in w.Jpeg --P -300 300 300 300 300 -300 -300 -300
#colorwall.py -in w.Jpeg --P -300 300 300 300 300 -300 -300 -300 --inv

#colorwall.py -in w.Jpeg --R 300 0 0
#colorwall.py -in w.Jpeg --R 300 0 0 --inv
#colorwall.py -in w.Jpeg --text "H" --text_size 150 --text_pos 0 0 --R 300 0 0
#colorwall.py -in w.Jpeg --text "HELLOW WORLD" --text_size 55 --text_pos 0 0 --R 300 0 0 --inv_text --inv
#
#colorwall.py -in w.Jpeg --text "HELLOW WORLD" --text_size 55 --text_pos 0 0 --R 300 0 0 --inv_text --inv --ring_color 1:1:1 --ring_pos 300 10 0 0