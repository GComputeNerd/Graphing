import cairo
import cairofunctions as cf
import math

#w = int(input("Width:"))
#h = int(input("Height:"))

w = 1080
h = 720

ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
cr = cairo.Context(ims)
ORIGIN = (w/2,h/2)

cr.set_source_rgb(0,0,0)
cr.paint()
cr.set_source_rgb(255,255,255)

cr.move_to(0, h/2)
cf.double_arrow_to(cr, w, h/2, 20, math.pi/8)
cr.move_to(w/2, 0)
cf.double_arrow_to(cr,w/2, h, 20, math.pi/8)

u = w/22 # unit
i = (u, 0)
j = (0, -u)
d = 8 # width of grid mark

# X axis Grid Marks
for k in range(math.floor(w/(2*u))):
    p = cf.add(ORIGIN, cf.scale(i,k))
    cr.move_to(*cf.add(p, (0,d)))
    cr.line_to(*cf.add(p,(0,-d)))
    cr.stroke()
    p = cf.add(ORIGIN, cf.scale(i,-k))
    cr.move_to(*cf.add(p, (0,d)))
    cr.line_to(*cf.add(p,(0,-d)))
    cr.stroke()

# Y axis Grid Marks
for k in range(math.ceil(h/(2*u))):
    p = cf.add(ORIGIN, cf.scale(j,k))
    cr.move_to(*cf.add(p, (d,0)))
    cr.line_to(*cf.add(p,(-d,0)))
    cr.stroke()
    p = cf.add(ORIGIN, cf.scale(j,-k))
    cr.move_to(*cf.add(p, (d,0)))
    cr.line_to(*cf.add(p,(-d,0)))
    cr.stroke()

cr.set_source_rgb(255,0,0)
cf.plot_func(cr, "x**2", ORIGIN, i, j, -10, 10)
cr.set_source_rgb(0,255,0)
cf.plot_func(cr, "x", ORIGIN, i, j, -10, 10)
cr.set_source_rgb(0,0,255)
cf.plot_func(cr, "x**3", ORIGIN, i, j, -10, 10)
ims.write_to_png("img.png")
