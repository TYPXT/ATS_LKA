# ATS_LKA
基于CNN的美国卡车模拟车道保持小程序

使用一个摇杆收集训练数据，并将其送入CNN训练，然后再把模型计算结果输入游戏，过程就是如此简单（所以性能可能很差）

## 环境说明
python 3.10.4

OpenCV 4.5.5

tensorflow 2.10.0

pygame 2.1.2

pywin32 304

pyvjoy 1.0.1

PyGetWindow 0.0.9


## 使用说明
没有摇杆（建议最好有一个，不加以控制只能天天修车了）：

在detect.py中选择模型路径，项目中提供了一个由5391幅游戏画面和对应的摇杆输出通过正常驾驶车辆训练的模型，打开你的美国卡车模拟，进入画面设置，改为非全屏模式，设置分辨率为1280$\times$720。
再进入控制设置，选择操控设备为“键盘+vjoy”，此时启动detect.py，再设定方向控制轴，按下“7”或“8”使轴偏向最左边或最右边，设定结束后记得按下“1”键暂时停止控制，不然你将无法移动你的鼠标。

设置完毕后可进入游戏驾驶页面，按下“9”键启动LKA，随后切换到视角6（游戏默认按大键盘数字“6”进入），现在可以开动了，记得按下“1”暂时停止LKA的操控。

有摇杆，愿意自制数据集：
在拍摄.py中修改自己的摇杆输入端口（第12行），一般是0，1，2这些值，启动程序，直至按下13键会终止程序（如果没有13键可自己改为其他的按钮）。
在游戏的驾驶页面，打开视角6（车头视角），按下6键盘预备拍摄，此时按下摇杆上的0号按钮即可正常记录，松开回到预备拍摄状态，注意程序只会在摇杆有动作（线性轴有运动或者按钮被按下、放开）时才会记录数据。
经过一段时间的驾驶，你将会获得可被用来训练的画面和摇杆输出。

在Test.ipynb中载入数据集，在cell 7-15中训练你自己的模型并保存，随后的步骤同上“没有摇杆”部分

## ToDo
1.提升性能

2.增加ACC

