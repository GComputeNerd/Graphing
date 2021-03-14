import cairo
import cairofunctions
import math

# Defining Variables
w = 545
h = 390
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
cr = cairo.Context(ims)
cf = cairofunctions.Context(cr, w, h)

ORIGIN = cairofunctions.Point(0,0)
i = cairofunctions.Point(w/22, 0)
j = cairofunctions.Point(0,w/22)

cg = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, i, j) # Defining Coordinate Grid

cr.set_source_rgb(0,0,0) 
cr.paint() # Set background color

cr.set_source_rgba(0,0,1,0.5)
cg.DrawGridLinesX()
cg.DrawGridLinesY()

cr.set_source_rgba(1,1,1, 0.8)
cg.DrawAxes()
cg.DrawGridMarks(0.2)

# Plot a bunch of points
points = [cairofunctions.Point(2*i, 3*i) for i in range(1, 6)]

# Write the coordinates of the points near the point
for point in points:
    cg.Plot(point, r=3)
    cg.Write(f"{point.x,point.y}", point + 0.12*cairofunctions.RIGHT + 0.12*cairofunctions.DOWN, size=17.5)

# Arrows showing the directions
cr.set_source_rgba(1, 0.5, 0.2, 0.8)

cg.arrow(cairofunctions.Point(15,1),
        cairofunctions.Point(19,1), 15)

cr.set_source_rgba(1,1,1,0.8)

cg.Write("'+' X-Axis", cairofunctions.Point(19,1) + 0.1*cairofunctions.RIGHT + 0.1*cairofunctions.UP, size=15.5)

cr.set_source_rgba(1,0.5,0.2,0.8)

cg.arrow(cairofunctions.Point(15,1),
        cairofunctions.Point(15,5), 15)

cr.set_source_rgba(1,1,1,0.8)

cg.Write("'+' Y-Axis", cairofunctions.Point(15,5) + 0.5*cairofunctions.UP, size=15.5)

ims.write_to_png("cairo-coordinates.png")
