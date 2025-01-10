import numpy as np
import colorsys
import math

def rainbow(t, l, dtype=float):
	def f(c):
		if dtype in (int,np.int16,np.int32):
			return dtype(255*c)
		elif dtype in (float,np.float32,np.float64):
			return dtype(c)
		else:
			raise TypeError("Unsupported type: {dtype.__name__}")
	def red(t):
		return np.sqrt(2/9)*(np.cos(t)+1)
	r,g,b = red(t), red(t+np.pi*2/3), red(t+np.pi*4/3)
	l = 1-2*l
	if l>=0:
		l = 1-l
		return f(l*r), f(l*g), f(l*b)
	l = -l
	return f(l+(1-l)*r), f(l+(1-l)*g), f(l+(1-l)*b)

def rainbow_convert(t, l, dtype=float, fn=colorsys.rgb_to_hls):
	r,g,b = rainbow(t, l, float)
	x,y,z = fn(r,g,b)
	if dtype in (int, np.int16, np.int32):
		return dtype(255*x),dtype(255*y),dtype(255*z)
	if dtype in (float, np.float32, np.float64):
		return dtype(x),dtype(y),dtype(z)
	raise TypeError("Unsupported type: {dtype.__name__}")

def octaves(f, dtype=float):
	return dtype(math.log(f/27.5)/math.log(2))

def note_color(f, l=0.5, dtype=float):
	return rainbow(octaves(f, dtype) * math.tau, l, dtype)
