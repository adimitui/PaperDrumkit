import numpy as np

class Paper_Buffer:
	def __init__(self, size):
		self.size = size
		self.array = [(10000, 10000)] * size
		self.head = 0

	def enqueue(self, item):
		self.array[self.head] = item
		self.head += 1
		if self.head == self.size:
			self.head = 0

	def clear(self):
		self.array = [(-10000, -10000)] * self.size
		self.head = 0

	def display(self):
		print list(np.roll(self.array, -self.head, axis = 0))