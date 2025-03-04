from PIL import Image,ImageDraw
import random
from PIL import ImageFilter
import math
import seaborn as sns

PATTREN_HEXAGON_1 = "hex1"
PATTREN_HEXAGON_2 = "hex2"
PATTREN_CUBES = "cubes"
PATTREN_RHOMBUS = "rhombus"

class Config:
    WIDTH = 1920
    HEIGHT = 1080
    
    PATTERN = PATTREN_HEXAGON_1
    
    NAME = "result.png"
    
    COLOR = (255, 255, 255)
    COLOR_PALLITRE = []
    GEN_PALLITRE = False
    RANDOM_COLOR = False
    PALLITRE_SIZE = 8
    PALLITRE_NAME = ""
    
    OUTLINE = False
    OUTLINE_COLOR = (255, 255, 255)
    OUTLINE_RANDOM_COLOR = False
    OUTLINE_SET_SAME_COLOR = False
    
    CUBES_MONOCHROME = False
    
    INPUT_IMAGE = ""
    
    #for romb
    XS = 1
    YS = 2
    DS = 2
    
    HEX_R = 50
    
    HX = 50
    HY = 30
    
class ImGen:
    def __init__(self, config):
        self.config = config
        self.imMap = []
        
        if self.config.GEN_PALLITRE:
            sns.set()
            cur = []
            if self.config.PALLITRE_NAME != "":
                cur = sns.color_palette(self.config.PALLITRE_NAME, self.config.PALLITRE_SIZE)
            else:
                cur = sns.diverging_palette(random.randint(0, 359), random.randint(0, 359), random.randint(0, 100), n=self.config.PALLITRE_SIZE)
            self.config.COLOR_PALLITRE = [(int(x[0]*255),int(x[1]*255),int(x[2]*255)) for x in cur]
            #print(cur)
            
        if self.config.COLOR_PALLITRE == []:
            if self.config.RANDOM_COLOR:
                self.config.COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            
        if self.config.OUTLINE:
            if self.config.OUTLINE_RANDOM_COLOR:
                self.config.OUTLINE_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            elif self.config.OUTLINE_SET_SAME_COLOR and self.config.COLOR_PALLITRE == []:
                self.config.OUTLINE_COLOR = self.getSameColor(self.config.COLOR)
        
        if self.config.INPUT_IMAGE != "":
            self.config.COLOR_PALLITRE = []
    
    def RGBtoHSV(self, r, g, b):
        r, g, b = r/255.0, g/255.0, b/255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx-mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g-b)/df) + 360) % 360
        elif mx == g:
            h = (60 * ((b-r)/df) + 120) % 360
        elif mx == b:
            h = (60 * ((r-g)/df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = (df/mx)*100
        v = mx*100
        #print("HSV",h,s,v)
        return h, s, v
    
    def HSVtoRGB(self, h, s, v):
        i = math.floor(h/60) % 6
        
        vm = ((100-s)*v)/100
        
        a = (v-vm)*(h%60)/60
        
        vi = vm + a
        vd = v - a
        
        r, g, b = [
            (v, vi, vm),
            (vd, v, vm),
            (vm, v, vi),
            (vm, vd, v),
            (vi, vm, v),
            (v, vm, vd)
        ][int(i)]
        #print("RGB",r,g,b)
        return int(r), int(g), int(b)
    
    def getSameColor(self, color, moreShine=False):
        h,s,v = self.RGBtoHSV(color[0],color[1],color[2])
        
        if moreShine:
            s = s + 10 if s+10 < 100 else 100
        else:
            s = s - 10 if s - 10 > 0 else 0
            
        r,g,b = self.HSVtoRGB(h,s,v)
        
        return (r,g,b)
        
    
    def genImage(self):
        if self.config.INPUT_IMAGE != "":
            self.inImg = Image.open(self.config.INPUT_IMAGE)
            self.im = Image.new('RGBA', self.inImg.size)
        else:
            self.im = Image.new('RGBA', (self.config.WIDTH, self.config.HEIGHT))
        self.draw = ImageDraw.Draw(self.im)
        
        if self.config.PATTERN == PATTREN_HEXAGON_1:
            self._genHex1()
        elif self.config.PATTERN == PATTREN_HEXAGON_2 or self.config.PATTERN == PATTREN_CUBES:
            self._genHex2()
        elif self.config.PATTERN == PATTREN_RHOMBUS:
            self._genRomb()
        
        smooth = self.im.filter(ImageFilter.SMOOTH)
        smooth.save(self.config.NAME)
    
    def _genHex1(self):
        y = 0
        x = 0
        R=self.config.HEX_R
        dir=1
        h = R/math.sqrt(3)
        
        genMap = False
        if self.config.COLOR_PALLITRE != []:
            genMap = True
        
        self.imMap = []
        
        while x < self.config.WIDTH + 2*R:
            y=0
            if genMap:
                self.imMap.append([])
            while y < self.config.HEIGHT + 2*R:
                points = []
                alpha = 0
                while alpha < 2*math.pi:
                    points.append((R*math.cos(alpha)+x, R*math.sin(alpha)+y + math.sqrt(3)*R/4*dir))
                    alpha += 2*math.pi/6
                    
                
                if genMap:
                    self.imMap[-1].append([False, points])
                else:
                    if self.config.INPUT_IMAGE != "":
                        _rgb = [0,0,0]
                        for p in points:
                            if p[0] < 0 or p[1] < 0 or p[0] > self.inImg.size[0]  or p[1] > self.inImg.size[1]:
                                continue
                            r, g, b = self.inImg.getpixel(p)
                            _rgb[0]+=r
                            _rgb[1]+=g
                            _rgb[2]+=b
                            
                        _rgb[0] /= len(points)
                        _rgb[1] /= len(points)
                        _rgb[2] /= len(points)
                        self.config.COLOR = (int(_rgb[0]),int(_rgb[1]),int(_rgb[2]))
                    
                    self.draw.polygon(points, fill = self.config.COLOR)
                    #OUTLINE
                    if self.config.OUTLINE:
                        self.draw.polygon(points, outline = self.config.OUTLINE_COLOR)
                y+=R*math.sqrt(3)
            x+=R*1.5
            dir*=-1
        
        if self.config.COLOR_PALLITRE != []:
            self._paintImage()
    
    def _genHex2(self):
        y = 0
        x = 0
        R=self.config.HEX_R
        dir=1
        h = R/math.sqrt(3)

        genMap = False
        if self.config.COLOR_PALLITRE != []:
            genMap = True
        
        self.imMap = []

        while x < self.config.WIDTH + 2*R:
            y=0
            if genMap:
                self.imMap.append([])
            while y < self.config.HEIGHT + 2*R:
                points = []
                alpha = 0
                while alpha < 2*math.pi:
                    points.append((R*math.cos(alpha + math.pi/6)+x + math.sqrt(3)*R/4*dir, R*math.sin(alpha + math.pi/6)+y))
                    alpha += 2*math.pi/6
                    
                    
                if genMap:
                    self.imMap[-1].append([False, points])
                else:
                    if self.config.INPUT_IMAGE != "":
                        _rgb = (0,0,0)
                        for p in points:
                            r, g, b = self.inImg.getpixel(p)
                            _rgb[0]+=r
                            _rgb[1]+=g
                            _rgb[2]+=b
                            
                        _rgb[0] /= len(points)
                        _rgb[1] /= len(points)
                        _rgb[2] /= len(points)
                        self.config.COLOR = _rgb
                    self.draw.polygon(points, fill = self.config.COLOR)
                    #OUTLINE
                    if self.config.OUTLINE and self.config.PATTERN != PATTREN_CUBES:
                        self.draw.polygon(points, outline = self.config.OUTLINE_COLOR)
                    if self.config.PATTERN == PATTREN_CUBES:
                    
                        if not self.config.CUBES_MONOCHROME:
                            colorMore = self.getSameColor(self.config.COLOR, True)
                            colorLess = self.getSameColor(self.config.COLOR)
                            #draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[3], points[4], points[5]], fill = self.config.OUTLINE_COLOR)
                            self.draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[3], points[2], points[1]], fill = colorMore)
                            self.draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[5], points[0], points[1]], fill = colorLess)
                    
                        self.draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[3], points[4], points[5]], outline = self.config.OUTLINE_COLOR)
                        self.draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[3], points[2], points[1]], outline = self.config.OUTLINE_COLOR)
                        self.draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[5], points[0], points[1]], outline = self.config.OUTLINE_COLOR)
                

                y+=R*1.5
                dir*=-1
            x+=R*math.sqrt(3)
        if self.config.COLOR_PALLITRE != []:
            self._paintImage()
    
    def _genRomb(self):
        
        imMap = []
        
        HX = self.config.HX
        HY = self.config.HY
        YS = self.config.YS
        XS = self.config.XS
        DS = self.config.DS
        
        y = 0
        x = 0
        dir=1
        
        genMap = False
        if self.config.COLOR_PALLITRE != []:
            genMap = True
            
        while x < self.config.WIDTH + 2*HX:
            y=0
            if genMap:
                imMap.append([])
            while y < self.config.HEIGHT + 2*HY:
                points = []
                points.append((x - HX + dir*HX/DS, y))
                points.append((x + dir*HX/DS,      y - HY))
                points.append((x + HX + dir*HX/DS, y))
                points.append((x + dir*HX/DS,      y + HY))
                if genMap:
                    imMap[-1].append([False, points])
                else:
                    if self.config.INPUT_IMAGE != "":
                        _rgb = (0,0,0)
                        for p in points:
                            r, g, b = self.inImg.getpixel(p)
                            _rgb[0]+=r
                            _rgb[1]+=g
                            _rgb[2]+=b
                            
                        _rgb[0] /= len(points)
                        _rgb[1] /= len(points)
                        _rgb[2] /= len(points)
                        self.config.COLOR = _rgb
                        if self.config.OUTLINE_SET_SAME_COLOR:
                            self.config.OUTLINE_COLOR = self.getSameColor(self.config.COLOR)
                    self.draw.polygon(points, fill = self.config.COLOR)
                    if self.config.OUTLINE:
                        self.draw.polygon(points, outline = self.config.OUTLINE_COLOR)
                y+=HY*XS
                dir*=-1
            #return
            x+=HX*YS
        if self.config.COLOR_PALLITRE != []:
            self._paintImage()
    
    def _go(self,x, y):
        if self.imMap[x][y][0]:
            return
        
        r = random.randint(0, sum(self.gen))
        
        #selection
        _r = 0
        _id = 0
        while _r < r:
            _r+=self.gen[_id]
            _id+=1
        
        if _id >= self.config.PALLITRE_SIZE:
            _id = self.config.PALLITRE_SIZE-1
        
        self.draw.polygon(self.imMap[x][y][1], fill = self.config.COLOR_PALLITRE[_id])
        #OUTLINE
        if self.config.OUTLINE and self.config.PATTERN != PATTREN_CUBES:
            self.draw.polygon(self.imMap[x][y][1], outline = self.config.OUTLINE_COLOR)
        if self.config.PATTERN == PATTREN_CUBES:
            R=self.config.HEX_R
            _x = (self.imMap[x][y][1][0][0] + self.imMap[x][y][1][3][0]) / 2
            _y = (self.imMap[x][y][1][0][1] + self.imMap[x][y][1][3][1]) / 2
            
            dir = 1 if y % 2 == 0 else -1
            if not self.config.CUBES_MONOCHROME:
                colorMore = self.getSameColor(self.config.COLOR_PALLITRE[_id], True)
                colorLess = self.getSameColor(self.config.COLOR_PALLITRE[_id])
                #draw.polygon([(x+ math.sqrt(3)*R/4*dir, y), points[3], points[4], points[5]], fill = self.config.OUTLINE_COLOR)
                self.draw.polygon([(_x+ math.sqrt(3)*R/4*dir, _y), points[3], points[2], points[1]], fill = colorMore)
                self.draw.polygon([(_x+ math.sqrt(3)*R/4*dir, _y), points[5], points[0], points[1]], fill = colorLess)
            
            if self.config.OUTLINE_SET_SAME_COLOR:
                self.config.OUTLINE_COLOR = self.getSameColor(self.config.COLOR_PALLITRE[_id])
            self.draw.polygon([(_x+ math.sqrt(3)*R/4*dir, _y), points[3], points[4], points[5]], outline = self.config.OUTLINE_COLOR)
            self.draw.polygon([(_x+ math.sqrt(3)*R/4*dir, _y), points[3], points[2], points[1]], outline = self.config.OUTLINE_COLOR)
            self.draw.polygon([(_x+ math.sqrt(3)*R/4*dir, _y), points[5], points[0], points[1]], outline = self.config.OUTLINE_COLOR)
                
        
        
        self.imMap[x][y][0] = True
        
        #mutation
        for i in range(0, len(self.gen)):
            self.gen[i] += random.randint(-5, 5)
            if self.gen[i] <= 0:
                self.gen[i] = 1
        
        if self.config.PATTERN == PATTREN_RHOMBUS:
            if y-1>=0:
                self._go(x, y-1)
            if y+1 < len(self.imMap[0]):
                self._go(x-1, y-1)
            if x+1<len(self.imMap):
                self._go(x+1, y)
            if x-1>=0:
                self._go(x-1, y)
        else:
            if y-1>=0:
                self._go(x, y-1)
            if y-1>=0 and x-1>=0:
                self._go(x-1, y-1)
            if x+1<len(self.imMap):
                self._go(x+1, y)
            if x-1>=0:
                self._go(x-1, y)
            if y+1<len(self.imMap[0]):
                self._go(x, y+1)
            if y+1 < len(self.imMap[0]) and x+1 < len(self.imMap):
                self._go(x+1, y+1)
        
        
    
    def _paintImage(self):
        sx = random.randint(1, len(self.imMap))
        sy = random.randint(1, len(self.imMap[0]))
        
        self.gen = [10 for i in range(len(config.COLOR_PALLITRE))]
        self.draw.polygon(self.imMap[sx][sy][1], fill = self.config.COLOR_PALLITRE[0])
        self.imMap[sx][sy][0] = True
        
        self._go( sx-1, sy-1)
    




config = Config()
config.HEX_R = 50
config.HX = 50
config.HY = 50


#config.GEN_PALLITRE = True
#config.PALLITRE_NAME = "Blues"

#config.COLOR = (122, 122, 143)

config.RANDOM_COLOR = True
config.OUTLINE = True

#config.OUTLINE_COLOR = (155, 166,200)
#config.OUTLINE_RANDOM_COLOR = True
config.OUTLINE_SET_SAME_COLOR = True


config.INPUT_IMAGE = "1.jpg"
config.PATTERN = PATTREN_HEXAGON_1
#config.PATTERN = PATTREN_HEXAGON_2
#config.PATTERN = PATTREN_CUBES
#config.PATTERN = PATTREN_RHOMBUS
#config.CUBES_MONOCHROME = True

config.NAME = "result7.png"

genim = ImGen(config)
genim.genImage()





