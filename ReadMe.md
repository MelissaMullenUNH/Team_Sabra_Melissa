# README for Sabra and Melissa's Group Implementation Project

## Attention Detection

## 1. Objective of project
The goal of this project was to create a method of detecting if someone in a picture is looking at the screen or not. The aim was also to use a built-in algorithm on the Google Cloud Platform and use a basic web application for user interaction. 
The idea behind this project was to detect whether someone was paying attention to their computer. With our current pandemic much of school and business meetings are being conducted online, it is useful to make sure that people are paying attention to their screen.

## 2. Description of the Codebase
The model we used operates through GCP, so the majority of our codebase is Flask related. To elaborate, our codebase contains several important files - **myflask.py**, **index.html**, and **search_results.html**. app.py contains the functions that make the flask app operate, index.html contains the HTML and CSS to create the first page of the flask app, and search_results contains the HTML and CSS to create the second page of the flask app.

app.py contains three crucial functions - search(), upload_file(), and camera(). search() takes the picture that the user either uploads via upload_file() or captures via camera(), converts this image into binary code, and sends this code to our GCP Attention Detection model. Our model will return the probability that a user is both looking at the screen and looking away from the screen. 

Both upload_file() and camera() call the search() function. upload_file() simply allows the user to upload a file from their local directory, then sends this uploaded image to the search() function. Camera() opens the webcam (if you have one) on your computer, allows you to take a picture if you hit the space bar, and sends this picture to the search() function.

index.html contains the HTML and CSS that structures the "Attention Detection: Image Selection" page of the flask app. This is the first page users will see, and where users will be able to open their camera to take a picture or upload a picture from their computer.

search_results.html contains the HTML and CSS that structures the "Attention Detection: Model Results" page of the flask app. This is the second page users will see after an image is sent to our model. On this page, users will see the probability that the individual in their picture is looking at the screen, and the probability that the individual in their picture is looking away from the screen. 

## 3. How it works
Speaking broadly, our project works like this:

* An image is either uploaded or captured on the "Attention Detection: Image Selection" page of the flask app
* This image is sent to our Attention Detection model on the Google Cloud Platform
* The model's results are displayed on the "Attention Detection: Model Results" page of the flask app.

To give an overview of how to navigate the flask app, the first page users will see (Attention Detection: Image Selection) has three buttons - open camera, choose file, and submit. By clicking open camera, the users webcam will open in a separate window. Users will then click on this window, pose, then hit the space bar to take a picture. This picture will automatically be sent to our model. By clicking on choose file, the users File Explorer will open in a separate window. Users will then select the image they want to upload, and click submit. By clicking submit, the image is sent to the model. 

Once the image has been sent to the model, the flask app will redirect to the Attention Detection: Model Results page. This page displays the image that was sent to the model, and lists the models prediction results. Users will see both the probability of looking at the screen and the probability of looking away from the screen.
