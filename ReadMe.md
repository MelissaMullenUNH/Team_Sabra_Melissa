# README for Sabra and Melissa's Group Implementation Project

## Attention Detection
(Because the dataset contain thousands of images it was too big to upload to github. Here is the link to the webpage where it describes the dataset and you can download it: https://www.cs.columbia.edu/CAVE/databases/columbia_gaze/)

## 1. Objective of project
The goal of this project was to create a method of detecting if someone in a picture is looking at the screen or not. The aim was also to use a built-in algorithm on the Google Cloud Platform and use a basic web application for user interaction. 
The idea behind this project was to detect whether someone was paying attention to their computer. With our current pandemic much of school and business meetings are being conducted online, it is useful to make sure that people are paying attention to their screen.

## 2. Description of the Codebase
The model we used operates through GCP, so the majority of our codebase is Flask and html related. To elaborate, our codebase contains several important files - **myflask.py**, **capture.js**, and the templates: **main.css**, **capture.html**, **index.html**, and **search_results.html**. 
myflask.py contains the functions that make the flask app operate, index.html contains the HTML and CSS to create the first page of the flask app, and search_results contains the HTML and CSS to create the second page of the flask app. Capture.js creates the page to open and access your camera locally. The capture.html and main.css support and create the open camera page.

myflask.py takes the picture that the user either uploads or captures, converts this image into binary code, and sends this code to our GCP Attention Detection model. Our model will return the probability that a user is both looking at the screen and looking away from the screen. 

capture.js is a javascript file that bulds the "open camera" page so it can access the users camera locally. It is supported by the capture.html and main.css. It allows the user to take a picture of themselves, selects a photo, and submits it to the model. The results are returned by the search results.html.

index.html contains the HTML and CSS that structures the "Attention Detection: Image Selection" page of the flask app. This is the first page users will see, and where users will be able to open their camera to take a picture or upload a picture from their computer.

search_results.html contains the HTML and CSS that structures the "Attention Detection: Model Results" page of the flask app. This is the second page users will see after an image is sent to our model. On this page, users will see the probability that the individual in their picture is looking at the screen, and the probability that the individual in their picture is looking away from the screen. 

## 3. How it works
Speaking broadly, our project works like this:

* An image is either uploaded or captured on the "Attention Detection: Image Selection" page of the flask app
* This image is sent to our Attention Detection model on the Google Cloud Platform
* The model's results are displayed on the "Attention Detection: Model Results" page of the flask app.

To give an overview of how to navigate the flask app, the first page users will see (Attention Detection: Image Selection) has three buttons - open camera, choose file, and submit. By clicking open camera you are redirected to a new page where you can take a photo, select the photo, and submit it to the model.
By clicking on choose file, the users file explorer/finder will open in a separate window. Users will then select the image they want to upload, and click submit. By clicking submit, the image is sent to the model. 

Once the image has been sent to the model, the flask app will redirect to the Attention Detection: Model Results page. This page displays the image that was sent to the model, and lists the models prediction results. Users will see both the probability of looking at the screen and the probability of looking away from the screen.
