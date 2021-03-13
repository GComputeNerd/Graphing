import cairo
import cairofunctions
import math

# Basic Variables
w = 545 # Width
h = 390 # Height
ORIGIN = cairofunctions.Point(w/2, h/2) # Coordinates of Origin
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h) # Image Surface
cr = cairo.Context(ims) # Cairo Context
cf = cairofunctions.Context(cr, w, h) # CairoFunctions Context


i = cairofunctions.Point(w/22, 0) # X Axis Unit Vector
j = cairofunctions.Point(0, -w/22) # Y Axis Unit Vector

cr.set_source_rgb(0,0,0) # Set Color to black
cr.paint() # Paint Full Screen Black

cg1 = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, i, j) # Define a Coordinate Grid

cr.set_source_rgba(0,0,1,0.5) # Set Color to Blue, with opacity 0.5
cg1.DrawGridLinesY() # Draw Y Axis Grid Lines
cg1.DrawGridLinesX() # Draw X Axis Grid Lines
cr.set_source_rgba(1,1,1,0.8) # Set Color to White, with opacity 0.8
cg1.DrawAxes() # Draw Coordinate Axes
cg1.DrawGridMarks(0.2) # Draw Grid Marks

cr.set_source_rgba(1,1,0,0.8) # Set Color to Yellow
cg1.PlotParametric(lambda x: 6/math.cos(x), lambda y: 6*math.tan(y), 0, 7, 1, 0.0025) # Plot Hyperbola

cr.set_source_rgba(1,0,1,0.8) # Set Color to Purple
cg1.PlotParametric(lambda x: 3*math.cos(x), lambda y: 3*math.sin(y), 0, 7) # Plot Circle

cr.set_source_rgba(0,1,1,0.8) # Set Color to Blueish Green
cg1.PlotParametric(lambda x: 4*math.cos(x), lambda y: 5*math.sin(y),0,7) # Plot Ellipse

cr.set_source_rgba(1,0.5,0.2,0.8) # Set Color to Orangish
cg1.PlotParametric(lambda x: x, lambda y: 0.24*y*y -6, -20, 20) # Plot Parabola

ims.write_to_png("conics.png") # Save image to file
