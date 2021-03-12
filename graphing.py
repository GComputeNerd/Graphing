import cairo
import cairofunctions
import math

w = 545
h = 390
ORIGIN = cairofunctions.Point(w/2, h/2)
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
cr = cairo.Context(ims)
cf = cairofunctions.Context(cr, w, h)

"""
cr.set_source_rgb(0,0,0)
cr.paint()
cr.set_source_rgb(255,255,255)
cg.DrawAxes()
cg.DrawGridMarks(8)
cg.PlotFunc(lambda x: 3*math.sin(math.pi*x/10), -20, 20)
"""

ORIGIN = cairofunctions.Point(w/2 - 40, h/2)
i = cairofunctions.Point(w/22, 0)
j = cairofunctions.Point(20, -w/22 -20)

cr.set_source_rgb(0,0,0)
cr.paint()

cg1 = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, i, j)
cr.set_source_rgba(0,0,255,0.5)
cg1.DrawGridLinesY()
cg1.DrawGridLinesX()
cr.set_source_rgba(255,255,255,0.8)
cg1.DrawAxes()
cg1.DrawGridMarks(0.2)
#cg1.Plot(cairofunctions.Point(3,3), 3, 'square')
#cg1.Plot(cairofunctions.Point(3,-3), 3)
#cg1.Plot(cairofunctions.Point(6,3),3)

p1 = cg1.coords(2,3)
p2 = cg1.coords(2,-3)
p3 = cg1.coords(-2,-3)
p4 = cg1.coords(-2,3)

#cf.Polygon(p1, p2, p3, p4)
#cr.stroke()

cr.set_source_rgba(0,255,0,0.8)

cg1.PlotFunc(lambda x: math.sin(x), -20, 20)

ims.write_to_png("img.png")
