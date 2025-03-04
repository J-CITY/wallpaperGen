from enum import Enum
import argparse
from PIL import Image
import json

class Ditherer(Enum):
    none = 0,
    floyd_steinberg = 1,
    atkinson = 2,
    jjn = 3,
    burkes = 4,
    sierra = 5,
    sierra_lite = 6

    def __str__(self):
        return self.value

class Config:
    inFile = "in.jpg"
    outFile = "out.png"
    theme = "Aura"
    dither = Ditherer.none

config = Config()
channels = 0
height = 0
width = 0
pixels = None

def parseArgs():
    parser = argparse.ArgumentParser(prog='colorizer')
    parser.add_argument('--inFile', type=str, help='Input image file')
    parser.add_argument('--outFile', type=str, help='Output image file name')
    parser.add_argument('--theme', type=str, help='Palette theme')
    parser.add_argument('--dither', choices=Ditherer.__members__, help='Ditherer type')
    args = parser.parse_args()

    if args.inFile != None:
        config.inFile = args.inFile
    if args.outFile != None:
        config.outFile = args.outFile
    if args.dither != None:
        config.dither = args.dither
    if args.theme != None:
        config.theme = args.theme

def updatePixel(img, x, y, err, mul, div):
    if x < 0 or x >= width:
        return
    if y < 0 or y >= height:
        return
    #pixel = img[y, x]
    #r = pixel[0] + err[0] * mul / div
    #g = pixel[1] + err[1] * mul / div
    #b = pixel[2] + err[2] * mul / div

    r = img.getpixel((x, y))[0] + err[0] * mul / div
    g = img.getpixel((x, y))[1] + err[1] * mul / div
    b = img.getpixel((x, y))[2] + err[2] * mul / div

    #r = pixels[x, y][0] + err[0] * mul / div
    #g = pixels[x, y][1] + err[1] * mul / div
    #b = pixels[x, y][2] + err[2] * mul / div

    clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

    clamp(r, 0, 255)
    clamp(g, 0, 255)
    clamp(b, 0, 255)

    #img[y, x] = (255,0,0)
    #print(r,g,b)
    img.putpixel((x,y), (int(r),int(g),int(b)))
    #pixels[y, x] = (r,g,b)


def dither_floyd_steinberg(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 7, 16)
    if y + 1 >= height:
        return
    updatePixel(img, x - 1, y + 1, err, 3, 16)
    updatePixel(img, x + 0, y + 1, err, 5, 16)
    updatePixel(img, x + 1, y + 1, err, 1, 16)

def dither_atkinson(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 1, 8)
    updatePixel(img, x + 2, y + 0, err, 1, 8)
    if y + 1 >= height:
        return
    updatePixel(img, x - 1, y + 1, err, 1, 8)
    updatePixel(img, x + 0, y + 1, err, 1, 8)
    updatePixel(img, x + 1, y + 1, err, 1, 8)
    if y + 2 >= height:
        return
    updatePixel(img, x + 1, y + 2, err, 1, 8)

def dither_jjn(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 7, 48)
    updatePixel(img, x + 2, y + 0, err, 5, 48)
    if y + 1 >= height:
        return
    updatePixel(img, x - 2, y + 1, err, 3, 48)
    updatePixel(img, x - 1, y + 1, err, 5, 48)
    updatePixel(img, x + 0, y + 1, err, 7, 48)
    updatePixel(img, x + 1, y + 1, err, 5, 48)
    updatePixel(img, x + 2, y + 1, err, 3, 48)
    if y + 2 >= height:
        return
    updatePixel(img, x - 2, y + 2, err, 1, 48)
    updatePixel(img, x - 1, y + 2, err, 3, 48)
    updatePixel(img, x + 0, y + 2, err, 5, 48)
    updatePixel(img, x + 1, y + 2, err, 3, 48)
    updatePixel(img, x + 2, y + 2, err, 1, 48)

def dither_burkes(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 8, 32)
    updatePixel(img, x + 2, y + 0, err, 4, 32)
    if y + 1 >= height:
        return
    updatePixel(img, x - 2, y + 1, err, 2, 32)
    updatePixel(img, x - 1, y + 1, err, 4, 32)
    updatePixel(img, x + 0, y + 1, err, 8, 32)
    updatePixel(img, x + 1, y + 1, err, 4, 32)
    updatePixel(img, x + 2, y + 1, err, 2, 32)

def dither_sierra(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 5, 32)
    updatePixel(img, x + 2, y + 0, err, 3, 32)
    if y + 1 >= height:
        return
    updatePixel(img, x - 2, y + 1, err, 2, 32)
    updatePixel(img, x - 1, y + 1, err, 4, 32)
    updatePixel(img, x + 0, y + 1, err, 5, 32)
    updatePixel(img, x + 1, y + 1, err, 4, 32)
    updatePixel(img, x + 2, y + 1, err, 2, 32)
    if y + 2 >= height:
        return
    updatePixel(img, x - 1, y + 2, err, 2, 32)
    updatePixel(img, x + 0, y + 2, err, 3, 32)
    updatePixel(img, x + 1, y + 2, err, 2, 32)

def dither_sierra_lite(img, x, y, err):
    updatePixel(img, x + 1, y + 0, err, 2, 4)
    if y + 1 >= height:
        return
    updatePixel(img, x - 1, y + 1, err, 1, 4)
    updatePixel(img, x + 0, y + 1, err, 1, 4)

from multiprocessing.pool import ThreadPool as Pool
# from multiprocessing import Pool

pool_size = 15

def worker(y, img, palette, dither):
    global config
    global width
    global height
    global channels
    for x in range(0, width):
        old_color = img.getpixel((x, y))
        #old_color = img[y, x]
        error = None #error color
        min_diff = -1
        for color in palette:
            dr = old_color[0] - color[0]
            dg = old_color[1] - color[1]
            db = old_color[2] - color[2]
            diff = dr * dr + dg * dg + db * db
            if min_diff == -1 or diff < min_diff:
              min_diff = diff
              #img[y,x] = color
              img.putpixel((x,y), color)
              error = (dr, dg, db)
        if dither == Ditherer.none:
            break
        if dither == Ditherer.floyd_steinberg:
            dither_floyd_steinberg(img, x, y, error)
        if dither == Ditherer.atkinson:
            dither_atkinson(img, x, y, error)
        if dither == Ditherer.jjn:
            dither_jjn(img, x, y, error)
        if dither == Ditherer.burkes:
            dither_burkes(img, x, y, error)
        if dither == Ditherer.sierra:
            dither_sierra(img, x, y, error)
        if dither == Ditherer.sierra_lite:
            dither_sierra_lite(img, x, y, error)
def recolor(img, palette, dither):
    global config
    global width
    global height
    global channels
    
    pool = Pool(pool_size)
    for y in range(0, height):
        #print(y)
        #worker(y, img, palette, dither)
        pool.apply_async(worker, args=(y, img, palette, dither))
    pool.close()
    pool.join()

def main():
    global config
    global width
    global height
    global channels
    global pixels

    parseArgs()
    print(config.inFile)
    print(config.outFile)
    #print(config.dither)
    print(config.theme)

    if config.inFile == "":
        print("Input file is empty")
        return

    #print(config.inFile)
    
    #image = cv2.imread(config.inFile)
    #width = image.shape[1]
    #height = image.shape[0]
    #channels = image.shape[2]

    image = Image.open(config.inFile)
    channels = len(image.split())
    width, height = image.size
    pixels = image.load()

    data = json.load(open('themes.json'))
    themeData = data["themes"][0]
    for value in data["themes"]:
        #print(value["name"])
        if config.theme == value["name"]:
            themeData = value
            break

    palette = []
    for k, v in themeData.items():
        if k == "name":
            continue
        h = v.lstrip('#')
        palette.append(tuple(int(h[i:i+2], 16) for i in (0, 2, 4)))
    #print(palette)
    recolor(image, palette, config.dither)

    print("Save to: " + config.outFile)
    image.save(config.outFile)
    #cv2.imwrite(config.outFile, image)


if __name__ == "__main__":
    main()
