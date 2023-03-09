import glfw
from OpenGL.GL import *
import numpy as np
from Draw import DrawBlockR,DrawBlockUn, tex


class DropItem:
    tex= tex[0]
    x,y,z = float(),float(),float()
    model3d = bool(True)
    ID = int(0)
    rot = int()
    def __init__(self, ID, x,y,z):
        self.tex = tex[ID]
        self.ID = ID
        self.x,self.y,self.z = x,y,z
        self.rot = 0
    def update(self):
        self.rot += 1

        self.y = np.sin(self.rot/20)*0.1
        glPushMatrix()
        glTranslatef(self.x, self.y+1, self.z)
        glScalef(0.2,0.2,0.2)
        glRotatef(self.rot, 0, 1, 0)
        DrawBlockR(0, 0, 0,
                   [True, True, True, True, True, True], self.ID)

        glPopMatrix()