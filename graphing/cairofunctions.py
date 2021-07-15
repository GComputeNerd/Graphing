import cairo
import math
from datetime import datetime
import graphing.writeMathEq as writeMathEq

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

    __rmul__ = __mul__

    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def __truediv__(self, scalar):
        if (isinstance(scalar, float) or isinstance(scalar,int)):
            return Point(self.x / scalar, self.y / scalar)

    def mod(self):
        return math.sqrt(self.x**2 + self.y**2)

    def norm(self):
        return self / self.mod()

UP = Point(0,1)
DOWN = Point(0,-1)
LEFT = Point(-1,0)
RIGHT = Point(1,0)

class Transform():
    def __init__(self, i, j, ORIGIN = Point(0,0)):
        self.i = i
        self.j = j
        self.ORIGIN = ORIGIN

    def __mul__(self, point):
        if (isinstance(point, Point)):
            return Point(point.x * self.i.x + point.y * self.j.x,
                    point.x*self.i.y + point.y*self.j.y) + self.ORIGIN

rot90 = Transform(Point(0, 1), Point(-1, 0))

class Context():
    def __init__(self, cr, w, h):
        self.cr = cr
        self.w = w
        self.h = h

    def arrow(self, point1, point2, arrow_height=20, arrow_angle=math.pi/8):
        #Draws an arrow from current point to (x,y)
        x = point2.x
        y = point2.y
        cx = point1.x
        cy = point1.y

        self.cr.move_to(cx,cy)
    
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

    def double_arrow(self, point1, point2, arrow_height=20, arrow_angle=math.pi/8):
        # Draws a double arrow between 2 points
        x = point2.x
        y = point2.y

        cx = point1.x
        cy = point1.y

        self.arrow(point1, point2,arrow_height, arrow_angle)
        self.arrow(point2, point1,arrow_height, arrow_angle)
        self.cr.move_to(x,y)

    def Polygon(self, *points):
        self.cr.move_to(points[0].x, points[0].y)
        
        for i in range(1, len(points)):
            self.cr.line_to(points[i].x, points[i].y)

        self.cr.close_path()

    def plotPoint(self,point,r=5, shape='circle'):
        # Draws a point at (x,y)

        if (shape == 'circle'):
            self.cr.arc(point.x,point.y, r, 0, 2*math.pi)
        elif (shape == 'square'):
            r = r/math.sqrt(2)
            self.Polygon(
                    Point(point.x +r, point.y +r),
                    Point(point.x +r, point.y -r),
                    Point(point.x -r, point.y -r),
                    Point(point.x -r, point.y +r)
                    )
        self.cr.fill()

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
        # The output is based on binary. DURL
        # D - Down
        # U - Up
        # R - Right
        # L - Left
        # 1 if the line intersects, 0 if it doesnt.
        # Sum is outputted

        x1 = point.x

        y1 = point.y

        f = lambda x: m*(x-x1) + y1

        r = 0

        if (not self.isOutOfView(Point(0, f(0)))):
            r += 1
        if (not self.isOutOfView(Point(self.w, f(self.w)))):
            r += 2
        
        if (m != 0):
            f = lambda y: (y-y1)/m + x1
    
            if (not self.isOutOfView(Point(f(0), 0))):
                r += 4
            if (not self.isOutOfView(Point(f(self.h), self.h))):
                r += 8
        

        return ((True, r) if r > 0 else (False, r))

    def intersectCoords(self, m, point, r):
        r = format(r, 'b') # Get r in binary in string
        r = "0"*(4 - len(r)) + r
        x1 = point.x
        y1 = point.y
        points = []

        f = lambda y: (y-y1)/m + x1
        if (r[0] == '1'):
            points.append(
                    Point(f(self.h), self.h)
                    )
        if (r[1] == '1'):
            points.append(
                    Point(f(0), 0)
                    )

        f = lambda x: m*(x-x1) + y1
        if (r[2] == '1'):
            points.append(
                    Point(self.w, f(self.w))
                    )
        if (r[3] == '1'):
            points.append(
                    Point(0, f(0))
                    )

        return points

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

    coords = lambda self,point : self.ORIGIN + self.i*point.x + self.j*point.y


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
            intersect = self.cf.intersectBoundary(m,p)

            if (not intersect[0]):
                break

            points = self.cf.intersectCoords(m,p,intersect[1])

            self.cr.move_to(points[0].x, points[0].y)
            self.cr.line_to(points[1].x, points[1].y)

        a = 0
        while True:
            # Plotting the lines
            a -= 1
            n = 0
            p = self.ORIGIN + self.j*a
            intersect = self.cf.intersectBoundary(m,p)

            if (not intersect[0]):
                break

            points = self.cf.intersectCoords(m,p,intersect[1])

            self.cr.move_to(points[0].x,points[0].y)
            self.cr.line_to(points[1].x,points[1].y)

        self.cr.stroke()

    def DrawGridLinesX(self):
        # Y Axis GridLines Direction One
        a = 0
        m = (self.j.y / self.j.x if self.j.x != 0 else 'NAN')

        if (m == 'NAN'):
            n = 0
            while True:
                n += 1
                p = self.ORIGIN + self.i*n
                if (self.cf.isOutOfViewX(p)): break
                self.cr.move_to(p.x, 0)
                self.cr.line_to(p.x, self.height)

            self.cr.stroke()

            n = 0
            while True:
                n -= 1
                p = self.ORIGIN + self.i*n
                if (self.cf.isOutOfViewX(p)): break
                self.cr.move_to(p.x, 0)
                self.cr.line_to(p.x, self.height)

            self.cr.stroke()
            return 1


        while True:
            # Plotting the lines
            a += 1
            n = 0
            p = self.ORIGIN + self.i*a
            intersect = self.cf.intersectBoundary(m,p)

            if (not intersect[0]):
                break

            points = self.cf.intersectCoords(m,p,intersect[1])

            self.cr.move_to(points[0].x, points[0].y)
            self.cr.line_to(points[1].x, points[1].y)

        a = 0
        while True:
            # Plotting the lines
            a -= 1
            n = 0
            p = self.ORIGIN + self.i*a
            intersect = self.cf.intersectBoundary(m,p)

            if (not intersect[0]):
                break

            points = self.cf.intersectCoords(m,p,intersect[1])

            self.cr.move_to(points[0].x,points[0].y)
            self.cr.line_to(points[1].x,points[1].y)

        self.cr.stroke()

    def Plot(self, point, r=5, shape='circle'):
        self.cf.plotPoint(self.coords(point), r, shape)

    def PlotFunc(self, f, xlow, xmax, r=1, step=0.005):
        x = xlow
        while (x <= xmax):
            self.Plot(
                    Point(x, f(x)),
                    r,
                    'square'
                    )
            x += step

    def PlotFuncYLim(self, f, xlow, xmax, ylow, ymax, r=1, step=0.005):
        x = xlow
        while (x <= xmax):
            y = f(x)

            if (y > ymax or y < ylow):
                x += step
                continue

            self.Plot(
                    Point(x, y),
                    r,
                    'square'
                    )
            x += step


    def PlotParametric(self, x, y, tmin, tmax, r=1, step=0.005):
        t = tmin
        while (t <= tmax):
            self.Plot(
                    Point(x(t), y(t)),
                    r,
                    'square'
                    )
            t += step

    def Write(self, text, point, font_face="Arial", slant=cairo.FONT_SLANT_NORMAL, weight=cairo.FONT_WEIGHT_NORMAL, size=13):
        # This is a Temporary Write Function.
        # Planning to upgrade this with support for LaTeX.
        # And Using Pango, for now, just using The Standard
        # PyCairo Text Functions.
        point = self.coords(point)

        self.cr.move_to(point.x, point.y)
        self.cr.select_font_face(font_face, slant, weight)
        self.cr.set_font_size(size)
        self.cr.text_path(text)

    def WriteMath(self, eqn, point):
        name = datetime.now().strftime("eqn-%m%d%H%M%S%f")
        writeMathEq.renderMath(eqn, name)
        eqn = cairo.ImageSurface.create_from_png("tex-files/" + name + ".png")
        self.cr.set_source_surface(eqn, point.x, point.y)
        self.cr.get_source().set_filter(cairo.FILTER_NEAREST)
        self.cr.paint()

    def arrow(self, point1, point2, arrow_height=20, arrow_angle=math.pi/8):
        point1 = self.coords(point1)
        point2 = self.coords(point2)
        self.cf.arrow(point1, point2, arrow_height, arrow_angle)


