from Draw import DrawMAP
from HUD import HUD_Show
from SurvivalMode import TimerUpdate
from Init_Window import Create_Window,Delete_Window
import glfw


window = Create_Window()
w,h=glfw.get_window_size(window)

# основной цикл
while not glfw.window_should_close(window):

    # обработка событий
    glfw.poll_events()

    TimerUpdate(window)

    DrawMAP(True,w,h)
    HUD_Show(window)
    #Счет ФПС
    #FPS_count()


    #Смена буферов(переход к следующему файлу)
    glfw.swap_buffers(window)

Delete_Window()


