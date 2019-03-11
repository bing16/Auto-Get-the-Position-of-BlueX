#-*-coding: utf-8-*-
import os
from PIL import Image
import time
import math

#dis1的基点为往北
#dis2的基点为往东1.03km
#dis3的基点为往南
#dis1,dis3作方位校准用

'''
#Y头像(熊本)像素点信息
objective = {
	"Point1":[[118, 890], (  1,   8,   2, 255)],
	"Point2":[[169, 854], (194,  28,  20, 255)],
	"Point3":[[ 61, 953], (110,  96,  67, 255)]
}
'''

#Y头像(人像)像素点信息
objective = {
	"Point1":[[ 118,  890], (148,  88,  86, 255)],
	"Point2":[[ 169,  854], (223, 223, 173, 255)],
	"Point3":[[  61,  953], (181, 168, 150, 255)]
}

#区域划分
position = {
	"time0":[ 908,  825],
	"time1":[ 888,  825],
	"dis0": [ 808,  825],
	"dis1": [ 788,  825],
	"dis2": [ 758,  825],
	"dis3": [ 738,  825],
	"dis0_just": [ 873,  825],
	"dis1_just": [ 853,  825],
	"dis2_just": [ 823,  825],
	"dis3_just": [ 803,  825],
	"dis0_longer": [ 788,  825],
	"dis1_longer": [ 768,  825],
	"dis2_longer": [ 738,  825],
	"dis3_longer": [ 718,  825],
	"dis0_1": [ 808,  597],
	"dis1_1": [ 788,  597],
	"dis2_1": [ 758,  597],
	"dis3_1": [ 738,  597],
	"dis0_1_just": [ 873,  597],
	"dis1_1_just": [ 853,  597],
	"dis2_1_just": [ 823,  597],
	"dis3_1_just": [ 803,  597],
	"dis0_1_longer": [ 788,  597],
	"dis1_1_longer": [ 768,  597],
	"dis2_1_longer": [ 738,  597],
	"dis3_1_longer": [ 718,  597]
}

just = {
	"Point1":[[ 967,  821], (165, 166, 178, 255)],
	"Point2":[[1030,  821], (165, 166, 178, 255)],
	"Point3":[[1003,  851], (165, 166, 178, 255)]
}

num = {
	"0":[[ 8,  9], (229, 229, 232, 255)],
	"1":[[ 1,  7], (165, 166, 178, 255)],
	"2":[[ 7, 24], (165, 166, 178, 255)],#(165, 166, 178, 255)(178, 179, 189, 255)
	"3":[[-8, 21], (194, 194, 202, 255)],
	"4":[[-2,  7], (165, 166, 178, 255)],
	"5":[[ 8, 20], (228, 228, 232, 255)],
	"6":[[-2,  4], (220, 220, 225, 255)],
	"7":[[-8,  0], (165, 166, 178, 255)],
	"8":[[-5, 15], (176, 176, 187, 255)],
	"9":[[-3, 14], (165, 166, 178, 255)],
	"None":[[1,0], (255, 255, 255, 255)]
}

word = {
	"min": [[931, 851], (165, 166, 178, 255)]
}

def if_objective():
	im = Image.open('tmp.png')
	pix = im.load()
	for key in objective:
		if(pix[objective[key][0][0],objective[key][0][1]] != objective[key][1]):
			return False
	return True

#返回上线时间
def online_time():
	im = Image.open('tmp.png')
	pix = im.load()
	time = 0
	if(pix[just["Point1"][0][0], just["Point1"][0][1]] == just["Point1"][1] and pix[just["Point2"][0][0], just["Point2"][0][1]] == just["Point2"][1] and pix[just["Point3"][0][0], just["Point3"][0][1]] == just["Point3"][1]):
		return 0
	elif(pix[word["min"][0][0], word["min"][0][1]] == word["min"][1]):
		if(pix[position["time1"][0] + num["None"][0][0], position["time1"][1] + num["None"][0][1]] != num["None"][1]):
			for key in num:
				if(pix[position["time1"][0] + num[key][0][0], position["time1"][1] + num[key][0][1]] == num[key][1]): 
					time += int(key)*10
					break
		for key in num:
			if(pix[position["time0"][0] + num[key][0][0], position["time0"][1] + num[key][0][1]] == num[key][1]): 
				time += int(key)
				return time
				break

	return -1

#返回原始位置的距离
def get_dis(i, onlinetime):
	dis = 0.0
	im = Image.open('tmp.png')
	pix = im.load()
	dd = ""
	if(onlinetime == 0):  #修正“刚刚”造成的的偏差
		dd = "_just"
	elif(onlinetime >= 10):
		dd = "_longer"
	if(i == 0):
		if(pix[position["dis3" + dd][0] + num["None"][0][0], position["dis3" + dd][1] + num["None"][0][1]] != num["None"][1]):
			for key in num:
				if(pix[position["dis3" + dd][0] + num[key][0][0], position["dis3" + dd][1] + num[key][0][1]] == num[key][1]): 
					dis += int(key)*10
					break
		for key in num:
			if(pix[position["dis2" + dd][0] + num[key][0][0], position["dis2" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)
				break
		for key in num:
			if(pix[position["dis1" + dd][0] + num[key][0][0], position["dis1" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)*0.1
				break
		for key in num:
			if(pix[position["dis0" + dd][0] + num[key][0][0], position["dis0" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)*0.01
				break
		return dis
	elif(i == 1):
		os.system("adb shell input tap 995 155")
		time.sleep(0.05)
		os.system("adb shell input tap 383 706")
		time.sleep(0.05)
		os.system("adb shell input swipe 542 460 542 1162")
		time.sleep(0.05)
		os.system("adb shell input swipe 542 460 542 1162")
		time.sleep(0.05)
		os.system("adb shell input tap 550 1892")
		time.sleep(0.5)
		message = os.popen('adb shell screencap -p > tmp.png').readlines()  #截图当前界面
		os.system("adb shell input tap 553 2095")
		time.sleep(0.05)
		os.system("adb shell input tap 553 2095")
		im = Image.open('tmp.png')
		pix = im.load()
	elif(i==2):
		os.system("adb shell input tap 995 155")
		time.sleep(0.05)
		os.system("adb shell input tap 383 706")
		time.sleep(0.05)
		os.system("adb shell input swipe 1000 1162 542 1162")
		time.sleep(0.05)
		os.system("adb shell input swipe 1000 1162 542 1162")
		time.sleep(0.05)
		os.system("adb shell input tap 550 1892")
		time.sleep(0.5)
		message = os.popen('adb shell screencap -p > tmp.png').readlines()  #截图当前界面
		os.system("adb shell input tap 553 2095")
		time.sleep(0.05)
		os.system("adb shell input tap 553 2095")
		im = Image.open('tmp.png')
		pix = im.load()

	elif(i==3):
		os.system("adb shell input tap 995 155")
		time.sleep(0.05)
		os.system("adb shell input tap 383 706")
		time.sleep(0.05)
		os.system("adb shell input swipe 551 1300 542 1162")
		time.sleep(0.05)
		os.system("adb shell input swipe 551 1300 542 1162")
		time.sleep(0.05)
		os.system("adb shell input tap 550 1892")
		time.sleep(0.5)
		message = os.popen('adb shell screencap -p > tmp.png').readlines()  #截图当前界面
		os.system("adb shell input tap 553 2095")
		time.sleep(0.05)
		os.system("adb shell input tap 553 2095")
		im = Image.open('tmp.png')
		pix = im.load()
	try:
		if(pix[position["dis3_1" + dd][0] + num["None"][0][0], position["dis3_1" + dd][1] + num["None"][0][1]] != num["None"][1]):
			for key in num:
				if(pix[position["dis3_1" + dd][0] + num[key][0][0], position["dis3_1" + dd][1] + num[key][0][1]] == num[key][1]): 
					dis += int(key)*10
					break
		for key in num:
			if(pix[position["dis2_1" + dd][0] + num[key][0][0], position["dis2_1" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)
				break
		for key in num:
			if(pix[position["dis1_1" + dd][0] + num[key][0][0], position["dis1_1" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)*0.1
				break
		for key in num:
			if(pix[position["dis0_1" + dd][0] + num[key][0][0], position["dis0_1" + dd][1] + num[key][0][1]] == num[key][1]): 
				dis += int(key)*0.01
				break
		return dis
	except:
		return (-1)

#刷新当前页面
def refresh():
	os.system("adb shell input swipe 534 830 534 1328")

#主函数
if __name__ == '__main__':
	print("Ready!")

	while(1):
		#print()
		tmp = input("Please enter \"1\" to continue: ")
		if(tmp == "1"):
			print("Try to connecte...")
			break

	while(1):
		message = os.popen('adb devices').readlines()  #读取连接的设备
		if(message[1] != "\n"):
			print("Connected!")
			break;

	last_dis0 = -100

	TIME_MSG = time.localtime(time.time())
	TIME = int(TIME_MSG[0]*1e8 + TIME_MSG[1]*1e6 + TIME_MSG[2]*1e4 + TIME_MSG[3]*1e2 + TIME_MSG[4])
	FILE = "log/"+str(TIME)+".txt"

	wrong_time = 0

	while(1):
		refresh()
		time.sleep(wrong_time + 3)
		message = os.popen('adb shell screencap -p > tmp.png').readlines()  #截图当前界面

		if(message == []):
			if(if_objective()):
				wrong_time = 0
				onlinetime = online_time()
				dis0 = get_dis(0, onlinetime)
				if(abs(dis0 - last_dis0) > 0.5):  #移动距离超过0.5km
					if(onlinetime >= 0):  #判断在5分钟内是否在线
						dis1 = get_dis(1, onlinetime)
						dis2 = get_dis(2, onlinetime)
						dis3 = get_dis(3, onlinetime)
						if(dis1 < 0 or dis2 < 0):
							continue
						TIME_MSG = time.localtime(time.time())
						TIME = int(TIME_MSG[0]*1e8 + TIME_MSG[1]*1e6 + TIME_MSG[2]*1e4 + TIME_MSG[3]*1e2 + TIME_MSG[4])
						alpha = math.acos((1.03*1.03+dis0*dis0-dis2*dis2)/2/1.03/dis0)/3.1415*180
						if(dis1 > dis3):
							alpha = -alpha
						f = open(FILE, "a")  #以追加方式打开文件
						f.write(str(TIME) + " %dmin_ago dis:%0.2f dir:%0.2f\n" % (onlinetime, dis0, alpha))  #存储当前信息
						f.close()
						last_dis0 = dis0  #更新上一次的dis0
						print("OK!")
						time.sleep(120)
				else:
					TIME_MSG = time.localtime(time.time())
					TIME = int(TIME_MSG[0]*1e8 + TIME_MSG[1]*1e6 + TIME_MSG[2]*1e4 + TIME_MSG[3]*1e2 + TIME_MSG[4])
					f = open(FILE, "a")  #以追加方式打开文件
					f.write(str(TIME) + " " + str(onlinetime) + "min_ago" + " same"\n)  #存储当前信息
					f.close()
					last_dis0 = dis0  #更新上一次的dis0
					print("OK!")
					time.sleep(120)
			else:
				print("Loss the target... "+str(5-wrong_time))
				wrong_time += 1
				if(wrong_time >= 5):
					break
				continue
		
