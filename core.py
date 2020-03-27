import cv2
import numpy as np
from joblib import dump, load
from random import randint
import glob


class Frame:
    def __init__(self, img):
        self.img = img
        self.area = 0

    def calc_area(self,
                  lower_green=np.array([25, 100, 0]),
                  upper_green=np.array([60, 255, 230])):

        image = self.img
        hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv_image, lower_green, upper_green)
        res = cv2.bitwise_and(image, image, mask=mask)
        gray_res = cv2.cvtColor(res, cv2.COLOR_RGB2GRAY)
        nonzero = cv2.countNonZero(gray_res)
        self.area = nonzero
        return nonzero

class Analysis:
    def __init__(self, area):
        self.area = area
        self.mass = 0
        self.day = 0

        self.area2mass = load('area2mass.joblib')
        self.day2mass = load('day2mass.joblib')
        self.area2day = load('area2day.joblib')

    def get_mass(self):
        if self.area < 700000:
            self.mass = 0
        elif self.area > 8000000:
            self.mass = 120
        else:
            area = np.array([self.area])
            area = area[:, np.newaxis]
            mass = self.area2mass.predict(area)
            self.mass = round(mass[0], 2)

        return self.mass

    def get_day(self):
        if self.area > 8000000:
            self.day = 40
        else:
            area = np.array([self.area])
            area = area[:, np.newaxis]
            day = self.area2day.predict(area)
            self.day = round(day[0], 2)

        return self.day

class Core(Frame, Analysis):
    def __init__(self, filename):
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        frame = Frame(img)
        self.area = frame.calc_area()

        an = Analysis(frame.area)
        self.mass = an.get_mass()
        self.day = an.get_day()





if __name__ == '__main__':

    files = glob.glob("D:\\iFarm_data\\Ligtning_power\\YD_04_top\\*\\*.JPG")
    filename = files[randint(0, len(files))]

    core=Core(filename)

    print(f"area = {core.area}")
    print(f"mass = {core.mass}")
    print(f"day = {core.day}")