from svgpathtools import svg2paths,Path
import colorsys
import numpy
import sys
import tty
import termios
import argparse






ALPHA_MODE_CLS = "\x1b\x0c"
GRAPHICS_MODE = "\x1d"
ALPHAMODE = "\x1f"
CLEAR_SCREEN = "\x1b\x0c"

##samples_per_seg = 32
#bezier_mesh_size = .25
#decimation_size = 20
#scalefactor = 1.0 #sccaling to keep points smaller then 1024..
TERM_MAX_X_RESOLUTION = 1024
TERM_MAX_Y_RESOLUTION = 768
RED   = 1
GREEN = 2
BLUE  = 4


def build_path(bezier_mesh_size):
	mypaths = []
	a =0
	xxmin = 0
	xxmax = 0
	yymin = 0
	yymax = 0

	for pidx in range(len(pathlist)):
		path = pathlist[pidx]
		xmin, xmax, ymin, ymax =path.bbox()
		if xmin < xxmin:
			xxmin = xmin
		if xmax > xxmax:
			xxmax = xmax
		if ymin < yymin:
			yymin = ymin
		if ymax > yymax:
			yymax = ymax

		attrib = attributes[pidx]
		myPath = []
		for p in path:
			if p.length():
				for i in numpy.arange(0,1.0, 1.0/(p.length()/bezier_mesh_size)):
					dx1, dy1 =  p.point(i).real, p.point(i).imag
					myPath.append((dx1,dy1))

		c1 =  colorsys.rgb_to_hls(0,0,0)
		c2 =  colorsys.rgb_to_hls(255,255,255)
		
		if "fill" in attrib:
			if attrib["fill"] != "none":
				(r,g,b) = tuple(int(attrib["fill"][i:i+2], 16) for i in (1, 2, 4))
				c1 = colorsys.rgb_to_hls(r,g,b)
		if "stroke" in attrib:
			if attrib["stroke"] != "none":
				(r,g,b) = tuple(int(attrib["stroke"][i:i+2], 16) for i in (1, 2, 4))
				c2 = colorsys.rgb_to_hls(r,g,b)
		mypaths.append((c1,c2,myPath)) #fixme color
	#
	return ((xxmin,xxmax,yymin,yymax),mypaths)
	
	
	
def color(c):
	print("\x1b[1;3%dm" % c,end='')

def scaled_coord(x,y,scale=1.0):
	x *= scale
	y *= scale
	y = TERM_MAX_Y_RESOLUTION - y
	print(chr(int((y / 32) + 32)), end='');       # high y
	print(chr(int((y % 32) + 96)), end='');       # low y
	print(chr(int((x / 32) + 32)), end='');       # high x
	print(chr(int((x % 32) + 64)), end='');       # low x

def build_tek_path(mypaths):
	oc1 = oc2 = 0
	outpaths = []
	for c1,c2,p  in mypaths:
		plist = []
		for vecpoint in p:
			plist += [vecpoint[0],vecpoint[1]]

		outpaths.append((c1,c2,plist))
	return outpaths
	
def display_tek_paths(path,scale,decimate_size):
	for c1,c2,p  in mypaths:
		print(GRAPHICS_MODE,end='')
		for vecpoint in p[::decimate_size]:
			scaled_coord(vecpoint[0],vecpoint[1],scale)


#print((xxmin,xxmax,yymin,yymax))
if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("file", type=str,help="svg file")
	parser.add_argument("-a", "--auto", type=bool,help="automatically scale image to fit the screen",default=False)
	parser.add_argument("-c", "--clear", type=bool,help="clear the screen before drawing",default=False)
	parser.add_argument("-b", "--beziermesh", type=float,help="resolution of the mesh to apply to bezier curves (smooth round shapes)", default=.25)
	parser.add_argument("-d", "--decimate", type=int,help="decimate the final vector list to reduce its complexity for faster display (and low poly render)", default=1)
	parser.add_argument("-P", "--pause", type=bool,help="wait for <enter> before  exiting",default=False)
	args = parser.parse_args()


	if args.clear:
		print(CLEAR_SCREEN)

	pathlist, attributes = svg2paths(args.file)
		
	((xxmin,xxmax,yymin,yymax),mypaths) = build_path(args.beziermesh)

	if args.auto:
		if xxmax < TERM_MAX_X_RESOLUTION and yymax < TERM_MAX_Y_RESOLUTION:
			xscale = (TERM_MAX_X_RESOLUTION / xxmax)
			yscale = (TERM_MAX_Y_RESOLUTION / yymax)
			
			if xscale<yscale:
				scalefactor = xscale
			else:
				scalefactor = yscale
		else:
			xscale = (xxmax/TERM_MAX_X_RESOLUTION)
			yscale = (yymax/TERM_MAX_Y_RESOLUTION)
			if xscale>yscale:
				scalefactor = xscale
			else:
				scalefactor = yscale
	else:
		scalefactor = 1.0

	tekpath = build_tek_path(mypaths)

	display_tek_paths(tekpath,scalefactor, args.decimate)
	
	if args.pause:
		input()


	#file_desc = sys.stdin.fileno()
	#old_setting = termios.tcgetattr(file_desc)
	#tty.setraw(sys.stdin)
	#
	#for i in range(5):
	#   char = sys.stdin.read(1)
	#   print("Char: " + str(char))
	#termios.tcsetattr(file_desc, termios.TCSADRAIN, old_setting)
	#
