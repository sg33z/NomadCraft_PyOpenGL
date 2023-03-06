from Controls import *
from Draw import *
import time
import pycuda.autoinit
import pycuda.driver as drv

# Выбираем вторую видеокарту (с индексом 1)
dev = drv.Device(0)
# Выводим информацию о выбранной видеокарте
print(dev.get_attributes())

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
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)

    # установка функций обработчиков
    keyboard_listener = keyboard.Listener(on_press=OnKeyDown, on_release=OnKeyUp)
    keyboard_listener.start()

    glfw.set_framebuffer_size_callback(window, OnResize)
    glfw.set_key_callback(window, OnKey)
    glfw.set_cursor_pos_callback(window, MouseMove)
    glfw.set_mouse_button_callback(window, MouseClick)
    lastX, lastY = glfw.get_cursor_pos(window)
    # FPS ept
    frames = 0
    start_time = time.time()
    #Зародыш генерации карты
    BlockStart()
    # основной цикл
    while not glfw.window_should_close(window):
        # обработка событий
        glfw.poll_events()


        DrawMAP(True)

        # обновление счетчика FPS
        frames += 1
        current_time = time.time()
        if current_time - start_time >= 1.0:
            fps = frames / (current_time - start_time)
            print("FPS: ", fps)
            frames = 0
            start_time = current_time

        # обновление окна
        glfw.swap_buffers(window)

    # выход
    glfw.terminate()
    keyboard_listener.stop()

if __name__ == '__main__':
    main()