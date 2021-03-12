import cairo
import cairofunctions
import math

w = 1080
h = 720
ORIGIN = cairofunctions.Point(w/2 - 10, h/2)
i = cairofunctions.Point(w/22, 10)
j = cairofunctions.Point(10, w/22)

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

cg = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, i, j)
cr.set_source_rgb(0,0,0)
cr.paint()
cr.set_source_rgb(0,0,255)
cg.DrawGridLines()
cr.set_source_rgb(255,255,255)
cg.DrawAxes()
cg.DrawGridMarks(0.2)

ims.write_to_png("img.png")
