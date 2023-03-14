import glfw

from OpenGL.GL import *
import numpy as np
from PIL import Image


vbo = []
vbotex = []
# вершинные координаты
FrontVBO = np.array([
    -1, -1, 1,
     1, -1, 1,
     1,  1, 1,
     -1,  1, 1
], dtype=np.float32)

BackVBO = np.array([
    -1, 1, -1,
     1, 1, -1,
     1,  -1, -1,
     -1,  -1, -1
], dtype=np.float32)

TopVBO = np.array([
    -1, 1, -1,
     -1, 1, 1,
     1,  1, 1,
     1,  1, -1
], dtype=np.float32)

BottomVBO = np.array([
    -1, -1, -1,
     1, -1, -1,
     1,  -1, 1,
     -1,  -1, 1
], dtype=np.float32)

RightVBO = np.array([
    1, 1, 1,
     1, -1, 1,
     1,  -1, -1,
     1,  1, -1
], dtype=np.float32)

LeftVBO = np.array([
    -1, 1, -1,
     -1, -1, -1,
     -1,  -1, 1,
     -1,  1, 1
], dtype=np.float32)


# текстурные координаты ---------------
FrontTexCoord = np.array([
    0, 1,
    1, 1,
    1, 0,
    0,0
], dtype=np.float32)

BackTexCoord = np.array([
    1, 0,
    0, 0,
    0, 1,
    1, 1
], dtype=np.float32)

TopTexCoord = np.array([
    0, 0,
    0, 1,
    1, 1,
    1, 0
], dtype=np.float32)

BottomTexCoord = np.array([
    0, 0,
    1, 0,
    1, 1,
    0, 1
], dtype=np.float32)

RightTexCoord = np.array([
    0, 0,
    0, 1,
    1, 1,
    1, 0
], dtype=np.float32)

LeftTexCoord = np.array([
    0, 0,
    0, 1,
    1, 1,
    1, 0
], dtype=np.float32)
def load_texture(filename):
    # Загрузить изображение из файла с помощью библиотеки PIL
    img = Image.open(filename)
    img_data = img.convert("RGBA").tobytes()

    # Создать объект текстуры в OpenGL
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # Настроить параметры текстуры
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexParameter(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

    # Загрузить данные изображения в текстуру
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.size[0], img.size[1], 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    return tex
def InitItems():
    global tex,DestTex


    DestTex=[load_texture("block/destroy_0.png"),
             load_texture("block/destroy_1.png"),
             load_texture("block/destroy_2.png"),
             load_texture("block/destroy_3.png"),
             load_texture("block/destroy_4.png"),
             load_texture("block/destroy_5.png"),
             load_texture("block/destroy_6.png"),
             load_texture("block/destroy_7.png"),
             load_texture("block/destroy_8.png"),
             load_texture("block/destroy_9.png"),]

    tex = [ load_texture("block/stone_bricks.png"), #0
            load_texture("block/dirt.png"),         #1
            load_texture("block/wood.png"),         #2
            load_texture("block/oreDiamond.png"),   #3
            load_texture("block/glass.png")         #4
            ]
    # C
    global vbo, vboTex , TopVBO,BottomVBO,LeftVBO,RightVBO,FrontVBO,BackVBO
    global TopTexCoord,BottomTexCoord , LeftTexCoord, RightTexCoord,FrontTexCoord, BackTexCoord
    vbo = glGenBuffers(6)
    vboTex = glGenBuffers(6)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, FrontVBO.nbytes, FrontVBO, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, BackVBO.nbytes, BackVBO, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[2])
    glBufferData(GL_ARRAY_BUFFER, TopVBO.nbytes, TopVBO, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[3])
    glBufferData(GL_ARRAY_BUFFER, BottomVBO.nbytes, BottomVBO, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[4])
    glBufferData(GL_ARRAY_BUFFER, RightVBO.nbytes, RightVBO, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vbo[5])
    glBufferData(GL_ARRAY_BUFFER, LeftVBO.nbytes, LeftVBO, GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, vboTex[0])
    glBufferData(GL_ARRAY_BUFFER, FrontTexCoord.nbytes, FrontTexCoord, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTex[1])
    glBufferData(GL_ARRAY_BUFFER, BackTexCoord.nbytes, BackTexCoord, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTex[2])
    glBufferData(GL_ARRAY_BUFFER, TopTexCoord.nbytes, TopTexCoord, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTex[3])
    glBufferData(GL_ARRAY_BUFFER, BottomTexCoord.nbytes, BottomTexCoord, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTex[4])
    glBufferData(GL_ARRAY_BUFFER, RightTexCoord.nbytes, RightTexCoord, GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, vboTex[5])
    glBufferData(GL_ARRAY_BUFFER, LeftTexCoord.nbytes, LeftTexCoord, GL_STATIC_DRAW)



#Класс выпавшего предмета(Зародыш)
class DropItem:
    def __init__(self, ID, x,y,z):
        global tex,DestTex
        self.tex = tex[ID]
        self.ID = ID
        self.x,self.y,self.z = x,y,z
        self.rot = 0
        self.model3d = True

    def update(self,mask):
        self.rot += 1

        self.y = np.sin(self.rot/20)*0.1
        glPushMatrix()
        glTranslatef(self.x, self.y+1, self.z)
        glScalef(0.2,0.2,0.2)
        glRotatef(self.rot, 0, 1, 0)
        if self.model3d:
            Block(self.ID,0,0,0).Lidraw(mask)


        glPopMatrix()

#Класс блока
class Block:
    def __init__(self, ID, x,y,z):
        global tex, DestTex
        self.ID = ID
        self.x,self.y,self.z = x,y,z
        self.have = False
        self.hard = 5
        self.destroy = 0
        if ID > 100:
            self.Clear = True
            self.tex = tex[ID-100]
        else:
            self.tex = tex[ID]
            self.Clear = False
    def SetHave(self,ID,have):
        self.ID = ID
        self.have = have
    def SetDestroy(self,DestroyLVL):
        self.destroy = DestroyLVL
    def Optimization(self,obj):
        #Низшая оптимизация
        side = [True,True,True,True,True,True]
        if self.Clear:
            if obj[self.x, self.y + 1, self.z].have and obj[self.x, self.y + 1, self.z].Clear:
                side[2] = False
            if obj[self.x, self.y - 1, self.z].have and obj[self.x, self.y - 1, self.z].Clear:
                side[3] = False
            if obj[self.x, self.y, self.z + 1].have and obj[self.x, self.y, self.z+1].Clear:
                side[0] = False
            if obj[self.x, self.y, self.z - 1].have and obj[self.x, self.y, self.z-1].Clear:
                side[1] = False
            if obj[self.x + 1, self.y, self.z].have and obj[self.x+1, self.y, self.z].Clear:
                side[4] = False
            if obj[self.x - 1, self.y, self.z].have and obj[self.x-1, self.y, self.z].Clear:
                side[5] = False
            return side
        else:
            if obj[self.x, self.y + 1, self.z].have and not obj[self.x, self.y + 1, self.z].Clear:
                side[2] = False
            if obj[self.x, self.y - 1, self.z].have and not obj[self.x, self.y - 1, self.z].Clear:
                side[3] = False
            if obj[self.x, self.y, self.z + 1].have and not obj[self.x, self.y, self.z + 1].Clear:
                side[0] = False
            if obj[self.x, self.y, self.z - 1].have and not obj[self.x, self.y, self.z - 1].Clear:
                side[1] = False
            if obj[self.x + 1, self.y, self.z].have and not obj[self.x + 1, self.y, self.z].Clear:
                side[4] = False
            if obj[self.x - 1, self.y, self.z].have and not obj[self.x - 1, self.y, self.z].Clear:
                side[5] = False

            return side


    def Lidraw(self,mask):
        size = 0.5
        if mask:
            glColor3f(1, 1, 1)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex)
        else:
            glColor3f(0,0,0)
        # Задать положение блока
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScalef(size, size, size)
        # Отрисовка блока
        glBegin(GL_QUADS)
        if mask:
            glTexCoord2f(1, 1)
            glVertex3f(-1, -1, 1)
            glTexCoord2f(0, 1)
            glVertex3f(1, -1, 1)
            glTexCoord2f(0, 0)
            glVertex3f(1, 1, 1)
            glTexCoord2f(1, 0)
            glVertex3f(-1, 1, 1)
        else:
            glVertex3f(-1, -1, 1)
            glVertex3f(1, -1, 1)
            glVertex3f(1, 1, 1)
            glVertex3f(-1, 1, 1)

        # Зад
        if mask:
            glTexCoord2f(1, 1)
            glVertex3f(-1, 1, -1)
            glTexCoord2f(0, 1)
            glVertex3f(1, 1, -1)
            glTexCoord2f(0, 0)
            glVertex3f(1, -1, -1)
            glTexCoord2f(1, 0)
            glVertex3f(-1, -1, -1)
        else:
            glVertex3f(-1, 1, -1)
            glVertex3f(1, 1, -1)
            glVertex3f(1, -1, -1)
            glVertex3f(-1, -1, -1)

        # Верх
        if mask:
            glTexCoord2f(1, 1)
            glVertex3f(-1, 1, -1)
            glTexCoord2f(0, 1)
            glVertex3f(-1, 1, 1)
            glTexCoord2f(0, 0)
            glVertex3f(1, 1, 1)
            glTexCoord2f(1, 0)
            glVertex3f(1, 1, -1)
        else:
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, 1, 1)
            glVertex3f(1, 1, 1)
            glVertex3f(1, 1, -1)

        # Низ
        if mask:
            glTexCoord2f(1, 1)
            glVertex3f(-1, -1, -1)
            glTexCoord2f(0, 1)
            glVertex3f(1, -1, -1)
            glTexCoord2f(0, 0)
            glVertex3f(1, -1, 1)
            glTexCoord2f(1, 0)
            glVertex3f(-1, -1, 1)
        else:
            glVertex3f(-1, -1, -1)
            glVertex3f(1, -1, -1)
            glVertex3f(1, -1, 1)
            glVertex3f(-1, -1, 1)

        # право
        if mask:
            glTexCoord2f(1, 0)
            glVertex3f(1, 1, 1)
            glTexCoord2f(1, 1)
            glVertex3f(1, -1, 1)
            glTexCoord2f(0, 1)
            glVertex3f(1, -1, -1)
            glTexCoord2f(0, 0)
            glVertex3f(1, 1, -1)
        else:
            glVertex3f(1, 1, 1)
            glVertex3f(1, -1, 1)
            glVertex3f(1, -1, -1)
            glVertex3f(1, 1, -1)

        # Лево
        if mask:
            glTexCoord2f(1, 0)
            glVertex3f(-1, 1, -1)
            glTexCoord2f(1, 1)
            glVertex3f(-1, -1, -1)
            glTexCoord2f(0, 1)
            glVertex3f(-1, -1, 1)
            glTexCoord2f(0, 0)
            glVertex3f(-1, 1, 1)
        else:
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, -1, -1)
            glVertex3f(-1, -1, 1)
            glVertex3f(-1, 1, 1)


        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def draw(self,mask,obj):
        if self.have:
            if self.ID > 100:
                self.tex = tex[self.ID-100]
                self.Clear = True
            else:
                self.tex = tex[self.ID]


            global vbo, vbotex
            size = 0.5
            # NN
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_TEXTURE_COORD_ARRAY)

            if mask:
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glEnable(GL_BLEND)
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.tex)
                glColor3f(1, 1, 1)
            side = self.Optimization(obj)
            # Задать положение блока
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            glScalef(size, size, size)
            for i in range(6):
                if side[i]:
                    if mask:
                        glBindBuffer(GL_ARRAY_BUFFER, vboTex[i])
                        glTexCoordPointer(2, GL_FLOAT, 0, None)
                    else:
                        glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - i)

                    glBindBuffer(GL_ARRAY_BUFFER, vbo[i])
                    glVertexPointer(3, GL_FLOAT, 0, None)
                    glDrawArrays(GL_QUADS, 0, 4)


            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)
            glDisable(GL_TEXTURE_2D)
            glPopMatrix()
            glDisable(GL_BLEND)







