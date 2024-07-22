from PIL import Image

im_file = "Project1/test-files/jpg_image1.jpeg"

im = Image.open(im_file)
print(im.size)
im.show()
im.save("Project1/temp/jpg_image1.jpg")
