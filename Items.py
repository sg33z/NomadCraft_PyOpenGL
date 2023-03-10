import glfw
from OpenGL.GL import *
import numpy as np
from PIL import Image

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
tex = []
DestTex =[]
def InitTexMass():
    global tex,DestTex
    for i in range(10):
        DestTex = [load_texture(f"block/destroy_{i}.png")]
    tex = [ load_texture("block/stone_bricks.png"),
            load_texture("block/dirt.png"),
            load_texture("block/wood.png"),
            load_texture("block/oreDiamond.png")]


#Класс выпавшего предмета(Зародыш)
class DropItem:
    def __init__(self, ID, x,y,z):
        self.tex = tex[ID]
        self.ID = ID
        self.x,self.y,self.z = x,y,z
        self.rot = 0
        self.model3d = True
    def update(self):
        self.rot += 1

        self.y = np.sin(self.rot/20)*0.1
        glPushMatrix()
        glTranslatef(self.x, self.y+1, self.z)
        glScalef(0.2,0.2,0.2)
        glRotatef(self.rot, 0, 1, 0)
        if self.model3d:
            Block(self.ID,0,0,0).Lidraw(True)


        glPopMatrix()

#Класс блока
class Block:
    def __init__(self, ID, x,y,z):

        self.ID = ID
        self.tex = tex[ID]
        self.x,self.y,self.z = x,y,z
        self.have = False
        self.hard = 5
        self.destroy = 0
    def SetHave(self,ID,have):
        self.ID = ID
        self.have = have
    def SetDestroy(self,DestroyLVL):
        self.destroy = DestroyLVL
    def Optimization(self,obj):
        #Низшая оптимизация
        side = [True,True,True,True,True,True]
        if obj[self.x, self.y + 1, self.z] == True:
            side[2] = False
        if obj[self.x, self.y - 1, self.z] == True:
            side[3] = False
        if obj[self.x, self.y, self.z + 1] == True:
            side[0] = False
        if obj[self.x, self.y, self.z - 1] == True:
            side[1] = False
        if obj[self.x + 1, self.y, self.z] == True:
            side[4] = False
        if obj[self.x - 1, self.y, self.z] == True:
            side[5] = False
        return side

    def Lidraw(self,mask):
        size = 0.5
        if mask:
            glColor3f(1, 1, 1)
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.tex)

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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 0)
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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 1)
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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 2)
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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 3)
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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 4)
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
            glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 5)
            glVertex3f(-1, 1, -1)
            glVertex3f(-1, -1, -1)
            glVertex3f(-1, -1, 1)
            glVertex3f(-1, 1, 1)


        glEnd()
        glPopMatrix()
        glDisable(GL_TEXTURE_2D)

    def draw(self, mask, obj):
        if self.have:
            self.tex = tex[self.ID]
            if self.destroy !=0:
                # Активируем текстурный блок 0
                glActiveTexture(GL_TEXTURE0)

                # Связываем первую текстуру с текстурным блоком 0
                glBindTexture(GL_TEXTURE_2D, self.tex)

                # Активируем текстурный блок 1
                glActiveTexture(GL_TEXTURE1)

                # Связываем вторую текстуру с текстурным блоком 1
                glBindTexture(GL_TEXTURE_2D, DestTex[self.destroy])

                # Объединяем две текстуры в одну
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
                glTexEnvi(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)
                glTexEnvi(GL_TEXTURE_ENV, GL_COMBINE_RGB, GL_INTERPOLATE)
                glTexEnvi(GL_TEXTURE_ENV, GL_SRC0_RGB, GL_TEXTURE)
                glTexEnvi(GL_TEXTURE_ENV, GL_SRC1_RGB, GL_PREVIOUS)
                glTexEnvi(GL_TEXTURE_ENV, GL_SRC2_RGB, GL_TEXTURE)
                glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND0_RGB, GL_SRC_COLOR)
                glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND1_RGB, GL_SRC_COLOR)
                glTexEnvi(GL_TEXTURE_ENV, GL_OPERAND2_RGB, GL_SRC_ALPHA)

                # Активируем текстурный блок 0
                glActiveTexture(GL_TEXTURE0)
            size = 0.5
            if mask:
                glColor3f(1, 1, 1)
                glEnable(GL_TEXTURE_2D)
                self.tex = tex[self.ID]
                glBindTexture(GL_TEXTURE_2D, self.tex)

            side = self.Optimization(obj)

            # Задать положение блока
            glPushMatrix()
            glTranslatef(self.x, self.y, self.z)
            glScalef(size, size, size)
            # Отрисовка блока
            glBegin(GL_QUADS)
            if side[0]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 0)
                    glVertex3f(-1, -1, 1)
                    glVertex3f(1, -1, 1)
                    glVertex3f(1, 1, 1)
                    glVertex3f(-1, 1, 1)

            # Зад
            if side[1]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 1)
                    glVertex3f(-1, 1, -1)
                    glVertex3f(1, 1, -1)
                    glVertex3f(1, -1, -1)
                    glVertex3f(-1, -1, -1)

            # Верх
            if side[2]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 2)
                    glVertex3f(-1, 1, -1)
                    glVertex3f(-1, 1, 1)
                    glVertex3f(1, 1, 1)
                    glVertex3f(1, 1, -1)

            # Низ
            if side[3]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 3)
                    glVertex3f(-1, -1, -1)
                    glVertex3f(1, -1, -1)
                    glVertex3f(1, -1, 1)
                    glVertex3f(-1, -1, 1)

            # право
            if side[4]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 4)
                    glVertex3f(1, 1, 1)
                    glVertex3f(1, -1, 1)
                    glVertex3f(1, -1, -1)
                    glVertex3f(1, 1, -1)

            # Лево
            if side[5]:
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
                    glColor4ub(255 - self.x, 255 - self.y, 255 - self.z, 255 - 5)
                    glVertex3f(-1, 1, -1)
                    glVertex3f(-1, -1, -1)
                    glVertex3f(-1, -1, 1)
                    glVertex3f(-1, 1, 1)




            glEnd()
            glPopMatrix()
            glDisable(GL_TEXTURE_2D)




