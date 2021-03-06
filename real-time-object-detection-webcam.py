import numpy as np
import cv2
import time


PathCaffeModel = "MobileNetSSD_deploy.caffemodel"
PathPrototxt= "MobileNetSSD_deploy.prototxt.txt"

CLASSES = ["person,bicycle,car,motorbike,aeroplane,bus,train,truck,boat,traffic light,fire hydrant,stop sign,parking meter,bench,bird,cat,dog,horsem,sheep,cow,elephant,bear,zebra,giraffe,backpack,umbrella,handbag,tie,suitcase"]

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


print("LOADING MODEL...")
net = cv2.dnn.readNetFromCaffe(PathPrototxt, PathCaffeModel)

print("STARTING VIDEO STREAM...")

vs=cv2.VideoCapture('test5.mp4')

time.sleep(2.0)

while True:
    ret, frame = vs.read()
    frame = cv2.resize(frame, (900, 900))
    (h, w) = frame.shape[:2]
    
    blob= cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()
    
    # loop over the detections
    for i in np.arange(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
        confidence = detections[0, 0, i, 2]

		# filter out weak detections by ensuring the `confidence` is
		# greater than the minimum confidence
        if confidence > 0.6:
			# extract the index of the class label from the
			# `detections`, then compute the (x, y)-coordinates of
			# the bounding box for the object
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # draw the prediction on the frame
            label = "{}: {:.2f}%".format(CLASSES[idx],
                confidence * 100)
            cv2.rectangle(frame, (startX, startY), (endX, endY),
                COLORS[idx], 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(frame, label, (startX, y),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

	# show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


# do a bit of cleanup
cv2.destroyAllWindows()
    
    
