from PIL import Image, ImageDraw
from enum import Enum
from random import randint
import numpy as np
import argparse

class Type(Enum):
	TRIANGLE = 1
	VORONOI = 2

class Config:
	path = "image/in.jpg"
	xStep = 10
	yStep = 10
	outName = "out.png"
	type = Type.TRIANGLE
	xDispersion = 7
	yDispersion = 7

def convertImage(config):
	if config.path == "":
		return
	image = Image.open(config.path)
	width, height = image.size
	print(width, height)
	w = 0
	h = 0
	points = []
	while w < width+config.xStep:
		h = 0
		while h < height+config.yStep:
			x = w + randint(-config.xDispersion, config.xDispersion)
			if x < 0:
				x = 0
			if x >= width:
				x = width-1
			
			y = h + randint(-config.yDispersion, config.yDispersion)
			if y < 0:
				y = 0
			if y >= height:
				y = height-1
			points.append([x, y])
			h += config.yStep
		w += config.xStep
			
	resimage = Image.new('RGB', (width, height))
	
	from scipy.spatial import Delaunay, Voronoi
	draw = ImageDraw.Draw(resimage)
	px = image.load()
	
	if config.type == Type.TRIANGLE:
		_points = np.array(points)
		polygons = Delaunay(points)
		for item in polygons.simplices:
			polygon = []
			r, g, b = 0, 0, 0
			for e in item:
				_x, _y = points[e][0], points[e][1]
				_r, _g, _b = px[_x, _y][0], px[_x, _y][1], px[_x, _y][2]
				r += _r
				g += _g
				b += _b
				polygon.append(tuple(points[e]))
			n = len(item)
			draw.polygon(polygon, fill = (int(r/n), int(g/n), int(b/n)))
		
	if config.type == Type.VORONOI:
		w = 0
		while w < width+config.xStep:
			h = 0
			while h < height+config.xStep:
				x = w
				if x >= width:
					x = width-1
				y = h
				if y >= height:
					y = height-1
				if x == 0 or y == 0 or y == height-1 or x == width-1:
					points.append([x, y])
				if x == 0:
					points.append([x-50, y])
				if x == width-1:
					points.append([x+50, y])
				if y == 0:
					points.append([x, y-50])
				if y == height-1:
					points.append([x, y+50])
				h += config.yStep
			w += config.xStep
		
		_points = np.array(points)
		polygons = Voronoi(points)
		vertices = polygons.vertices
		for item in polygons.regions:
			if len(item) <= 2:
				continue
			polygon = []
			r, g, b = 0, 0, 0
			
			for e in item:
				if e < 0:
					break
				_x, _y = int(vertices[e][0]), int(vertices[e][1])
				if _x >= width:
					_x = width-1
				if _x < 0 :
					_x = 0
				if _y >= height:
					_y = height-1
				if _y < 0:
					_y = 0
				_r, _g, _b = px[_x, _y][0], px[_x, _y][1], px[_x, _y][2]
				r += _r
				g += _g
				b += _b
				polygon.append((_x, _y))
			if len(polygon) > 2:
				n = len(item)
				draw.polygon(polygon, fill = (int(r/n), int(g/n), int(b/n)))
		
	resimage.save(config.outName)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(prog="Triangulate effect")
	parser.add_argument('-input', type=str, help="Input image")
	parser.add_argument('-output', type=str, help="Output image")
	parser.add_argument('-xDispersion', type=int, help="xDispersion default 7")
	parser.add_argument('-yDispersion', type=int, help="yDispersion default 7")
	parser.add_argument('-xStep', type=int, help="x step default 10")
	parser.add_argument('-yStep', type=int, help="y step default 10")
	parser.add_argument('-type', type=str, help="type TRIANGLE or VORONOI")
	parser.set_defaults(isFront=False)

	xStep = 10
	yStep = 10
	type = Type.TRIANGLE

	args = parser.parse_args()
	config = Config()
	if args.input is not None:
		config.path = args.input
	if args.output is not None:
		config.outName = args.output
	if args.xDispersion is not None and args.xDispersion > 0:
		config.xDispersion = args.xDispersion
	if args.yDispersion is not None and args.yDispersion > 0:
		config.yDispersion = args.yDispersion
	if args.xStep is not None and args.xStep > 0:
		config.xStep = args.xStep
	if args.yStep is not None and args.yStep > 0:
		config.yStep = args.yStep
	if args.type is not None and args.type > 0:
		if args.type == "TRIANGLE":
			config.type = Type.TRIANGLE
		elif args.type == "VORONOI":
			config.type = Type.VORONOI
	convertImage(config)




















