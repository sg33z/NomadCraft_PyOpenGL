import glfw
from OpenGL.GL import *
import pyrr
import glad
import numpy as np


# Зародыши Отрисовки
MAP = np.zeros((11,11,11),dtype=bool)
ID = np.zeros((11,11,11),dtype=int)
vision = [0,0,0]
def DrawBlock(x, y, z, side):
    size = 0.5
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size,size,size)


    # Отрисовка блока
    glBegin(GL_QUADS)
    # Перед
    if side[0]:
        glColor3f(0.0, 1, 0.0)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
    # Зад
    if side[1]:
        glColor3f(1, 0.0, 0.0)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
    # Верх
    if side[2]:
        glColor3f(0.0, 0.0, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)
    # Низ
    if side[3]:
        glColor3f(1, 1, 0.0)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
    # право
    if side[4]:
        glColor3f(1, 0.0, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
    # Лево
    if side[5]:
        glColor3f(0.0, 1, 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
    glEnd()

    glPopMatrix()

def DrawBlockR(x, y, z, side):
    size = 0.5
    glColor3f(0.6, 0.6, 0.6)
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    # Отрисовка блока
    glBegin(GL_QUADS)
    # Перед
    if side[0]:
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
    # Зад
    if side[1]:
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
    # Верх
    if side[2]:
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)
    # Низ
    if side[3]:
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
    # право
    if side[4]:
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
    # Лево
    if side[5]:
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
    glEnd()

    glPopMatrix()


def BlockStart():
    global MAP,ID
    for x in range(10):
        for y in range(10):
            for z in range(10):
                MAP[x, y, z] = False
                ID[x, y, z] = -1
    for x in range(10):
        for z in range(10):
            MAP[x, z, 0] = True
            ID[x, z, 0] = 0
    for x in range(10):
        for z in range(10):
            MAP[x, 0, z] = True
            ID[x, 0, z] = 0
    MAP[1, 1, 0] = True
    ID[1, 1, 0] = 2

def DrawMAP():
    from Controls import get_object_coordinates
    for x in range(10):
        for y in range(10):
            for z in range(10):
                    if MAP[x,y,z]==True:
                        if ID[x,y,z]==0:
                            DrawBlock(x,y,z,OPT(x, y, z))
                        elif ID[x,y,z]==2:
                            DrawBlockR(x, y, z, OPT(x, y, z))

    bPos = get_object_coordinates(MAP,True)

    if bPos is not None:
        x, y, z = bPos
        print(bPos)
        x, y, z = np.floor(x), np.floor(y), np.floor(z)
        DrawBlockR(x, y, z, [True,True,True,True,True,True])





# Низшая оптимизация
def OPT(x,y,z):
    side = [True,True,True,True,True,True]
    if MAP[x,y+1,z]==True:
        side[2]=False
    if MAP[x, y-1, z] == True:
        side[3]=False
    if MAP[x, y, z+1] == True:
        side[0]=False
    if MAP[x, y, z-1] == True:
        side[1]=False
    if MAP[x+1, y, z] == True:
        side[4]=False
    if MAP[x-1, y, z] == True:
        side[5]=False
    return side

