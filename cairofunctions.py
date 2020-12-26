import cairo
import math

add = lambda point1, point2: tuple(point1[i] + point2[i] for i in range(len(point1)))

scale = lambda point, scalar: tuple(scalar*i for i in point)

norm2 = lambda vec: math.sqrt(sum([i**2 for i in vec]))

coords = lambda ORIGIN,i,j,x,y: (add(ORIGIN,scale(i,x))[0], add(ORIGIN,scale(j,y))[1])

def plot_func(cr, f, ORIGIN ,i,j, xlow, xmax):
    for n in range((xmax-xlow)*100):
        m1 = xlow + n*0.01
        y1 = eval(f, {"x":m1})
        m2 = m1 + 0.01
        y2 = eval(f, {"x":m2})
        cr.move_to(*coords(ORIGIN,i,j,m1,y1))
        cr.line_to(*coords(ORIGIN,i,j,m2,y2))
        cr.stroke()

def arrow_to(cr, x, y, arrow_height, arrow_angle):
    #Draws an arrow from curret point to (x,y)

    cx, cy = cr.get_current_point() # Gets Current Point
    cr.line_to(x,y)
    cr.stroke() # Draw Regular Line

    l = math.sqrt((x-cx)**2 + (y-cy)**2) # Length of line

    # Coordinates of point on line `arrow_height` away from end
    x1 = (arrow_height*cx + (l-arrow_height)*x)/l
    y1 = (-arrow_height*cy - (l-arrow_height)*y)/l

    # Draw 2 lines from (x,y) to points rotating (x1,y1) by `arrow_angle` and `-arrow_angle` about the point (x,y)
    cr.move_to(x,y)
    cr.line_to(((x1-x)*math.cos(arrow_angle) - (y1+y)*math.sin(arrow_angle) +x),-((x1-x)*math.sin(arrow_angle) + (y1+y)*math.cos(arrow_angle) -y))

    cr.move_to(x,y)
    arrow_angle = -arrow_angle

    cr.line_to(((x1-x)*math.cos(arrow_angle) - (y1+y)*math.sin(arrow_angle) +x),-((x1-x)*math.sin(arrow_angle) + (y1+y)*math.cos(arrow_angle) -y))

    cr.stroke() # Draw Arrowhead

def double_arrow_to(cr, x, y, arrow_height, arrow_angle):
    # Draws a double arrow between 2 points

    cx, cy = cr.get_current_point()
    arrow_to(cr, x,y,arrow_height, arrow_angle)
    cr.move_to(x,y)
    arrow_to(cr, cx,cy,arrow_height, arrow_angle)
    cr.move_to(x,y)

def Point(cr,x,y,r=5):
    # Draws a point at (x,y)

    cr.arc(x,y, r, 0, 2*math.pi)
    cr.fill()
