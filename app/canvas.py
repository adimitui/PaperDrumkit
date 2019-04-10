import math
import numpy as np
import matplotlib.path as mplPath
import audio

# Return the distance between 2 points
def distance_point_point(point1, point2):
	# Find the change in the coordinates
	d_y = (point2[1] - point1[1])
	d_x = (point2[0] - point1[0])

	# Return the statement
	return math.sqrt((d_y * d_y) + (d_x * d_x))

# Divide a line into thirds given two endpoints
def get_thirds(point1, point2):
	# Initialize fractions
	one_third = 1.0 / 3.0
	two_thirds = 2.0 / 3.0

	# Divide the top line into thirds
	x_temp = (point1[0] + one_third * (point2[0] - point1[0]))
	y_temp = (point1[1] + one_third * (point2[1] - point1[1]))
	third1 = np.array([x_temp, y_temp]) # One-third
	x_temp = (point1[0] + two_thirds * (point2[0] - point1[0]))
	y_temp = (point1[1] + two_thirds * (point2[1] - point1[1]))
	third2 = np.array([x_temp, y_temp]) # Two-thirds

	# Return statement
	return third1, third2

# Upload to the audio class
def upload():
	letters = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
	sound = audio.Audio(letters)
	sound.setAudio()

# Class defining a line
class Line:
	# Create a line from two points
	def __init__(self, point1, point2):
		self.slope = (point2[1] - point1[1]) / (point2[0] - point[0] + 0.1) # Prevent from dividing by zero
		self.points = [point1, point2]

	# Return the distance from a line to a point
	def distance_line_point(self, point):
		point1 = self.points[0]
		point2 = self.points[1]
		temp = ((point1[1] - point2[1]) * point[0]) - ((point1[0] - point2[0]) * point[1]) + (point1[0] * point2[1]) - (point1[1] * point2[0]) / distance_point_point(point1, point2)
		return temp

# Class defining calculation functions
class Canvas:
	labels = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
	sound = audio.Audio(labels)

	# Constructor
	def __init__(self, points):
		# Sort the points
		points = sorted(points, key = lambda p: p[0])
		self.points_full = points

		# Store the points in more memorable variables
		top_left = points[0]
		bottom_left = points[1]
		bottom_right = points[2]
		top_right = points[3]

		# Calculate the midpoints between the top and bottom left points
		x_temp = (top_left[0] + bottom_left[0]) / 2
		y_temp = (top_left[1] + bottom_left[1]) / 2
		mid_left = np.array([x_temp, y_temp])

		# Calculate the midpoints between the top and bottom right points
		x_temp = (top_right[0] + bottom_right[0]) / 2
		y_temp = (top_right[1] + bottom_right[1]) / 2
		mid_right = np.array([x_temp, y_temp])
		
		# Get thirds for each line
		top_third1, top_third2 = get_thirds(top_left, top_right)
		mid_third1, mid_third2 = get_thirds(mid_left, mid_right)
		bottom_third1, bottom_third2 = get_thirds(bottom_left, bottom_right)

		# Save the points into the corresponding buttons
		self.a = np.array([top_left, mid_left, mid_third1, top_third1])
		self.b = np.array([top_third1, mid_third1, mid_third2, top_third2])
		self.c = np.array([top_third2, mid_third2, mid_right, top_right])
		self.d = np.array([mid_left, bottom_left, bottom_third1, mid_third1])
		self.e = np.array([mid_third1, bottom_third1, bottom_third2, mid_third2])
		self.f = np.array([mid_third2, bottom_third2, bottom_right, mid_right])

	# Return the button that the user pressed
	def get_button(self, point):
		# Store all the buttons into an array
		paths = np.array([self.a, self.b, self.c, self.d, self.e, self.f])

		# Check which button the point is contained within
		index = 0
		for path in paths:
			temp_path = mplPath.Path(path)
			if temp_path.contains_point(point):
				break
			else:
				if index < 5:
					index += 1

		# Get the letter that the button corresponds to
		label = self.labels[index]
		self.sound.play_sound(label)

	# Play the recorded melody upon closing
	def replay(self):
		# Play the melody
		self.sound.play_melody()