
import glfw
from OpenGL.GL import *
import numpy as np
from Items import Block

# Отрисовка
vision = [0,0,0]

CubeMap = [-1,-1,1,  1,-1,1,  1,1,1,  -1,1,1]
CubeVBO =None
Blocks = np.empty((101,101,101),dtype=Block)
for x in range(101):
    for y in range(101):
        for z in range(101):
            Blocks[x, y, z] = Block(0, x, y, z)

def BlockStart():
    global CubeMap,tex
    CubeVBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER,CubeVBO)
    glBufferData(GL_ARRAY_BUFFER, len(CubeMap) * 4, (GLfloat * len(CubeMap))(*CubeMap), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

    for x in range(100):
        for y in range(100):
            Blocks[x,y,0].SetHave(2,True)
    for x in range(100):
        for z in range(100):
            Blocks[x,0,z].SetHave(0,True)
    from Items import DropItem
    global woodBlock
    woodBlock = DropItem(2, 5, 1, 5)


def DrawMAP(mask, w,h):
    from Init_Window import  True_Projection, AllFarSet
    True_Projection(w, h)

    if mask:
        glClearColor(0.678, 0.847, 0.902, 1.0)
    else:
        glClearColor(0, 0, 0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    from Controls import MoveCam
    glPushMatrix()
    MoveCam()
    from Controls import CamPos
    i,j,k= CamPos
    for x in range(int(i-AllFarSet),int(AllFarSet+i)):
        for y in range(int(j-AllFarSet),int(AllFarSet+j)):
            for z in range(int(k-AllFarSet),int(AllFarSet+k)):
                if not Blocks[x,y,z].Clear:
                    Blocks[x,y,z].draw(mask,Blocks)

    for x in range(int(i - AllFarSet), int(AllFarSet + i)):
        for y in range(int(j - AllFarSet), int(AllFarSet + j)):
            for z in range(int(k - AllFarSet), int(AllFarSet + k)):
                if Blocks[x,y,z].Clear:
                    Blocks[x,y,z].draw(mask,Blocks)

    global woodBlock
    woodBlock.update(mask)
    #if not mask:
        #glColor3f(0, 0, 0)
    #model = OBJ('chr_knight.obj')
    #model.render()



    glPopMatrix()

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

