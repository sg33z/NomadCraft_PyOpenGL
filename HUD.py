import glfw
from OpenGL.GL import *

SetFromHudId = 104
def HUD_Show(window):
    width, height = glfw.get_window_size(window)
    glDisable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0,1,0,1,-1,1)
    glMatrixMode(GL_MODELVIEW)


    coord_x = 200/width
    coord_y = 0/height

    size_x = 400/width
    size_y = 50/height

    glLoadIdentity()
    glPushMatrix()
    glBegin(GL_QUADS)
    glColor3f(1, 1, 0)
    glVertex2f(coord_x, coord_y)
    glVertex2f((coord_x+size_x), coord_y)
    glVertex2f((coord_x+size_x), (coord_y+size_y))
    glVertex2f(coord_x, (coord_y+size_y))
    glEnd()



    glPopMatrix()

