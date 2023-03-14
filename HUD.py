import glfw
from OpenGL.GL import *

SetFromHudId = 104
def HUD_Show(window):
    global  width, height
    width, height = glfw.get_window_size(window)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,width,height,0,-1,1)
    glMatrixMode(GL_MODELVIEW)
    glColor3f(1, 1, 0)
    HUDframe = HUDitem((width-500)/2,height-60,504,60)
    HUDframe.draw()

    glColor3f(0, 1, 1)
    HUDTiles = np.zeros((9),dtype=HUDitem)
    for i in range(9):
        HUDTiles[i] = HUDitem(((width-500)/2)+10+i*(500/9),height-50,40,40)
        HUDTiles[i].draw()


class HUDitem:
    def __init__(self,Cx,Cy,Sx,Sy):
        self.coord_x = Cx
        self.coord_y = Cy

        self.size_x = Sx
        self.size_y = Sy
    def draw(self):

        glPushMatrix()
        glBegin(GL_QUADS)

        glVertex2f(self.coord_x, self.coord_y + self.size_y)
        glVertex2f(self.coord_x + self.size_x, self.coord_y + self.size_y)
        glVertex2f(self.coord_x + self.size_x, self.coord_y)
        glVertex2f(self.coord_x, self.coord_y)
        glEnd()
        glPopMatrix()


import numpy as np
Invent = np.zeros(36, dtype=int)
for i in range(Invent.shape[0]):
    Invent[i]=-1
def Inventory():
    global Invent
    InventIndex = 0
    SetFromHudId = Invent[InventIndex]

