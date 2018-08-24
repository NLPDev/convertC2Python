import numpy as np
import cv2
import point
import random

class DrawWindow():
  img = np.zeros((512, 512, 3), np.uint8)
  width=512
  height=512
  border=1
  window_name='image'

  def setCanvasColor(self, r, g, b):
    self.canvas_color=(b, g, r)

  def clearWindow_init(self):
    self.img = np.zeros((self.height, self.width, 3), np.uint8)
    self.img[np.where((self.img == [0, 0, 0]).all(axis=2))] = self.canvas_color


  def clearWindow(self, r, g, b):
    DrawWindow.setCanvasColor(r, g, b)
    DrawWindow.clearWindow_init()

  def copy_w(self, w):
    self.grid=w.grid

  def setLineType(self, type):
    if type=="solid":
      self.line_type=8

  def setLineThickness(self, thickness):
    self.pen_thickness=thickness

  def setPenColor(self, r, g, b):
    self.pen_color=[g,b,r]

  def setPenColorRandom(self):
    self.setPenColor(int(random.uniform(100, 200)), int(random.uniform(100, 200)), int(random.uniform(100, 200)))
    print ("Setting pen to %i %i %i" % self.pen_color)

  def drawLine(self, pt1, pt2):
    pt1[0]+=self.border
    pt1[1]+=self.border
    pt2[0]+=self.border
    pt2[1]+=self.border
    cv2.line(self.img, pt1, pt2, self.pen_color, self.pen_thickness, self.line_type)

  def drawRectangle(self, pt1, pt2, fill):
    thickness=self.pen_thickness
    if fill>0:
      thickness=-1
    pt1[0]+=self.border
    pt1[1]+=self.border
    pt2[0]+=self.border
    pt2[1]+=self.border
    cv2.rectangle(self.img, pt1, pt2, self.pen_color, thickness)

  def drawCircle(self, pt, r, fill):
    pt[0]+=self.border
    pt[1]+=self.border
    thickness=self.pen_thickness
    if fill>0:
      thickness=-1
    cv2.circle(self.img, pt, r, self.pen_color, thickness, self.line_type)

  def drawEllipse(self, pt, axes, angle, fill):
    thickness=self.pen_thickness
    if fill> 0:
      thickness=-1

    pt[0]+=self.border
    pt[1]+=self.border

    cv2.ellipse(self.img, pt, axes, angle, 0., 360.0, self.pen_color, thickness, self.line_type)

  def drawText(self, pt, text):
    pt[0]+=self.border
    pt[1]+=self.border
    cv2.putText(self.img, text, pt, cv2.FONT_HERSHEY_DUPLEX, 0.3, self.pen_color, 1)

  def startPolyPoints(self):
    self.poly_points=np.array([[-1, -1]])

  def addPolyPoint(self, x, y):
    self.poly_points=np.append(self.poly_points, [[x, y]], 0)


  def drawPolyPoints(self):
    if self.poly_points[0][0]==-1:
      self.poly_points=np.delete(self.poly_points, 0, 0)

    cv2.fillPoly(self.img, np.int32([self.poly_points+self.border]), self.pen_color, self.line_type)

  def drawPixel(self, pt):
    cv2.circle(self.img, (pt[0]+self.border, pt[1]+self.border), 1, self.pen_color, 1)

  def getPixel(self, pt):
    pt[0]+=self.border
    pt[1]+=self.border
    ww, hh, cc=self.img.shape
    if pt[0]>=0 and pt[1]>=0 and pt[0]<ww and pt[1]<hh:
      return pt
    else:
      return [0, 0]

  def blur(self, size):
    cv2.blur(self.img , (size, size))

  def speckle(self, fraction):
    ww, hh, cc=self.img.shape
    n=fraction * ww * hh
    for i in range(n):
      self.setPenColor(0, int(random.uniform(0, 255)), int(random.uniform(0, 255)))
      self.drawPixel(int(random.uniform(0, ww)), int(random.uniform(0, hh)))

  def moveWindow(self, x, y):
    cv2.moveWindow(self.img, x, y)
    self.winx=x
    self.winy=y

  def moveWindowDelta(self, dx, dy):
    self.winx += dx
    self.winy += dy
    cv2.moveWindow(self.img, self.winx, self.winy)

  def hideWindow(self):
    cv2.moveWindow(self.img, 5000, 5000)

  def showWindow(self):
    cv2.moveWindow(self.img, self.winx, self.winy)

  def popWindow(self):
    cv2.namedWindow(self.window_name, cv2.WINDOW_AUTOSIZE)
    self.window_created = 1

  def show(self):
    if self.window_created==0:
      self.popWindow()
    cv2.imshow(self.window_name, self.img)

  def setMat(self, image):
    self.width, self.height, cc=image.shape

  def drawBorder(self, indent, set_thickness):
    orig_thickness = self.pen_thickness
    self.setLineThickness(set_thickness)
    if indent>self.border:
      indent=self.border
    self.drawRectangle((-indent, -indent), (self.width+indent, self.height+indent), 0)

  def setup(self, w, h, name, hide_window, blackwhite):
    self.width=w
    self.height=h
    self.window_name=name
    self.window_created=0

    if hide_window==0:
      self.popWindow()

    self.winx=0
    self.winy=0


    self.img=np.zeros([w, h, 3], (255, 255, 0))

    self.setLineType("solid")
    self.setLineThickness(2)
    self.setCanvasColor(255, 255, 255)
    self.clearWindow_init()

  def __init__(self, w, h, border_width, name, hide_window, blackwhite):
    self.border=border_width
    self.setup(w+2*border_width, h+2*border_width, name, hide_window, blackwhite)
    self.width=w
    self.height=h









































