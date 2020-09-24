# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2
from pylibdmtx import pylibdmtx
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
	help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())

# initialize the video stream and allow the camera sensor to warm up
print("[INFO] starting video stream...")
# vs = VideoStream(src=6).start()
vs = VideoStream(src=0).start() 
# my monocular in realsense
# vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (400,300))
# loop over the frames from the video stream
while True:
	# grab the frame from the threaded video stream and resize it to
	# have a maximum width of 400 pixels
	frame = vs.read()
	frame = imutils.resize(frame, width=400, height=300)
	img_h,img_w,_ = frame.shape 
	# find the barcodes in the frame and decode each of the barcodes
	barcodes = pyzbar.decode(frame);
	dms = pylibdmtx.decode(frame);

	for barcode in barcodes:
        # extract the bounding box location of the barcode and draw
        # the bounding box surrounding the barcode on the image
		(x, y, w, h) = barcode.rect
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
		barcodeData = barcode.data.decode("utf-8")
		barcodeType = barcode.type
		text = "{} ({})".format(barcodeData, barcodeType)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, text, (x, y - 10),
		    font, 0.5, (0, 0, 255), 2)

	for dm in dms:
		(x, y, w, h) = dm.rect
		y = img_h - y
		cv2.rectangle(frame, (x, y), (x + w, y - h), (0, 0, 255), 2)
		dmData = dm.data.decode("utf-8")
		text = "{}".format(dmData)
		font = cv2.FONT_HERSHEY_SIMPLEX
		cv2.putText(frame, text, (x, y - h - 10),
	        font, 0.5, (0, 0, 255), 2)

	out.write(frame)
	# show the output frame
	cv2.namedWindow("Barcode Scanner", cv2.WINDOW_NORMAL)
	cv2.resizeWindow("Barcode Scanner", 800,800)
	cv2.imshow("Barcode Scanner", frame)
	key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

print("[INFO] cleaning up...")
out.release()
vs.stop()
cv2.destroyAllWindows()
