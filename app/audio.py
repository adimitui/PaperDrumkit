from playsound import playsound
import numpy as np
import Tkinter, tkFileDialog
import os

class Audio:
	def __init__(self, letters):
		self.letters = letters
		self.sounds = np.array(['static/sounds/CYCdh_ElecK01-ClHat01.wav', 'static/sounds/CYCdh_ElecK01-Cymbal.wav', 'static/sounds/CYCdh_ElecK01-Kick01.wav', 'static/sounds/CYCdh_ElecK01-OpHat01.wav', 'static/sounds/CYCdh_ElecK01-Snr01.wav', 'static/sounds/CYCdh_ElecK01-Tom01.wav'])
		self.melody = list()

	# Play the sound corresponding to the given letter
	def play_sound(self, label):
		# Open the relevant file directory
		if label == 'A':
			self.melody.append(self.sounds[0])
			playsound(self.sounds[0])
		elif label == 'B':
			self.melody.append(self.sounds[1])
			playsound(self.sounds[1])
		elif label == 'C':
			self.melody.append(self.sounds[2])
			playsound(self.sounds[2])
		elif label == 'D':
			self.melody.append(self.sounds[3])
			playsound(self.sounds[3])
		elif label == 'E':
			self.melody.append(self.sounds[4])
			playsound(self.sounds[4])
		elif label == 'F':
			self.melody.append(self.sounds[5])
			playsound(self.sounds[5])
		print self.melody

	# Play the recorded melody
	def play_melody(self):
		for note in self.melody:
			playsound(note)
		del self.melody[:]

	# Update one of the sounds
	def setAudio(self, index):
		# Open the file explorer
		root = Tkinter.Tk()
		root.withdraw()
		file_path = tkFileDialog.askopenfilename()
		file_directory, file_name = os.path.split(file_path)
		file_path = 'static/sounds/' + file_name
		print file_path

		# Save the sound to the array
		self.sounds[index] = file_path