import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import pyrr
import glad
import numpy as np
from pynput import keyboard

from Controls import *
from Draw import *

def OnResize(window, width, height):

    glViewport(0, 0, width, height)
    glLoadIdentity()
    k = width / height
    sz = 0.1
    glFrustum(-k * sz, k * sz, -sz, sz, sz * 2, 80)






def main():
    # инициализация GLFW
    if not glfw.init():
        return

    # создание окна
    window = glfw.create_window(800, 500, "NomadCraft PyEdition", None, None)
    if not window:
        glfw.terminate()
        return

    w,h=glfw.get_framebuffer_size(window)
    k=w/h
    sz=0.1

    # установка контекста OpenGL
    glfw.make_context_current(window)
    glFrustum(-k * sz, k * sz, -sz, sz, sz * 2, 80)
    glEnable(GL_DEPTH_TEST)

    # установка функций обработчиков
    keyboard_listener = keyboard.Listener(on_press=OnKeyDown, on_release=OnKeyUp)
    keyboard_listener.start()

    glfw.set_framebuffer_size_callback(window, OnResize)
    glfw.set_key_callback(window, OnKey)
    glfw.set_cursor_pos_callback(window, MouseMove)
    glfw.set_mouse_button_callback(window, MouseClick)
    lastX, lastY = glfw.get_cursor_pos(window)


    #Зародиш генерации карты
    BlockStart()
    # основной цикл
    while not glfw.window_should_close(window):
        # обработка событий
        glfw.poll_events()
        # очистка экрана
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.678, 0.847, 0.902, 1.0)

        glPushMatrix()

        MoveCam()
        DrawMAP()

        glPopMatrix()
        # обновление окна
        glfw.swap_buffers(window)

    # выход
    glfw.terminate()
    keyboard_listener.stop()

if __name__ == '__main__':
    main()