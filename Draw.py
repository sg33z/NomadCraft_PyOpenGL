import glfw
from PIL import Image
from OpenGL.GL import *
import pyrr
import glad
import numpy as np
from objloader import *


# Зародыши Отрисовки
MAP = np.zeros((11,11,11),dtype=bool)
ID = np.zeros((11,11,11),dtype=int)
vision = [0,0,0]
def DrawBlockUn(x, y, z, side):
    size = 0.5

    glPushMatrix()

    glTranslatef(x, y, z)
    glScalef(size,size,size)
    # Отрисовка блока
    glBegin(GL_QUADS)
    # Перед
    if side[0]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 0)
        glVertex3f(-1, -1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(-1, 1, 1)
    # Зад
    if side[1]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 1)
        glVertex3f(-1, 1, -1)
        glVertex3f(1, 1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(-1, -1, -1)
    # Верх
    if side[2]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 2)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, 1, 1)
        glVertex3f(1, 1, 1)
        glVertex3f(1, 1, -1)
    # Низ
    if side[3]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 3)
        glVertex3f(-1, -1, -1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, -1, 1)
        glVertex3f(-1, -1, 1)
    # право
    if side[4]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 4)
        glVertex3f(1, 1, 1)
        glVertex3f(1, -1, 1)
        glVertex3f(1, -1, -1)
        glVertex3f(1, 1, -1)
    # Лево
    if side[5]:
        glColor4ub(255 - x, 255 - y, 255 - z, 255 - 5)
        glVertex3f(-1, 1, -1)
        glVertex3f(-1, -1, -1)
        glVertex3f(-1, -1, 1)
        glVertex3f(-1, 1, 1)
    glEnd()

    glPopMatrix()

def DrawBlockR(x, y, z, side):
    size = 0.5
    glColor3f(1, 1, 1)

    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    # Отрисовка блока
    glBegin(GL_QUADS)
    # Перед
    if side[0]:
        glTexCoord2f(1, 1)
        glVertex3f(-1, -1, 1)
        glTexCoord2f(0, 1)
        glVertex3f(1, -1, 1)
        glTexCoord2f(0, 0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1, 0)
        glVertex3f(-1, 1, 1)
    # Зад
    if side[1]:
        glTexCoord2f(1, 1)
        glVertex3f(-1, 1, -1)
        glTexCoord2f(0, 1)
        glVertex3f(1, 1, -1)
        glTexCoord2f(0, 0)
        glVertex3f(1, -1, -1)
        glTexCoord2f(1, 0)
        glVertex3f(-1, -1, -1)
    # Верх
    if side[2]:
        glTexCoord2f(1, 1)
        glVertex3f(-1, 1, -1)
        glTexCoord2f(0, 1)
        glVertex3f(-1, 1, 1)
        glTexCoord2f(0, 0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1, 0)
        glVertex3f(1, 1, -1)
    # Низ
    if side[3]:
        glTexCoord2f(1, 1)
        glVertex3f(-1, -1, -1)
        glTexCoord2f(0, 1)
        glVertex3f(1, -1, -1)
        glTexCoord2f(0, 0)
        glVertex3f(1, -1, 1)
        glTexCoord2f(1, 0)
        glVertex3f(-1, -1, 1)
    # право
    if side[4]:
        glTexCoord2f(1, 0)
        glVertex3f(1, 1, 1)
        glTexCoord2f(1, 1)
        glVertex3f(1, -1, 1)
        glTexCoord2f(0, 1)
        glVertex3f(1, -1, -1)
        glTexCoord2f(0, 0)
        glVertex3f(1, 1, -1)
    # Лево
    if side[5]:
        glTexCoord2f(1,0)
        glVertex3f(-1, 1, -1)
        glTexCoord2f(1, 1)
        glVertex3f(-1, -1, -1)
        glTexCoord2f(0, 1)
        glVertex3f(-1, -1, 1)
        glTexCoord2f(0, 0)
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
        for y in range(10):
            MAP[x, y, 0] = True
            ID[x, y, 0] = 2
    for x in range(10):
        for z in range(10):
            MAP[x, 0, z] = True
            ID[x, 0, z] = 0
    MAP[2, 1, 2] = True
    ID[2, 1, 2] = 2

def DrawMAP(mask):

    if mask:
        glClearColor(0.678, 0.847, 0.902, 1.0)
    else:
        glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    from Controls import MoveCam

    glPushMatrix()
    MoveCam()

    if mask:
        tex1 = load_texture("block/dirt.png")
        tex2 = load_texture("block/stone_bricks.png")
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, tex1)

    for x in range(10):
        for y in range(10):
            for z in range(10):
                    if MAP[x,y,z]==True:
                        if ID[x,y,z]==0:
                            if mask:
                                DrawBlockR(x,y,z,OPT(x, y, z))
                            else:
                                DrawBlockUn(x,y,z,OPT(x, y, z))
    if mask:

        glBindTexture(GL_TEXTURE_2D, tex2)
    for x in range(10):
        for y in range(10):
            for z in range(10):
                    if MAP[x,y,z]==True:
                        if ID[x,y,z]==2:
                            if mask:
                                DrawBlockR(x, y, z, OPT(x, y, z))
                            else:
                                DrawBlockUn(x, y, z, OPT(x, y, z))
    if mask:
        glDisable(GL_TEXTURE_2D)

    if not mask:
        glColor3f(0, 0, 0)
    glTranslatef(5, 0.5, 5)
    #model = OBJ('chr_knight.obj')
    #model.render()
    glPopMatrix()

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

def load_texture(filename):
    # Загрузить изображение из файла с помощью библиотеки PIL
    img = Image.open(filename)
    img_data = img.convert("RGBA").tobytes()

    # Создать объект текстуры в OpenGL
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)

    # Настроить параметры текстуры
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # Загрузить данные изображения в текстуру
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return tex

#NN
class OBJ:
    def __init__(self, filename):
        self.vertices = []
        self.faces = []

        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex = list(map(float, line.strip().split()[1:]))
                    self.vertices.append(vertex)
                elif line.startswith('f '):
                    face = [int(i.split('/')[0]) - 1 for i in line.strip().split()[1:]]
                    self.faces.append(face)

    def render(self):
        glBegin(GL_TRIANGLES)
        for face in self.faces:
            for vertex in face:
                glVertex3fv(self.vertices[vertex])
        glEnd()