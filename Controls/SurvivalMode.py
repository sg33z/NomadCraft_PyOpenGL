import threading
from pynput import keyboard
import numpy as np
from Draw import MAP,ID
import glfw
from OpenGL.GL import *

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
    global GoGo, Jump, jp
    if key == keyboard.KeyCode.from_char('w') == key:
        GoGo[0] = True
    if key == keyboard.KeyCode.from_char('a') == key:
        GoGo[1] = True
    if key == keyboard.KeyCode.from_char('s') == key:
        GoGo[2] = True
    if key == keyboard.KeyCode.from_char('d') == key:
        GoGo[3] = True
        print('w')
    if key == keyboard.Key.space == key:
        if not Jump and MAP[int(CamPos[0] + 0.5), int(CamPos[1] - 1), int(CamPos[2] + 0.5)]:
            Jump = True
            jp = CamPos[1] + 1.2

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
    global MAP
    if button == glfw.MOUSE_BUTTON_LEFT and action==glfw.PRESS:
        bPos = BlockUnCheck(window)
        print(bPos)
        if bPos is not None:
            x, y, z,s = bPos
            if x < 10 and y < 10 and z < 10:
                 MAP[int(x), int(y), int(z)] = False
    if button == glfw.MOUSE_BUTTON_RIGHT and action==glfw.PRESS:
        bPos = BlockUnCheck(window)
        print(bPos)
        if bPos is not None:
            x, y, z,s = bPos
            if x < 10 and y < 10 and z < 10:
                if s == 2:
                    MAP[int(x), int(y+1), int(z)] = True
                    ID[int(x), int(y+1), int(z)] = 2
                elif s == 3:
                    MAP[int(x), int(y-1), int(z)] = True
                    ID[int(x), int(y-1), int(z)] = 2
                elif s == 0:
                    MAP[int(x), int(y), int(z+1)] = True
                    ID[int(x), int(y), int(z+1)] = 2
                elif s == 1:
                    MAP[int(x), int(y), int(z - 1)] = True
                    ID[int(x), int(y), int(z - 1)] = 2
                elif s == 4:
                    MAP[int(x+1), int(y), int(z)] = True
                    ID[int(x+1), int(y), int(z)] = 2
                elif s == 5:
                    MAP[int(x - 1), int(y), int(z)] = True
                    ID[int(x - 1), int(y), int(z)] = 2

def BlockUnCheck(window):
    #Проверка цвета блока(ака его координаты)
    center_x, center_y = OldMousePos
    clr = [3]
    from Draw import DrawMAP
    from Init_Window import True_Projection
    w,h = glfw.get_window_size(window)
    True_Projection(w, h)
    DrawMAP(False)
    clr = glReadPixels(center_x, center_y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE)
    color = np.frombuffer(clr, dtype=np.uint8)

    x = (255-color[0])
    y = (255-color[1])
    z = (255-color[2])
    s = (255-color[3])
    if x!=255 and y!=255 and z!=255:
        return x,y,z,s
    else:
        return None