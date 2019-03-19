import os
import cv2
import sys
import shutil
import glob

counter = 0


def save(img, ctr):
    global counter
    cv2.imwrite("temp/temp" + str(counter) + str(ctr) + ".jpg", img)
    counter += 1


def rot():
    for filename in glob.iglob('temp/*.jpg'):
        os.system("python correct_skew.py -i " + filename)


def read():
    global counter
    for filename in glob.iglob('temp/*.jpg'):
        os.system("tesseract " + filename + " out"+str(counter))
	counter +=1
	


def aa(c):
    image = cv2.imread('temp/crop' + str(c) + '.jpg', 0)
    save(image, c)

    image = cv2.imread('temp/crop' + str(c) + '.jpg', cv2.CV_LOAD_IMAGE_GRAYSCALE)
    thresh = 127
    image = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]
    save(image, c)

    image = cv2.bitwise_not(image)
    save(image, c)

    image = cv2.imread('temp/crop' + str(c) + '.jpg')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gray = cv2.medianBlur(gray, 3)
    save(gray, c)

    ar = list(range(-250, 250, 90))

    for i in ar:
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, float(i)/10.0, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h),
                                 flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        save(rotated, c)

    rot()
    read()

if os.path.exists("temp.temp"):
    os.remove("temp.temp")

img_name = sys.argv[1]
retvalue = os.system("./darknet detector test obj.data yolo-obj.cfg yolo-obj_2300.weights " + img_name)
coords = []

if os.path.exists("temp"):
    shutil.rmtree("temp")

os.makedirs("temp")

file = open("temp.temp")

for line in file:
    coords.append(line.replace('\n', ''))

count = (len(coords)) / 4
print(count)
padding = 10
img = cv2.imread(img_name)

for line in range(0, int(count)):
    crop_img = img[int(coords[2 + 4 * line]) - padding:int(coords[3 + 4 * line]) + padding,
               int(coords[0 + 4 * line]) - padding:int(coords[1 + 4 * line]) + padding]
    cv2.imwrite("temp/crop" + str(line) + ".jpg", crop_img)
    aa(line)
