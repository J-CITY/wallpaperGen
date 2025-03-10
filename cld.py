import cv2
import numpy as np
import argparse

image_filename = "image/in.jpg"#sys.argv[1]
out_filename = "result.jpg"
color_image = cv2.imread(image_filename, cv2.IMREAD_COLOR)

height = color_image.shape[0]
width  = color_image.shape[1]
channel = color_image.shape[2]

gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)


M_0 = np.average(gray_image)
N = 32
threshold = 0.2

local_CLD = np.zeros((height, width, N))
for i in range(N):
    angle = i * 2 * np.pi / N
    for y in range(height):
        for x in range(width):
            progress = np.round(100*(i*height*width+y*width+x)/(N*width*height), 2)
            print( "Progress 1: ", str(progress)+"%", end='\r' )
            l = 0
            s = gray_image[y, x].astype(float)
            while(True):
                l += 1
                xx = x + int(l * np.cos(angle))
                yy = y + int(l * np.sin(angle))
                if not (yy < 0 or yy >= height or xx <= 0  or xx >= width):
                    s += gray_image[yy, xx]
                if (s/l - M_0) / M_0 <= threshold:
                    local_CLD[y,x,i] = l
                    break
L = 4
brushstroke_size = np.zeros((height, width))
for y in range(height):
    for x in range(width):
        brushstroke_size[y,x] = N * L / np.sum(local_CLD[y,x])

oil_image = np.zeros((height, width, channel))
for y in range(height):
    for x in range(width):
        progress = np.round(100*(y*width+x)/(width*height), 2)
        print( "Progress 2: ", str(progress)+"%", end='\r' )
        R = int(np.ceil(brushstroke_size[y,x]))
        local_histogram = np.zeros(256)
        local_channel_count = np.zeros((channel, 256))
        for dy in range(-R, R):
            for dx in range(-R, R):
                yy = y+dy
                xx = x+dx
                if dy*dy + dx*dx > R*R:
                    continue
                if yy < 0  or yy >= height or xx <= 0  or xx >= width:
                    continue
                intensity = gray_image[yy, xx]
                local_histogram[intensity] += 1
                for c in range(channel):
                    local_channel_count[c, intensity] += color_image[yy, xx, c]

        max_intensity = np.argmax(local_histogram)
        max_intensity_count = local_histogram[max_intensity]
        for c in range(channel):
            oil_image[y,x,c] = local_channel_count[c, max_intensity] / max_intensity_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Image cld effect")
    parser.add_argument('-input', type=str, help="Input image")
    parser.add_argument('-output', type=str, help="Output image")
    parser.add_argument('-N', type=int, help="N range")
    parser.add_argument('-threshold', type=int, help="Threshold")
    args = parser.parse_args()

    if args.input is not None:
        image_filename = args.input
    if args.output is not None:
        out_filename = args.output
    if args.N is not None and args.N > 0:
        N = args.N
    if args.threshold is not None and args.threshold > 0:
        threshold = args.threshold

    oil_image = oil_image.astype('int')
    cv2.imwrite(out_filename, oil_image)
    #cv2.imwrite("_"+out_filename, oil_image[50:100, 50:150])