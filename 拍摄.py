#截图并获取摇杆信息
import numpy as np
import pyautogui
import cv2
import pygetwindow as gw
import pygame
import win32api
# 初始化Pygame
pygame.init()

# 获取摇杆控制器
joystick = pygame.joystick.Joystick(0)
joystick.init()

# 创建日志文件
#log_file = open("./Euroyaogan/joystick_log.txt", "w")
log_file = open("./yaoganshuju/Nomal+enhancejoystick_log.txt", "w")

# 监听摇杆事件
flag = True#退出循环判断
i=0
last=0
REC=False#是否进入截图准备状态
TRI=False#是否执行录制
while flag:

    if win32api.GetAsyncKeyState(0x36):#按6激活
        REC=True
    if win32api.GetAsyncKeyState(0x30):#按0暂停
        REC=False

    if REC==True:    
        # 获取屏幕截图
        target_window = gw.getWindowsWithTitle('American Truck Simulator')[0]  # Replace '目标窗口标题' with the actual title of the window
        #target_window = gw.getWindowsWithTitle('Euro Truck Simulator 2')[0]  # Replace '目标窗口标题' with the actual title of the window
        window_rect = (target_window.left, target_window.top, target_window.width, target_window.height)
    
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.crop((window_rect[0]+11+50, window_rect[1]+39+220, window_rect[0] + window_rect[2]-11-50, window_rect[1] + window_rect[3]-11))
    
        # 将截图转换成OpenCV图像
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        #resize = cv2.resize(frame, (320,180))#[:270,:480]
        # 显示图像
        cv2.imshow('Screen Capture', frame)
    

        # 检测按键事件，按下q键退出循环
        if cv2.waitKey(1) == ord('q'):
            break
      
    
    #接收摇杆信息
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN:#按下0键开始录制
                if event.button==0:
                    TRI=True
            if event.type == pygame.JOYBUTTONUP:#松开暂停
                if event.button==0:
                    TRI=False
            if event.type == pygame.JOYAXISMOTION and TRI==True:
                if event.axis ==0:
                    axis = event.axis
                    value = event.value
                    if round(value,3)-round(last,3)>0.006 or round(last,3)-round(value,3)>0.006:
                        log_file.write("Axis {:}: {:.3f}\n".format(axis,value))
                        print("Axis {:}: {:.3f}\n".format(axis,value))
                        cv2.imwrite(f'./NEcapture/capture_{i}.png',frame)
                    last = event.value
                        
                    i+=1
            

            # 如果按下摇杆的13号按钮（SELECT），退出程序
            if event.type == pygame.JOYBUTTONDOWN and event.button == 13:
                flag=False
                log_file.close()
                #pygame.quit()      #这个是导致会话崩溃的根本原因
                break
                #exit()
            #i+=1       
    #i+=1
# 清理资源
cv2.destroyAllWindows()