import cairo
import math

add = lambda point1, point2: tuple(point1[i] + point2[i] for i in range(len(point1)))

scale = lambda point, scalar: tuple(scalar*i for i in point)

norm2 = lambda vec: math.sqrt(sum([i**2 for i in vec]))

coords = lambda ORIGIN,i,j,x,y: (add(ORIGIN,scale(i,x))[0], add(ORIGIN,scale(j,y))[1])

class Error(Exception):
    pass

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def __mul__(self, scalar):
        if (isinstance(scalar, float)):
            return Point(self.x * scalar, self.y * scalar)
        elif (isinstance(scalar, int)):
            return Point(self.x * scalar, self.y * scalar)

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __truediv__(self, scalar):
        if (isinstance(scalar, float) or isinstance(scalar,int)):
            return Point(self.x / scalar, self.y / scalar)

    def mod(self):
        return math.sqrt(self.x**2 + self.y**2)

    def norm(self):
        return self / self.mod()

class Transform():
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __mul__(self, point):
        if (isinstance(point, Point)):
            return Point(point.x * self.i.x + point.y * self.j.x,
                    point.x*self.i.y + point.y*self.j.y)

rot90 = Transform(Point(0, 1), Point(-1, 0))

class Context():
    def __init__(self, cr, w, h):
        self.cr = cr
        self.w = w
        self.h = h

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

    def isOutOfView(self, point):
        if (point.x < 0 or point.x > self.w):
            return True
        elif (point.y <0 or point.y > self.h):
            return True

        return False

    def isOutOfViewY(self, point):
        if (point.y < 0 or point.y > self.h):
            return True

        return False

    def isOutOfViewX(self, point):
        if (point.x < 0 or point.x > self.w):
            return True

        return False

    def intersectBoundary(self, m, point):
        # Check left and right boundary
        x1 = point.x
        y1 = point.y

        f = lambda x: m*(x-x1) + y1

        if (not self.isOutOfView(Point(0, f(0)))
                or
                not self.isOutOfView(Point(self.w, f(self.w)))):
            return True
        
        if (m != 0):
            f = lambda y: (y-y1)/m + x1
    
            if (not self.isOutOfView(Point(0, f(0)))
                    or
                    not self.isOutOfView(Point(self.h, f(self.h)))):
                
                return True

        return False


class CoordinateGrid():

    def __init__(self, cr, w, h, ORIGIN, i, j, xunit=1, yunit=1):
        self.cr = cr
        self.cf = Context(cr, w, h)
        self.width = w
        self.height = h
        self.ORIGIN = ORIGIN
        self.xunit = xunit
        self.yunit = yunit
        self.i = i
        self.j = j

        self.ymax = 0
        while (not self.cf.isOutOfView(self.ORIGIN + self.j*self.ymax)):
            self.ymax += 1
         
        self.ylow = 0
        while (not self.cf.isOutOfView(self.ORIGIN + self.j*self.ylow)):
            self.ylow -= 1

        self.xmax = 0
        while (not self.cf.isOutOfView(self.ORIGIN + self.i*self.xmax)):
            self.xmax += 1
         
        self.xlow = 0
        while (not self.cf.isOutOfView(self.ORIGIN + self.i*self.xlow)):
            self.xlow -= 1


    def DrawAxes(self):
        # Generate Y axis
        p = self.ORIGIN + self.j*self.ymax
        self.cr.move_to(p.x, p.y)
        p = self.ORIGIN + self.j*self.ylow
        self.cr.line_to(p.x, p.y)
        
        # Generate X axis
        p = self.ORIGIN + self.i*self.xmax
        self.cr.move_to(p.x, p.y)
        p = self.ORIGIN + self.i*self.xlow
        self.cr.line_to(p.x, p.y)

        self.cr.stroke()

    def DrawGridMarks(self, r):
        if (r < 0 or r > 1):
            raise ValueError("r must be between 0 and 1")

        # Generate Y axis Grid Marks
        for a in range(self.ylow, self.ymax):
            p = self.ORIGIN + self.j*a + self.i*r
            self.cr.move_to(p.x, p.y)
            p = self.ORIGIN + self.j*a - self.i*r
            self.cr.line_to(p.x, p.y)

        # Generate X axis Grid Marks
        for a in range(self.xlow, self.xmax):
            p = self.ORIGIN + self.i*a + self.j*r
            self.cr.move_to(p.x, p.y)
            p = self.ORIGIN + self.i*a - self.j*r
            self.cr.line_to(p.x, p.y)


        self.cr.stroke()

    def DrawGridLinesY(self):
        # Y Axis GridLines Direction One
        a = 0
        m = self.i.y / self.i.x
        while True:
            # Plotting the lines
            a += 1
            n = 0
            p = self.ORIGIN + self.j*a
            
            n = self.xmax
            while True:
                n += 1
                p1 = p + self.i*n
                if (self.cf.isOutOfView(p1)):
                    break

            n = self.xlow
            while True:
                n -= 1
                p2 = p + self.i*n
                if (self.cf.isOutOfView(p2)):
                    break

            self.cr.move_to(p1.x, p1.y)
            self.cr.line_to(p2.x, p2.y)

            if (not self.cf.intersectBoundary(m, p)):
                break

        a = 0
        while True:
            # Plotting the lines
            a -= 1
            n = 0
            p = self.ORIGIN + self.j*a
            
            n = self.xmax
            while True:
                n += 1
                p1 = p + self.i*n
                if (self.cf.isOutOfView(p1)):
                    break

            n = self.xlow
            while True:
                n -= 1
                p2 = p + self.i*n
                if (self.cf.isOutOfView(p2)):
                    break

            self.cr.move_to(p1.x, p1.y)
            self.cr.line_to(p2.x, p2.y)

            if (not self.cf.intersectBoundary(m, p)):
                break

        self.cr.stroke()

    def Plot(self, point):
        pass 

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
