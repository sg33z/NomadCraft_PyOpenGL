from Controls.SurvivalMode import *



def OnKey(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


Jump = False
jp = None


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


def MoveBody():
    global xCorn, yCorn, Corn, S_Mspeed, GoGo, MAP
    if GoGo[0] and not MAP[int(CamPos[0] + 0.5 + np.sin(-Corn) * -S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.cos(-Corn) * -S_Mspeed)]:  # W

        CamPos[0] += np.sin(-Corn) * -S_Mspeed
        CamPos[2] += np.cos(-Corn) * -S_Mspeed

    if GoGo[2] and not MAP[int(CamPos[0] + 0.5 + np.sin(-Corn) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.cos(-Corn) * S_Mspeed)]:  # S

        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[1] and not MAP[int(CamPos[0] + 0.5 + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed)]:  # A

        Corn += np.pi * 0.5
        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[3] and not MAP[int(CamPos[0] + 0.5 + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed)]:  # D

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
    global xCorn, yCorn, CamPos, Corn, viewport, modelview, projection, camera_pos, Jump, jp
    glMatrixMode(GL_MODELVIEW)

    if not MAP[int(CamPos[0] + 0.5), int(CamPos[1] - 1), int(CamPos[2] + 0.5)] and not Jump:
        CamPos[1] = CamPos[1] - 0.08

    if Jump:
        CamPos[1] = CamPos[1] + 0.08
        if CamPos[1] > jp:
            Jump = False
        else:
            Jump = True

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
    global MAP
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        bPos = BlockUnCheck(window)
        print(bPos)
        if bPos is not None:
            x, y, z, s = bPos
            if x < 10 and y < 10 and z < 10:
                MAP[int(x), int(y), int(z)] = False
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        bPos = BlockUnCheck(window)
        print(bPos)
        if bPos is not None:
            x, y, z, s = bPos
            if x < 10 and y < 10 and z < 10:
                if s == 2:
                    MAP[int(x), int(y + 1), int(z)] = True
                    ID[int(x), int(y + 1), int(z)] = 2
                elif s == 3:
                    MAP[int(x), int(y - 1), int(z)] = True
                    ID[int(x), int(y - 1), int(z)] = 2
                elif s == 0:
                    MAP[int(x), int(y), int(z + 1)] = True
                    ID[int(x), int(y), int(z + 1)] = 2
                elif s == 1:
                    MAP[int(x), int(y), int(z - 1)] = True
                    ID[int(x), int(y), int(z - 1)] = 2
                elif s == 4:
                    MAP[int(x + 1), int(y), int(z)] = True
                    ID[int(x + 1), int(y), int(z)] = 2
                elif s == 5:
                    MAP[int(x - 1), int(y), int(z)] = True
                    ID[int(x - 1), int(y), int(z)] = 2





# Неработает
def CHECK(arr, n):
    shape = np.shape(arr)
    return shape[n]

