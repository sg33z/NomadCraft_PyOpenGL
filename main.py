from Draw import *
from Init_Window import *



window = Create_Window()

# основной цикл
while not glfw.window_should_close(window):
    # обработка событий
    glfw.poll_events()


    DrawMAP(True)
    FPS_count()



    glfw.swap_buffers(window)

Delete_Window()


