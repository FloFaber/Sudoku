import pyscreenshot
import numpy
import cv2
from pytesseract import image_to_string
from PIL import Image
import re


def steal():

    im = pyscreenshot.grab()

    start_y = 336
    end_y = 1045

    start_x = 167
    end_x = 876

    image = numpy.array(im)
    # image = image[start_y:end_y, start_x:start_y]

    image = image[336:1045, 167:876]
    cv2.imwrite("images/test.png", image)

    img_ = Image.open("images/test.png")
    thresh = 240
    fn = lambda x : 255 if x > thresh else 0
    r = img_.convert('L').point(fn, mode='1')
    r.save("images/test.png")

    img = cv2.imread("images/test.png")

    w = image.shape[0]
    h = image.shape[1]

    cut = 3
    for x in range(9):
        for y in range(9):

            start_x = round(w / 9 * x) + cut
            start_y = round(h / 9 * y) + cut

            end_x = start_x + round(w / 9) - cut * 2
            end_y = start_y + round(h / 9) - cut * 2

            i = img[start_y:end_y, start_x:end_x]
            cv2.imwrite("images/" + str(y) + "-" + str(x) + ".png", i)

    grid = open("grids/1.txt", "w")

    print("\n-------------------------------")
    for x in range(9):
        for y in range(9):
            text = image_to_string(cv2.imread("images/" + str(x) + "-" + str(y) + ".png"), config='--psm 6')
            text = re.sub("[^0-9]", "", text)
            if not text.isnumeric():
                text = "0"
                pass

            end_ = ","
            if y == 2 or y == 5 or y == 8:
                end = " | "
            else:
                end = "  "

            text_ = text
            if y == 0:
                text = "| " + text

            if y == 8:
                grid.write(text_)
            else:
                grid.write(text_ + end_)

            print(text, end=end)
        if x == 2 or x == 5 or x == 8:
            print("\n-------------------------------")
        else:
            print()
        grid.write("\n")

    grid.close()
    return
