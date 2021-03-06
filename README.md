# Handwritten mathematical equation solver

## Details: 

There are 2 parts of this project:

### 1. Training:

This part is implemented in the **GenData.py** file. When you call the Train(img) function, it opens the image stored on the path provided as argument to this function. After this it will just make contours on the image and ask you to input what is contained in that green box. After all this is done, it saves all this information in two files *project/code/learned/classifications.txt* and *project/code/learned/flattened_images.txt*. After all this when you head over to the **TrainAndTest.py** file, and run the Test(imgPath) function. It will first of all head over to the files *project/code/learned/classifications.txt* and *project/code/learned/flattened_images.txt*, open these files and train a K-Nearest Neighbour algorithm using the data from these files.

### 2. Testing:
After the training is done, the algorithm will go and open the image whose path is provided in the imgPath argument. The algorithm will apply some openCV pre processing and then find contours the same way it did in the **GenData.py** file, except this time the algorithm will identify the letters in the image except asking for them. After it is done identifying the letters in the image, it will go in the **WolframAlpha.py** and run the getResult function to solve the equation.

## Limitations:

-Since the algoritm is trained with text written on white paper with a black marker, it will work on the same style only. The accuracy is not perfect due to lack of training data, feel free to add your own images.

-It will only solve upto cubic equtaions. However, you can make changes in the **WolframAlpha.py** file to make it work with heigher degree polynomials.

## Installations Required:

-[OpenCV](https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_setup/py_setup_in_windows/py_setup_in_windows.html)

-[WolframAlpha](https://pypi.org/project/wolframalpha/)

## References:

-[OpenCV 3 KNN Character Recognition Python](https://github.com/MicrocontrollersAndMore/OpenCV_3_KNN_Character_Recognition_Python)

-[Build an AI Assistant with Wolfram Alpha and Wikipedia in Python](https://medium.com/@salisuwy/build-an-ai-assistant-with-wolfram-alpha-and-wikipedia-in-python-d9bc8ac838fe)
