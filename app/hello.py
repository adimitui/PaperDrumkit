import flask
from flask import redirect
import numpy as np
import main
import audio

app = flask.Flask(__name__)
letters = np.array(['A', 'B', 'C', 'D', 'E', 'F'])
sound = audio.Audio(letters)

@app.route('/')
def index():
	return flask.render_template('index.html')

@app.route('/start')
def start():
	main.index()
	return redirect('http://localhost:5000/')

@app.route('/upload/a')
def upload_a():
	sound.setAudio(0)
	return redirect('http://localhost:5000/')

@app.route('/upload/b')
def upload_b():
	sound.setAudio(1)
	return redirect('http://localhost:5000/')

@app.route('/upload/c')
def upload_c():
	sound.setAudio(2)
	return redirect('http://localhost:5000/')

@app.route('/upload/d')
def upload_d():
	sound.setAudio(3)
	return redirect('http://localhost:5000/')

@app.route('/upload/e')
def upload_e():
	sound.setAudio(4)
	return redirect('http://localhost:5000/')

@app.route('/upload/f')
def upload_f():
	sound.setAudio(5)
	return redirect('http://localhost:5000/') 

@app.route('/preview/a')
def preview_a():
	sound.play_sound('A')
	return redirect('http://localhost:5000/')

@app.route('/preview/b')
def preview_b():
	sound.play_sound('B')
	return redirect('http://localhost:5000/')

@app.route('/preview/c')
def preview_c():
	sound.play_sound('C')
	return redirect('http://localhost:5000/')

@app.route('/preview/d')
def preview_d():
	sound.play_sound('D')
	return redirect('http://localhost:5000/')

@app.route('/preview/e')
def preview_e():
	sound.play_sound('E')
	return redirect('http://localhost:5000/')

@app.route('/preview/f')
def preview_f():
	sound.play_sound('F')
	return redirect('http://localhost:5000/')

if __name__ == '__main__':
	app.run()