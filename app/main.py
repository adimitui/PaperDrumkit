import numpy as np
import cv2
import canvas as canvas
import paper_buffer
import time

def index():
	# Start the webcam camera
	cap = cv2.VideoCapture(1)

	# Initialize variables
	paper_contour = np.array([])
	bg_thresh = None
	finger_thresh = None
	thresh2 = None
	finger_thresh2 = None
	stable_threshold = 0.01
	farthest = None # Point tracking the fingertip of the user
	current_position = None
	num_frames = 4
	history = paper_buffer.Paper_Buffer(num_frames)
	click_threshold = 8

	while(True):
		# Capture a video frame-by-frame
		ret, frame = cap.read()

		# Find the edges in each frame
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Turn image frame into grayscale version
		blur = cv2.GaussianBlur(gray, (5, 5), 0) # Execute a Gaussian blur to remove noise from the frame
		thresh = cv2.threshold(blur.copy(), 127, 255, cv2.THRESH_BINARY)[1] # Create a binary image
		edges = cv2.Canny(thresh, 50, 200) # Isolate the edges in the picture

		# Find contours in the edged image, keep only the largest ones, and initialize our screen contour
		_, temp_contours, _ = cv2.findContours(edges.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
		contours = sorted(temp_contours, key = cv2.contourArea, reverse = True)[:10]

		# Loop over contours to find which contour belongs to the paper
		count = 0
		for contour in contours:
			# Approximate how many points the perimeter of the contour has
			perimeter = cv2.arcLength(contour, True)
			area = cv2.contourArea(contour)
			approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

			# If the approximated contour has 4 points, we can assume we have found our paper
			if len(approx) == 4 and perimeter > 1000 and area > 2000:
				# Save the paper contour
				paper_contour = approx
				
				# Save the canvas thresholds
				bg_thresh = np.zeros(thresh.shape, dtype = np.uint8)
				finger_thresh = np.zeros(thresh.shape, dtype = np.uint8)

				# Store the canvas information for use in future calculations
				paper_canvas = canvas.Canvas(map(lambda x: x[0], paper_contour))

				# Fill in the paper to filter out the canvas later (when extracting the user's hand)
				cv2.fillConvexPoly(bg_thresh, paper_contour, 255)
				break

		# Draw red circles at the corners of the paper
		for point in paper_contour:
			cv2.circle(frame, (point[0][0], point[0][1]), 5, (0, 0, 255), 3)

		# Draw a green outline around the edges of the paper
		cv2.polylines(frame, [paper_contour], True, (0, 255, 0), 3)

		# Create a mask of the frame to prepare for bitwise operations
		_, mask = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
		mask_inv = cv2.bitwise_not(mask)

		# Check if the threshold and mask are the same size before performing operations
		if np.shape(bg_thresh) == np.shape(mask):
			# Isolate the user's hand in the binary image
			mask_clean = cv2.bitwise_and(mask, bg_thresh)
			bg_thresh_clean = cv2.bitwise_and(bg_thresh, bg_thresh)
			finger_thresh2 = cv2.bitwise_xor(mask_clean, bg_thresh)

			# Get rid of leftover noise at the paper edges
			cv2.polylines(finger_thresh2, [paper_contour], True, (0, 0, 0), 3)

			# Calculate the differential value
			temp = cv2.bitwise_xor(finger_thresh, finger_thresh2, mask = bg_thresh)
			dif_value = np.sum(temp / (np.sum(finger_thresh2) + 0.1))

			# Calculate the lowest point of the finger mask, corresponding to the fingertip
			if dif_value > stable_threshold:
				# Collect the coordinates where the finger threshold is above a certain height
				y_values, x_values = np.where(finger_thresh2 > 0)
				
				# Find the y-value with the highest magnitude, corresponding to the lowest point on the screen
				if len(y_values > 0):
					# Track the current position of the user's fingertip
					index = np.argmax(y_values)
					farthest = (x_values[index], y_values[index])
					current_position = farthest

					# Initialize booleans used to check if a click has occurred
					click_pre = False
					click_down = False
					click_up = False

					time.sleep(0.008)
					for element in np.roll(history.array, history.head, axis = 0):
						distance = canvas.distance_point_point(element, current_position)
						#print distance

						if click_up:
							continue
						if click_down and distance > 10:
							click_up = True
							print '=========================== CLICK ====================='
							paper_canvas.get_button(current_position)
							history.clear()
							click_up = False
							click_down = False
							click_pre = False
						elif click_pre and distance > 5 and distance < 20:
							click_down = True
							print '================ DOWN ==============='
						elif distance < 5:
							click_pre = True

					# Update history queue
					history.enqueue(current_position)

			# Place a blue circle to mark the fingertip
			cv2.circle(frame, farthest, 5, (255, 0, 0), 3)

			# Display the resulting frame
			cv2.imshow('frame', frame)
		else:
			# Display the resulting frame
			cv2.imshow('frame', frame)

		# Display the resulting frame
		if cv2.waitKey(1) & 0xFF == ord('q'):
			paper_canvas.replay()
			break

	# When everything is done, release the capture 
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	index()