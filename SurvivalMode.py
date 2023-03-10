import glfw
from OpenGL.GL import *
import numpy as np
from time import time
from pynput import keyboard
from Draw import DrawMAP
from VarLock import *



#Параметры камеры
xCorn = 0
yCorn = 0
Corn = 0
S_Mspeed = 0.05
GoGo = [False, False, False, False]
CamPos = [3, 2.1, 3]

#Параметры Мыши
OldMousePos = [500 + 800 / 2, 250 + 500 / 2]

#Флаги Прыжка
Jump = False
jp = None

#Параметр отрисовки(ненужен)
Mask = True
def OnKeyDown(key):
    global GoGo, Jump, jp,CamPos
    if key == keyboard.KeyCode.from_char('w') == key:
        GoGo[0] = True
    if key == keyboard.KeyCode.from_char('a') == key:
        GoGo[1] = True
    if key == keyboard.KeyCode.from_char('s') == key:
        GoGo[2] = True
    if key == keyboard.KeyCode.from_char('d') == key:
        GoGo[3] = True
    if key == keyboard.Key.space == key:
        if not Jump and Blocks[int(CamPos[0] + 0.5), int(CamPos[1] - 1), int(CamPos[2] + 0.5)].have:
            Jump = True
            jp = CamPos[1] + 1.2

def onJump():
    global Jump,jp
    if not Blocks[int(CamPos[0] + 0.5), int(CamPos[1] - 1), int(CamPos[2] + 0.5)].have and not Jump:
        CamPos[1] = CamPos[1] - 0.08
    if Jump:
        CamPos[1] = CamPos[1] + 0.08
        if CamPos[1] > jp:
            Jump = False



def OnKeyUp(key):
    global GoGo
    if key == keyboard.KeyCode.from_char('w') == key:
        GoGo[0] = False
    if key == keyboard.KeyCode.from_char('a') == key:
        GoGo[1] = False
    if key == keyboard.KeyCode.from_char('s') == key:
        GoGo[2] = False
    if key == keyboard.KeyCode.from_char('d') == key:
        GoGo[3] = False


def MouseClick(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_RIGHT and action==glfw.PRESS:
        bPos = BlockUnCheck(window)
        print(bPos)

        if bPos is not None:
            x, y, z,s = bPos
            Blocks[int(x), int(y + 1), int(z)].SetHave(2, True)
            if x < 11 and y < 11 and z < 11:
                if s == 2:
                    Blocks[int(x), int(y+1), int(z)].SetHave(2,True)

                elif s == 3:
                    Blocks[int(x), int(y-1), int(z)].SetHave(2,True)
                elif s == 0:
                    Blocks[int(x), int(y), int(z+1)].SetHave(2,True)
                elif s == 1:
                    Blocks[int(x), int(y), int(z - 1)].SetHave(2,True)
                elif s == 4:
                    Blocks[int(x+1), int(y), int(z)].SetHave(2,True)
                elif s == 5:
                    Blocks[int(x - 1), int(y), int(z)].SetHave(2,True)

    global start_time, stop_time, timer_enable
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            start_time = time()
            timer_enable = True

        if action == glfw.RELEASE:
            timer_enable = False
            stop_time = time()

timer_enable = False
stop_time= 0
g=0
def TimerUpdate(window):
    global start_time,stop_time, timer_enable,g
    if timer_enable:
        x, y, z, s = BlockUnCheck(window)
        if (time() - start_time) >= Blocks[x,y,z].hard/10:
            g+=1
            Blocks[x,y,z].SetDestroy(g)
            print(time() - start_time)
            print("destroy level = ", Blocks[x,y,z].destroy ,"|", Blocks[x,y,z].hard)
            start_time=time()
            if Blocks[x,y,z].destroy >= Blocks[x,y,z].hard:
                print("сломан")
                Blocks[x,y,z].SetHave(3,False)
                Blocks[x,y,z].SetDestroy(0)
                g=0
                
def BlockUnCheck(window):
    #Проверка цвета блока(ака его координаты)

    clr = [3]
    w,h = glfw.get_window_size(window)
    DrawMAP(False,w,h)

    clr = glReadPixels(w/2, h/2, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
    color = np.frombuffer(clr, dtype=np.uint8)

    x = (255-color[0])
    y = (255-color[1])
    z = (255-color[2])
    s = (255-color[3])
    if x!=255 and y!=255 and z!=255:
        return x,y,z,s
    else:
        return None