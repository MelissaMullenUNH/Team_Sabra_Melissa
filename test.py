import cv2

camera = cv2.VideoCapture(0)

cv2.namedWindow("Model Camera")

counter = 0

while True:
    ret, frame = camera.read()
    if not ret:
        print("Failed to launch camera")
        break
    cv2.imshow("Model Camera", frame)

    key = cv2.waitKey(1)
    if key%256 == 27:
        # ESC pressed
        print("Escape hit, closing camera")
        break

    elif key%256 == 32:
        # SPACE pressed
        image = "static/model_image.png"  
        cv2.imwrite(image, frame)
        print("{} written!".format(image))
        counter = 1

    elif counter == 1:
        print("Image captured, closing camera")
        break

camera.release()