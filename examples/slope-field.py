import cairo
import graphing.cairofunctions as cairofunctions
import math

w = 545
h = 390
ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
cr = cairo.Context(ims)
cf = cairofunctions.Context(cr, w, h)
cr.set_antialias(cairo.ANTIALIAS_SUBPIXEL)

# Initial Vectors
ORIGIN = cairofunctions.Point(w/2, h/2)
i = cairofunctions.Point(w/22,0)
j = cairofunctions.Point(0,-w/22)

cg = cairofunctions.CoordinateGrid(cr, w, h, ORIGIN, i, j)
ct = cairofunctions.Transform(i,j, ORIGIN=ORIGIN)

# Paint Screen Black
cr.set_source_rgb(255,255,255)
cr.paint()

cr.set_source_rgba(0.5,0.5,0.5,0.5)
cg.DrawGridLinesX()
cg.DrawGridLinesY()

cr.set_source_rgb(0.2,0.2,0.2)
cg.DrawAxes()
cg.DrawGridMarks(0.2)

# Generate Slope Field.
cr.set_source_rgb(0,0,1)

for y in range(-7, 8):
    for x in range(-11,12):
        try:
            m = -x/y
            cg.PlotFuncYLim(lambda a:m*(a-x) + y, x-0.25, x+0.25, y-0.25, y+0.25)
        except ZeroDivisionError:
            p1 = ct*cairofunctions.Point(x, y -0.25)
            p2 = ct*cairofunctions.Point(x, y+0.25)
            cr.move_to(p1.x, p1.y)
            cr.line_to(p2.x,p2.y)
            cr.stroke()

# Plot some functions
cr.set_line_width(0.8)
cr.set_source_rgb(1,0.2,0.2)
cg.PlotParametric(lambda x: 5*math.cos(x),
        lambda y: 5*math.sin(y),
        0, 2*math.pi)

cr.set_source_rgb(0.2,0.7,0.2)
cg.PlotParametric(lambda x: 3*math.cos(x),
        lambda y: 3*math.sin(y),
        0, 2*math.pi)

cr.set_source_rgb(0.2,0.2,0.6)
cg.PlotParametric(lambda x: 7*math.cos(x),
        lambda y: 7*math.sin(y),
        0, 2*math.pi)


# Box at the Corner
p1 = ct*cairofunctions.Point(5,8)
p2 = ct*cairofunctions.Point(11,8)
p3 = ct*cairofunctions.Point(11,4)
p4 = ct*cairofunctions.Point(5,4)

cr.set_line_width(1)
cf.Polygon(p1,p2,p3,p4)
cr.set_source_rgba(1,1,1,1)
cr.fill_preserve()
cr.set_source_rgb(0,0,0)
cr.stroke()

# Render The LaTeX
eqn = r"\Large$\dfrac{dy}{dx} = \dfrac{-x}{y}$"
p1 = ct*cairofunctions.Point(6.5,6.5)
cg.WriteMath(eqn, p1)

# Write Text
cg.Write("Slope Field for", cairofunctions.Point(5.6, 7), size=17.5)
cr.set_source_rgb(0,0,0)
cr.fill()

# Output End File
ims.write_to_png("img.png")
