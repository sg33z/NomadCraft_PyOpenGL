import glfw
from OpenGL.GL import *
def OnResize(window, width, height):
    glViewport(0, 0, width, height)
    glLoadIdentity()
    k = width / height
    sz = 0.1
    glFrustum(-k * sz, k * sz, -sz, sz, sz * 2, 80)
keyboard_listener = None

def Create_Window():
    global keyboard_listener
    #Инициализация GLFW
    if not glfw.init():
        return

    # создание окна
    window = glfw.create_window(800, 500, "NomadCraft PyEdition", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    # Установка настроек OpenGL
    width, height = glfw.get_window_size(window)
    k = width / height
    sz = 0.1
    glFrustum(-k * sz, k * sz, -sz, sz, sz * 2, 80)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)


    #Обьявление функций обработчиков
    from Controls import OnKeyDown , OnKeyUp, OnKey, MouseMove, MouseClick, keyboard

    keyboard_listener = keyboard.Listener(on_press=OnKeyDown, on_release=OnKeyUp)
    keyboard_listener.start()

    glfw.set_framebuffer_size_callback(window, OnResize)
    glfw.set_key_callback(window, OnKey)
    glfw.set_cursor_pos_callback(window, MouseMove)
    glfw.set_mouse_button_callback(window, MouseClick)

    # Зародыш генерации карты
    from Draw import BlockStart
    BlockStart()
    return window
def Delete_Window():
    global keyboard_listener
    glfw.terminate()
    keyboard_listener.stop()

def FPS_count():
    import time
    # Переменные для расчетa FPS
    frames = 0
    start_time = time.time()

    # обновление счетчика FPS
    frames += 1
    current_time = time.time()
    if current_time - start_time >= 1.0:
        fps = frames / (current_time - start_time)
        print("FPS: ", fps)
        frames = 0
        start_time = current_time