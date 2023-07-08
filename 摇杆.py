import pygame
import pygame
import win32api
# 初始化Pygame
pygame.init()

# 获取摇杆控制器
joystick = pygame.joystick.Joystick(0)
joystick.init()

# 创建日志文件
#log_file = open("./yaoganshuju/joystick_log.txt", "w")
flag=True
last=0
while flag:
    
    for event in pygame.event.get():
            if event.type == pygame.JOYAXISMOTION:
                if event.axis ==0:
                    axis = event.axis
                    value = event.value
                    
                    if round(value,3)-round(last,3)>0.006 or round(last,3)-round(value,3)>0.006:
                        #log_file.write("Axis {:}: {:.3f}\n".format(axis,value))
                        print("Axis {:}: {:.3f}\n".format(axis,value))
                    last = event.value

            if event.type == pygame.JOYBUTTONDOWN:
                button = event.button
                print(f"Button {button} down\n")
            if event.type == pygame.JOYBUTTONUP:
                button = event.button
                print(f"Button {button} up\n")

            # 如果按下摇杆的13号按钮（SELECT），退出程序
            if event.type == pygame.JOYBUTTONDOWN and event.button == 13:
                flag=False
                #log_file.close()
                #pygame.quit()      #这个是导致会话崩溃的根本原因
                break