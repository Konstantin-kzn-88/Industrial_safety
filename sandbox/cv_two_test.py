import cv2 as cv
import sys
file_path = 'C:\\Users\\Konstantin_user\\Desktop\\test_in.jpg'
img = cv.imread(cv.samples.findFile(file_path))
if img is None:
    sys.exit("Could not read the image.")
cv.imshow("Display window", img)
k = cv.waitKey(0)
if k == ord("s"):
    cv.imwrite("C:\\Users\\Konstantin_user\\Desktop\\test_out.png", img)

if __name__ == '__main__':
    pass