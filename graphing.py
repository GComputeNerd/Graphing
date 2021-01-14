import cairo
import cairofunctions

ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, 1080, 720)
cr = cairo.Context(ims)
cf = cairofunctions.Context(cr, 1080, 720)

cg = cairofunctions.CoordinateGrid(cr, 1080, 720, (540, 360), 1, 1080/22)

cr.set_source_rgb(0,0,0)
cr.paint()
cr.set_source_rgb(255,255,255)
cg.DrawAxes()
cg.DrawGridMarks(8)
cg.PlotFunc(lambda x: x**5, -10, 20)

ims.write_to_png("img.png")
