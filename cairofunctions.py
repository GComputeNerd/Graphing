import cairo
import math

add = lambda point1, point2: tuple(point1[i] + point2[i] for i in range(len(point1)))

scale = lambda point, scalar: tuple(scalar*i for i in point)

norm2 = lambda vec: math.sqrt(sum([i**2 for i in vec]))

coords = lambda ORIGIN,i,j,x,y: (add(ORIGIN,scale(i,x))[0], add(ORIGIN,scale(j,y))[1])

class Error(Exception):
    pass

class Context():
    def __init__(self, cr, w, h):
        self.cr = cr
        self.width = w
        self.height = h

    def arrow_to(self, x, y, arrow_height=20, arrow_angle=math.pi/8):
        #Draws an arrow from curret point to (x,y)
    
        cx, cy = self.cr.get_current_point() # Gets Current Point
        self.cr.line_to(x,y)
        self.cr.stroke() # Draw Regular Line
    
        l = math.sqrt((x-cx)**2 + (y-cy)**2) # Length of line
    
        # Coordinates of point on line `arrow_height` away from end
        x1 = (arrow_height*cx + (l-arrow_height)*x)/l
        y1 = (-arrow_height*cy - (l-arrow_height)*y)/l
    
        # Draw 2 lines from (x,y) to points rotating (x1,y1) by `arrow_angle` and `-arrow_angle` about the point (x,y)
        self.cr.move_to(x,y)
        self.cr.line_to(((x1-x)*math.cos(arrow_angle) - (y1+y)*math.sin(arrow_angle) +x),-((x1-x)*math.sin(arrow_angle) + (y1+y)*math.cos(arrow_angle) -y))
    
        self.cr.move_to(x,y)
        arrow_angle = -arrow_angle
    
        self.cr.line_to(((x1-x)*math.cos(arrow_angle) - (y1+y)*math.sin(arrow_angle) +x),-((x1-x)*math.sin(arrow_angle) + (y1+y)*math.cos(arrow_angle) -y))
    
        self.cr.stroke() # Draw Arrowhead

    def double_arrow_to(self, x, y, arrow_height=20, arrow_angle=math.pi/8):
        # Draws a double arrow between 2 points
    
        cx, cy = self.cr.get_current_point()
        self.arrow_to(x,y,arrow_height, arrow_angle)
        self.cr.move_to(x,y)
        self.arrow_to(cx,cy,arrow_height, arrow_angle)
        self.cr.move_to(x,y)

    def Point(cr,x,y,r=5):
        # Draws a point at (x,y)
    
        cr.arc(x,y, r, 0, 2*math.pi)
        cr.fill()


class CoordinateGrid():

    coords = lambda self,x,y: (add(self.ORIGIN,scale(self.i,x))[0], add(self.ORIGIN,scale(self.j,y))[1])

    def __init__(self, cr, w, h, ORIGIN, unit, vu):
        self.cr = cr
        self.cf = Context(cr, w, h)
        self.width = w
        self.height = h
        self.ORIGIN = ORIGIN
        self.unit = unit
        self.vu = vu
        self.i = (vu, 0)
        self.j = (0, -vu)

    def DrawAxes(self):
        self.cr.move_to(0,self.ORIGIN[1])
        self.cf.double_arrow_to(self.width, self.ORIGIN[1])
        self.cr.move_to(self.ORIGIN[0], 0)
        self.cf.double_arrow_to(self.ORIGIN[0], self.height)

    def DrawGridMarks(self, d):
        for k in range(math.floor(self.width/(2*self.unit))):
            l = add(self.ORIGIN, scale(self.i,k))
            self.cr.move_to(*add(l, (0, d)))
            self.cr.line_to(*add(l, (0, -d)))
            l = add(self.ORIGIN, scale(self.i,-k))
            self.cr.move_to(*add(l, (0, d)))
            self.cr.line_to(*add(l, (0, -d)))
            self.cr.stroke()

        for k in range(math.ceil(self.height/(2*self.unit))):
            l = add(self.ORIGIN, scale(self.j,k))
            self.cr.move_to(*add(l, (d, 0)))
            self.cr.line_to(*add(l, (-d, 0)))
            l = add(self.ORIGIN, scale(self.j,-k))
            self.cr.move_to(*add(l, (d, 0)))
            self.cr.line_to(*add(l, (-d, 0)))
            self.cr.stroke()

    def PlotFunc(self, f, xlow, xmax):
        step = self.unit/100

        for n in range((xmax-xlow)*100):
            m1 = xlow + n*step
            y1 = f(self.unit*m1)
            m2 = m1 + step
            y2 = f(self.unit*m2)
            self.cr.move_to(*scale(self.coords(m1,y1), 1/self.unit))
            self.cr.line_to(*scale(self.coords(m2,y2), 1/self.unit))
            self.cr.stroke()

def plot_func(cr, f, ORIGIN ,i,j, xlow, xmax):
    for n in range((xmax-xlow)*100):
        m1 = xlow + n*0.01
        y1 = eval(f, {"x":m1})
        m2 = m1 + 0.01
        y2 = eval(f, {"x":m2})
        cr.move_to(*coords(ORIGIN,i,j,m1,y1))
        cr.line_to(*coords(ORIGIN,i,j,m2,y2))
        cr.stroke()


def Point(cr,x,y,r=5):
    # Draws a point at (x,y)

    cr.arc(x,y, r, 0, 2*math.pi)
    cr.fill()

def Polygon(cr, *points):
    # Draws polygon passing through points
    # There's probably a better way to do this...Oh Well.
    if (len(points) < 6):
        raise Error("WTF YOU WANTED A POLYGON.... *POLY* GON!!!")
    elif (len(points) %2 == 1):
        raise Error("I NEED A PAIR OF COORDINATES FOR EVERY POINT!!! COME ON DUUDE!!! MY PATIENCE IS GONEEEEE, less existent than your polygon")

    m = len(points) - 2

    for i in range(m):
        if (i%2 == 1 ):
            continue
        cr.move_to(points[i], points[i+1])
        cr.line_to(points[i+2], points[i+3])

    cr.move_to(points[-2], points[-1])
    cr.line_to(points[0], points[1])

    cr.stroke()
