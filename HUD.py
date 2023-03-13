import glfw
from OpenGL.GL import *

SetFromHudId = 104
def HUD_Show(window):
    width, height = glfw.get_window_size(window)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()
    glViewport(0, 0, width, height)
    d = height/width
    glOrtho(-d, d, -1, 1, -1, 1)
    glMatrixMode(GL_MODELVIEW)




    glLoadIdentity()

    x = 0.7

    glPushMatrix()

    glBegin(GL_QUADS)
    glColor3f(1,0,0)
    glVertex2f(-0.7,-1)
    glVertex2f(-0.7, -0.7)
    glVertex2f(0.7, -0.7)
    glVertex2f(0.7, -1)
    glEnd()




    glPopMatrix()

