import cairo
import cairofunctions
import math

w = 1080
h = 720
ORIGIN = cairofunctions.Point(w/2, h/2)
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
cg.DrawGridMarks(0.2)

cg1 = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, cairofunctions.Point(w/22,0), j)
cr.set_source_rgb(255,0,0)
cg1.DrawAxes()
cg1.DrawGridMarks(0.2)

cg2 = cairofunctions.CoordinateGrid(cr, w, h, cairofunctions.Point(100,600), cairofunctions.Point(w/22,0), j)
cr.set_source_rgb(0,0,255)
cg2.DrawAxes()
cg2.DrawGridMarks(0.2)


ims.write_to_png("img.png")
