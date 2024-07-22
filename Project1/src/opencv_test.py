import cv2

#opening image 
image_file = "Project1/test-files/jpg_image1.jpeg"
img = cv2.imread(image_file)

#cv2.imshow("original image", img)
#cv2.waitKey(0)

#inverted image
#inverted_image = cv2.bitwise_not(img)
#cv2.imwrite("Project1/temp/inverted.jpg", inverted_image)
#cv2.imshow("Inverted Image", inverted_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

#binarization
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray_image = grayscale(img)
cv2.imwrite("Project1/temp/gray.jpg", gray_image)
#cv2.imshow("Grayscale Image", gray_image)
#cv2.waitKey(3000)
#cv2.destroyAllWindows()

thresh, im_bw = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY)
cv2.imwrite("Project1/temp/bw_image.jpg", im_bw)


#noise removal (not particularly necessary for our goal)
def noise_removal(image):
    import numpy as np
    kernal = np.ones((1, 1), np.uint8)
    image = cv2.dilate(image, kernal, iterations=1)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    image = cv2.medianBlur(image, 3)
    return(image)

no_noise = noise_removal(im_bw)
cv2.imwrite("Project1/temp/no_noise.jpg", no_noise)

#dilation and erosion (for font thats too thick or thin, not particularly necessary for this use case)
def thin_font(image):
    import numpy as np
    image = cv2.bitwise_not(image)
    kernel = np.ones((1, 1), np.uint8)
    image = cv2.erode(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return(image)

eroded_image = thin_font(no_noise)
cv2.imwrite("Project1/temp/eroded.jpg", eroded_image)

#adding borders
color = [0,0,0]
top, bottom, left, right = [50]*4

image_with_border = cv2.copyMakeBorder(no_noise, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
cv2.imwrite("Project1/temp/withBorder.jpg", image_with_border)








