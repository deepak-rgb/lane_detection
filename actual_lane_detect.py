import cv2
import numpy as np

url = 'http://192.168.43.1:8080/video'


def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)  # grayscaling
    blur = cv2.GaussianBlur(gray, (5, 5), 0)  # reducing noise using gaussian filter
    canny = cv2.Canny(blur, 50, 150)  # canny edge detection
    return canny


def display_lines(image, lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 3)
    return line_image


def region_of_interest(image):
    # get height
    width = image.shape[1]  # get width
    polygon = np.array([
        [(240, 670), (width, 670), (900, 450), (600, 450)]
    ])  # make a contour of required shape
    mask = np.zeros_like(image)  # creat the array with black
    cv2.fillPoly(mask, polygon, 255)  # fill the contour shape with white
    masked_image = cv2.bitwise_and(image, mask)  # bitwise 'and to get required shape
    return masked_image


cap = cv2.VideoCapture('C:\\Users\\deepa\\Downloads\\test1.mp4')  # 'C:\\Users\\deepa\\Downloads\\test1.mp4'
while cap.isOpened():
    _, frame = cap.read()

    canny_image = canny(frame)
    cropped_image = region_of_interest(canny_image)
    lines = cv2.HoughLinesP(cropped_image, 3, np.pi / 180, 100, maxLineGap=100)
    # averaged_lines = average_slope_intercept(lane_image, lines)
    line_image = display_lines(frame, lines)
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    cv2.imshow('res', combo_image)
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
