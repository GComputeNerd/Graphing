import cairo
import cairofunctions
import math

w = 1080
h = 720
ORIGIN = cairofunctions.Point(100, 30)
i = cairofunctions.Point(w/22, 30)
j = cairofunctions.Point(0, w/22)

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
cr.set_source_rgb(255,255,255)
cg.DrawAxes()
cr.move_to(ORIGIN.x, ORIGIN.y)
cr.line_to(i.x, i.y)

ims.write_to_png("img.png")
