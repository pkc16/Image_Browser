# Image viewer

from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import os
import pathlib

root = Tk()
root.title('Image Viewer Application')

# Set minsize for rows and columns so narrow images don't shrink the main window
root.grid_columnconfigure(0, minsize=341)
root.grid_columnconfigure(1, minsize=341)
root.grid_columnconfigure(2, minsize=341)
root.grid_rowconfigure(2, minsize=768)

def getDirectory():
	# get directory containing images to be viewed
	os.chdir("C:\\")
	path = filedialog.askdirectory(initialdir="C:", title="Select a Directory which has images")
	os.chdir(path)
	return path


def getImagesList(dirPath):
	# return a list of image files in the directory
	dirComponents = []
	for foldername, subfoldername, filename in os.walk(dirPath):
		dirComponents.append(filename)

	# filenames are contained (as a list) inside the first element of the list
	listFiles = []
	listFiles = dirComponents[0]

	# remove any files from the list which are not images
	typeList = ['jpg','png', 'gif','tif']
	listFiles = [file for file in listFiles if pathlib.Path(file).suffix[1:] in typeList]

	return listFiles


def resizeImages(listImageFiles):
	# This function resizes images if they are too big and returns a list of ImageTk.PhotoImage objects 
	global image_list
	image_list = []
	maxWidth = 1024
	maxHeight = 768

	for i, image in enumerate(listImageFiles):
		# Check the image dimensions and resize if too big
		temp_image = Image.open(listImageFiles[i])
		width, height = temp_image.size
		divisor = 1.0
		aspectRatio = width/height

		if width >= height:
			# For images which have longer or same width as height, resize to no greater than 1024 W x 768 H
			if width > maxWidth:
				divisor = width/maxWidth
		else:
			# For images which have shorter width than height, resize to no greater than 768 W x 1024 H
			if height > maxHeight:
				divisor = height/maxHeight

		newWidth = int(round(width/divisor))
		newHeight = int(round(height/divisor))

		# If either of newly calculated dimensions still exceeds a max dimension, scale image using aspect ratio
		if newWidth > maxWidth:
			# set the width to the max width and scale the height
			newWidth = maxWidth
			newHeight = int(round(newWidth/aspectRatio))
		elif newHeight > maxHeight:
			# set the height to the max height and scale the width
			newHeight = maxHeight
			newWidth = int(round(newHeight/aspectRatio))

		temp_image = temp_image.resize((newWidth, newHeight), Image.ANTIALIAS)
		newimage = ImageTk.PhotoImage(temp_image)

		image_list.append(newimage)

	return image_list


def forward(image_index):
	# forward button
	global lblImage
	global lblFile
	global lblImageCounter
	global btnForward
	global btnBack

	lblImage.grid_forget()
	lblImage = Label(image=image_list[image_index - 1])
	lblImageCounter.grid_forget()
	lblImageCounter = Label(root, text=str(image_index) + ' of ' + str(len(image_list)))
	lblFile.grid_forget()
	lblFile = Label(root, text=listImages[image_index - 1])
	btnForward = Button(root, text=">>", command=lambda: forward(image_index + 1))
	btnBack = Button(root, text="<<", command=lambda: back(image_index - 1))

	# if at final image, disable the forward button
	if image_index == len(image_list):
		btnForward = Button(root, text=">>", state=DISABLED)

	lblImage.grid(row=2, column=0, columnspan=3)
	lblFile.grid(row=0, column=2, sticky=E)
	lblImageCounter.grid(row=1, column=0, sticky=W)
	btnBack.grid(row=3, column=0)
	btnForward.grid(row=3, column=2)
	

def back(image_index):
	# back button
	global lblImage
	global lblFile
	global lblImageCounter
	global btnForward
	global btnBack

	lblImage.grid_forget()
	lblImage = Label(image=image_list[image_index - 1])
	lblImageCounter.grid_forget()
	lblImageCounter = Label(root, text=str(image_index) + ' of ' + str(len(image_list)))
	lblFile.grid_forget()
	lblFile = Label(root, text=listImages[image_index - 1])
	btnForward = Button(root, text=">>", command=lambda: forward(image_index + 1))
	btnBack = Button(root, text="<<", command=lambda: back(image_index - 1))

	# if at the first image, disable the back button
	if image_index == 1:
		btnBack = Button(root, text="<<", state=DISABLED)

	lblImage.grid(row=2, column=0, columnspan=3)
	lblFile.grid(row=0, column=2, sticky=E)
	lblImageCounter.grid(row=1, column=0, sticky=W)
	btnBack.grid(row=3, column=0)
	btnForward.grid(row=3, column=2)


def center_window(width, height):
	# center window on screen

    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()

    # get x.y coordinates
    x = (screenWidth/2) - (width/2)
    y = (screenHeight/2) - (height/2)
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))


def doAll():
	# This function does everything
	global lblDir
	lblDir.grid_forget()
	lblDir = Label(root, text='Loading images...please wait...')
	lblDir.grid(row=0, column=0, columnspan=2, sticky=W)

	# Disable browse button while images are being loaded
	btnChangeDir = Button(root, text="Browse", command=doAll, state=DISABLED)
	btnChangeDir.grid(row=3, column=3)

	global lblImageCounter
	lblImageCounter.grid_forget()
	lblImageCounter = Label(root, text='')
	lblImageCounter.grid(row=1, column=0, sticky=W)

	global lblImage
	lblImage.grid_forget()
	lblImage = Label(root, image='')
	lblImage.grid(row=2, column=0, columnspan=3)

	global lblFile
	lblFile.grid_forget()
	lblFile = Label(root, text='')
	lblFile.grid(row=0, column=2, sticky=E)

	directoryPath = getDirectory()

	global listImages
	listImages = getImagesList(directoryPath)
	if len(listImages) == 0:
		lblDir.grid_forget()
		lblDir = Label(root, text=f'There were no image files in {directoryPath}')
		lblDir.grid(row=0, column=0, columnspan=2, sticky=W)

		# Set button states when directory contains no images to display
		btnBack = Button(root, text="<<", command=back, state=DISABLED)
		btnBack.grid(row=3, column=0)
		btnForward = Button(root, text=">>", command=lambda: forward(2), state=DISABLED)
		btnForward.grid(row=3, column=2)
		btnExit = Button(root, text="Exit", command=root.destroy)
		btnExit.grid(row=3, column=1)
		btnChangeDir = Button(root, text="Browse", command=doAll)
		btnChangeDir.grid(row=3, column=3)
		return

	global image_list
	image_list = []
	image_list = resizeImages(listImages)

	lblImage.grid_forget()
	lblImage = Label(root, image=image_list[0])
	lblImage.grid(row=2, column=0, columnspan=3)
	
	lblDir.grid_forget()
	lblDir = Label(root, text=directoryPath)
	lblDir.grid(row=0, column=0, columnspan=2, sticky=W)
	
	lblImageCounter.grid_forget()
	lblImageCounter = Label(root, text='1 of ' + str(len(image_list)))
	lblImageCounter.grid(row=1, column=0, sticky=W)

	lblFile.grid_forget()
	lblFile = Label(root, text=listImages[0])
	lblFile.grid(row=0, column=2, sticky=E)

	btnBack = Button(root, text="<<", command=back, state=DISABLED)
	btnExit = Button(root, text="Exit", command=root.destroy)
	if len(image_list) == 1:
		btnForward = Button(root, text=">>", command=lambda: forward(2), state=DISABLED)
	else:
		btnForward = Button(root, text=">>", command=lambda: forward(2))

	btnBack.grid(row=3, column=0)
	btnExit.grid(row=3, column=1)
	btnForward.grid(row=3, column=2)

	btnChangeDir = Button(root, text="Browse", command=doAll)
	btnChangeDir.grid(row=3, column=3)

	center_window(1100,850)



# Need to create variables so they can be referenced in doAll function
lblDir = Label(root, text='')
lblImageCounter = Label(root, text='')
lblImage = Label(root, image='')
lblFile = Label(root, text='')

btnChangeDir = Button(root, text="Browse", command=doAll)
btnChangeDir.grid(row=3, column=3)

center_window(1100,850)

root.mainloop()
