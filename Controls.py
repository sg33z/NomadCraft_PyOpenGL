from SurvivalMode import *

def OnKey(window, key, scancode, action, mods):
    if key == glfw.KEY_ESCAPE:
        glfw.set_window_should_close(window, True)


def MoveBody():
    global xCorn, yCorn, Corn, S_Mspeed, GoGo
    from Draw import Blocks
    if GoGo[0] and not Blocks[int(CamPos[0] + 0.5 + np.sin(-Corn) * -S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.cos(-Corn) * -S_Mspeed)].have:  # W

        CamPos[0] += np.sin(-Corn) * -S_Mspeed
        CamPos[2] += np.cos(-Corn) * -S_Mspeed

    if GoGo[2] and not Blocks[int(CamPos[0] + 0.5 + np.sin(-Corn) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.cos(-Corn) * S_Mspeed)].have:  # S

        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[1] and not Blocks[int(CamPos[0] + 0.5 + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.sin(-Corn + (np.pi * 0.5)) * S_Mspeed)].have:  # A

        Corn += np.pi * 0.5
        CamPos[0] += np.sin(-Corn) * S_Mspeed
        CamPos[2] += np.cos(-Corn) * S_Mspeed

    if GoGo[3] and not Blocks[int(CamPos[0] + 0.5 + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed), int(CamPos[1] - 0.5), int(
            CamPos[2] + 0.5 + np.sin(-Corn - (np.pi * 0.5)) * S_Mspeed)].have:  # D

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

    onJump()

    glRotatef(-xCorn, 1, 0, 0)
    glRotatef(-yCorn, 0, 1, 0)
    glTranslatef(-CamPos[0], -CamPos[1], -CamPos[2])

    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    camera_pos = glGetFloatv(GL_MODELVIEW_MATRIX)[3][:3]

    Corn = (-yCorn / 180) * np.pi
    MoveBody()


