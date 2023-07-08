import numpy as np
import pyautogui
import cv2
import pygetwindow as gw
import pygame
import pyvjoy
from keras.models import load_model
import win32api
import time

global j
j = pyvjoy.VJoyDevice(1)

model = load_model('./771637_steering_model.h5')

def set_joystick_axis(x_value, y_value):
    # 创建 vJoy 设备实例
    joystick = pyvjoy.VJoyDevice(1)  # 1 表示设备 ID，根据你的设置进行调整
    
    # 设置左摇杆的值
    joystick.set_axis(pyvjoy.HID_USAGE_X, x_value)  # 设置 X 轴的值
    joystick.set_axis(pyvjoy.HID_USAGE_Y, y_value)  # 设置 Y 轴的值
    
    joystick.update()
    # 释放 vJoy 设备
    joystick.__del__

def stop_joystick():
    # 创建 vJoy 设备实例
    joystick = pyvjoy.VJoyDevice(1)  # 1 表示设备 ID，根据你的设置进行调整
    
    # 将摇杆值设置为中心位置
    x_value = 16384  # X 轴中心位置的值
    y_value = 16384  # Y 轴中心位置的值
    
    joystick.set_axis(pyvjoy.HID_USAGE_X, x_value)  # 设置 X 轴的值
    joystick.set_axis(pyvjoy.HID_USAGE_Y, y_value)  # 设置 Y 轴的值
    
    joystick.update()
    # 释放 vJoy 设备
    joystick.__del__

#img = cv2.imread('./P1.png')
AP = False
SETL = False
SETR = False
flag=True
while flag:
    if win32api.GetAsyncKeyState(0x39):#按9激活
        print('9pressed')
        AP=True
    if win32api.GetAsyncKeyState(0x31):#按1暂停
        print('1pressed')
        SETL=SETR=False
        AP=False
    if win32api.GetAsyncKeyState(0x30):#按0结束
        print('0pressed')

        AP=False
        flag = False
    
    #进行设置
    if win32api.GetAsyncKeyState(0x37):
        print('set left')
        SETL = True
        SETR = False
    if win32api.GetAsyncKeyState(0x38):
        print('set right')
        SETR = True
        SETL = False

    if SETL==True:
        j.data.wAxisX = int(0)
        j.data.wAxisY = int(0.5*32767)
        j.update()
        
    if SETR==True:
        j.data.wAxisX = int(1*32767)
        j.data.wAxisY = int(0.5*32767)
        j.update()
        
    
    if AP==True:
        target_window = gw.getWindowsWithTitle('American Truck Simulator')[0]  # Replace '目标窗口标题' with the actual title of the window
        #target_window = gw.getWindowsWithTitle('Euro Truck Simulator 2')[0]  # Replace '目标窗口标题' with the actual title of the window
        window_rect = (target_window.left, target_window.top, target_window.width, target_window.height)
    
        screenshot = pyautogui.screenshot()
        screenshot = screenshot.crop((window_rect[0]+11+50, window_rect[1]+39+220, window_rect[0] + window_rect[2]-11-50, window_rect[1] + window_rect[3]-11))
    
        # 将截图转换成OpenCV图像
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        img = cv2.resize(frame[80:,:],(256,256))

        FD_img = np.expand_dims(img, axis=0)

        #print(FD_img.shape)
        # 显示图像
        cv2.imshow('Screen Capture', img)
        steering_value=model.predict(FD_img)[0][0]
        print(int(steering_value*16384 +16384),steering_value)
        # 设置虚拟手柄的输入
        #set_joystick_axis(int(steering_value*32767), 0)
        j.data.wAxisX = int(steering_value * 16384 + 16384)
        j.data.wAxisY = int(0.5*32767)
        j.update()

    if AP==False and SETL==False and SETR==False:
        j.data.wAxisX = int(0.5*32767)
        j.data.wAxisY = int(0.5*32767)
        j.update()
    if cv2.waitKey(1) == ord('q'):
        flag = False
        break

cv2.destroyAllWindows()
