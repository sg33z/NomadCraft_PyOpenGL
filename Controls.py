import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from pynput import keyboard
from Draw import MAP,ID

# Зародыши Управления

xCorn = 0
yCorn = 0
Corn = 0
S_Mspeed = 0.05
GoGo = [False, False, False, False]

CamPos = [3, 2.1, 3]

OldMousePos = [500 + 800 / 2, 250 + 500 / 2]


def OnKey(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


def OnKeyDown(key):
    global GoGo
    if key == keyboard.KeyCode.from_char('w') == key:
        GoGo[0] = True
    if key == keyboard.KeyCode.from_char('a') == key:
        GoGo[1] = True
    if key == keyboard.KeyCode.from_char('s') == key:
        GoGo[2] = True
    if key == keyboard.KeyCode.from_char('d') == key:
        GoGo[3] = True


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


def MoveBody():
    global xCorn, yCorn, Corn, S_Mspeed, GoGo, MAP
    if GoGo[0]:  # and MAP[int(CamPos[0] + np.sin(-Corn) * -S_Mspeed), int(CamPos[1]-1), int(CamPos[2] + np.cos(-Corn) * -S_Mspeed)]!=True: # W

        CamPos[0] += np.sin(-Corn) * -S_Mspeed
        CamPos[2] += np.cos(-Corn) * -S_Mspeed

    if GoGo[2]:  # and MAP[int(CamPos[0] + np.sin(-Corn) * S_Mspeed), int(CamPos[1]-1), int(CamPos[2]+ np.cos(-Corn) * S_Mspeed)]!=True: # S

        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[1]:  # and MAP[int(CamPos[0] + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed),int(CamPos[1]-1),int(CamPos[2] + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed)]!=True: # A

        Corn += np.pi * 0.5
        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[3]:  # and MAP[int(CamPos[0] + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed),int(CamPos[1]-1),int(CamPos[2] + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed)]!=True: # D

        Corn -= np.pi * 0.5
        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed


def MouseMove(window, xpos, ypos):
    global xCorn, yCorn, OldMousePos

    sensitivity = 0.1

    center_x, center_y = glfw.get_framebuffer_size(window)
    center_x, center_y = center_x / 2, center_y / 2

    dx = xpos - OldMousePos[0]
    dy = OldMousePos[1] - ypos

    xCorn += dy * sensitivity
    yCorn -= dx * sensitivity

    if xCorn > 89.0:
        xCorn = 89.0
    elif xCorn < -89.0:
        xCorn = -89.0

    if yCorn > 360.0:
        yCorn -= 360.0
    elif yCorn < -360.0:
        yCorn += 360.0

    glfw.set_cursor_pos(window, center_x, center_y)
    OldMousePos = center_x, center_y


viewport = None
modelview = None
projection = None
camera_pos = np.array([0, 0, 0], dtype=np.float32)


def MoveCam():
    global xCorn, yCorn, CamPos, Corn, viewport, modelview, projection, camera_pos
    glMatrixMode(GL_MODELVIEW)

    glRotatef(-xCorn, 1, 0, 0)
    glRotatef(-yCorn, 0, 1, 0)
    glTranslatef(-CamPos[0], -CamPos[1], -CamPos[2])

    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    camera_pos = glGetFloatv(GL_MODELVIEW_MATRIX)[3][:3]

    Corn = (-yCorn / 180) * np.pi
    MoveBody()


def MouseClick(window, button, action, mods):
    global MAP, CamPos, viewport, modelview, projection, camera_pos
    ## NN

    bPos = get_object_coordinates(camera_pos, viewport, modelview, projection, MAP)
    if bPos is not None:
        x, y, z = bPos
        if MAP[int(x), int(y), int(z)]:
            MAP[int(x), int(y), int(z)] = False


def CHECK(arr, n):
    shape = np.shape(arr)
    return shape[n]


##NN
def get_object_coordinates(camera_pos, viewport, modelview, projection, map_data):
    # Получить координаты центра экрана
    center = np.array([(viewport[2] - viewport[0]) / 2, (viewport[3] - viewport[1]) / 2])

    # Преобразовать координаты центра экрана в мировые координаты
    winz = glReadPixels(center[0], center[1], 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)
    worldx, worldy, worldz = gluUnProject(center[0], center[1], winz, modelview, projection, viewport)
    ray_start = np.array([worldx, worldy, worldz])

    # Определить направление луча, проходящего через центр экрана
    winx, winy, winz = gluProject(camera_pos[0], camera_pos[1], camera_pos[2], modelview, projection, viewport)
    ray_end = np.array(gluUnProject(winx, winy, 0.0, modelview, projection, viewport))
    ray_dir = ray_end - camera_pos

    # Найти координаты блока, на который смотрит камера
    block_size = 1  # Размер блока в мировых координатах
    max_distance = 100  # Максимальная дистанция, на которую ищется блок
    t = 0
    while t < max_distance:
        # Вычислить координаты блока, на котором находится луч
        block_pos = np.floor(ray_start / block_size)

        # Если блок находится в пределах карты и существует в булевом массиве MAP,
        # то вернуть его координаты
        if np.all(block_pos >= 0) and np.all(block_pos < map_data.shape) and map_data[
            tuple(block_pos.astype(int))] == True:
            object_pos = block_pos * block_size + block_size / 2
            return object_pos

        # Сдвинуть точку начала луча в направлении луча
        ray_start += ray_dir * block_size
        t += block_size

    # Если не найдено ни одного блока на максимальной дистанции, вернуть None
    return None
