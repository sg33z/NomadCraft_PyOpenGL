import glfw
from OpenGL.GL import *

def HUD_Show(window):
    width, height = glfw.get_window_size(window)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,width,0,height,-1,1)
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)
    glVertex2f(200, 0)
    glVertex2f(600, 0)
    glVertex2f(600, 80)
    glVertex2f(200, 80)
    glEnd()
    glPopMatrix()

