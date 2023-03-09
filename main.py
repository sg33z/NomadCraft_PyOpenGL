from Draw import *
from HUD import *
from Init_Window import *



window = Create_Window()
w,h=glfw.get_window_size(window)
# основной цикл
while not glfw.window_should_close(window):
    # обработка событий
    glfw.poll_events()
    True_Projection(w,h)
    DrawMAP(True)
    HUD_Show(window)



    FPS_count()



    glfw.swap_buffers(window)

Delete_Window()


