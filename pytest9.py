## function searchBluePerson
##スクリーンショットをとって指定の矩形から青の矩形領域を取得する


import pyautogui as gui
import pyperclip
import sys
import time
import cv2
import speech_recognition as sr

SAY_FLG_NONE = 1
SAY_FLG_CAMERA_UP = 2
SAY_FLG_CAMERA_DOWN = 3
SAY_FLG_CAMERA_LEFT = 4
SAY_FLG_CAMERA_LEFTUP = 5
SAY_FLG_CAMERA_LEFTDOWN = 6
SAY_FLG_CAMERA_RIGHT = 7
SAY_FLG_CAMERA_RIGHTUP = 8
SAY_FLG_CAMERA_RIGHTDOWN = 9
SAY_FLG_MOVE_NORTH = 10
SAY_FLG_MOVE_SOUTH = 11
SAY_FLG_MOVE_WEST = 12
SAY_FLG_MOVE_EAST = 13
SAY_FLG_MOVE_FORWARD = 14
SAY_FLG_MOVE_BACKWARD = 15

parse1_point = [86, 335]
parse2_point = [117,333]

mitorizu_lect = [399, 361, 1323, 498]

g_width = 320;
g_height = 240;

g_dw_c_x = 811
g_dw_c_y = 635

#カメラのサイズを適宜変更して処理速度を調整
g_width2 = 100;
g_height2 = 100;

out_img = cv2.imread("C:\\Users\81805\\Desktop\\python\\WalkingWithChats\\white.jpg");
out_img = cv2.resize(out_img, (g_width2, g_height2))


timeStart = 0
timeEnd = 0
spanTime = 0
g_chatLineX = 751;
g_chatLineY = 718;
g_consoleX = 282
g_consoleY = 120

args = sys.argv

print(len(sys.argv))

if len(args) < 4:
 exit()
 
#差分判定率
DiffJudgePercent = float(args[1])
g_chatLineX = int(args[2])
g_chatLineY = int(args[3])

# VideoCapture オブジェクトを取得します
g_capture = cv2.VideoCapture(0)

print(g_capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width2))
print(g_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height2)) 


ExecFlg = SAY_FLG_NONE;
PrevZahyoIdoFlg = False;


def calcWhiteRate(img1):

    global g_width2
    global g_height2
    
    WCount = 0
    
    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
             
             if ( img1[y, x, 0] == 255 and
                  img1[y, x, 1] == 255 and
                  img1[y, x, 2] == 255 ) :
                    WCount = WCount+1
    
    WRate = WCount / (g_width2 * g_height2)
    WRate = WRate * 100.0
    
    return WRate

def Diff(img1, img2):
    
    global g_width
    global g_height
    global out_img

    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
            if img1[y, x, 0] >= img2[y, x, 0]:
                out_img[y, x, 0] = abs(img1[y, x, 0] - img2[y, x, 0]);
            else:
                out_img[y, x, 0] = abs(img2[y, x, 0] - img1[y, x, 0]);

            if img1[y, x, 1] >= img2[y, x, 1]:
                out_img[y, x, 1] = abs(img1[y, x, 1] - img2[y, x, 1]);
            else:
                out_img[y, x, 1] = abs(img2[y, x, 1] - img1[y, x, 1]);

            if img1[y, x, 2] >= img2[y, x, 2]:
                out_img[y, x, 2] = abs(img1[y, x, 2] - img2[y, x, 2]);
            else:
                out_img[y, x, 2] = abs(img2[y, x, 2] - img1[y, x, 2]);

            absSum = int(out_img[y, x, 0]) + int(out_img[y, x, 1]) + int(out_img[y, x, 2])
            if absSum >= 120:
                    out_img[y, x, 0] = 255
                    out_img[y, x, 1] = 255
                    out_img[y, x, 2] = 255
            else:
                    out_img[y, x, 0] = 0
                    out_img[y, x, 1] = 0
                    out_img[y, x, 2] = 0
                    
    return out_img

    

def Play():

    global g_capture
    global g_width
    global g_height

    global out_img
    global WalkFlg
    global DiffJudgePercent
    
    global MatchCount
    global ExecFlg
    
    timeStart = 0.0
    timeEnd = 0.0
    spanTime = 0.0
    timeSpan = 0.1;

    StopCount = 0
    
    WalkFlg = False;

    print("Ctrl+Cを押して終了")    
    while True:


        ret, frame = g_capture.read()
        img1 = frame;

        cv2.imshow('frame', frame)
        
        str1 = cv2.waitKey(1)
                
            
        currentTime = time.time()
        if timeStart == 0:
            timeStart = time.time()
            timeEnd = time.time()
            img2 = img1
            
        else:
            timeEnd = time.time()
            
        timeDiff = timeEnd - timeStart
        
        if(timeDiff >= timeSpan):
            img3 = Diff(img1, img2)
            WRate = calcWhiteRate(img3)
            #print(WRate)
            if WRate >= DiffJudgePercent:
                StopCount = 0
                
                if WalkFlg == False:
                    print("散歩を開始しました")
                    gui.click(g_chatLineX, g_chatLineY)
                    gui.click(g_chatLineX, g_chatLineY)
                    pyperclip.copy("散歩を開始しました")
                    gui.hotkey('ctrl','v')
                    gui.press('enter')
                    gui.click(g_consoleX, g_consoleY)
                    
                WalkFlg = True
                #print("walkFlg:True");
                
            else:
                if StopCount >= 10:
                    if WalkFlg == True:
                        print("休憩中です")
                        gui.click(g_chatLineX, g_chatLineY)
                        gui.click(g_chatLineX, g_chatLineY)
                        pyperclip.copy("休憩中です")
                        gui.hotkey('ctrl','v')
                        gui.press('enter')
                        gui.click(g_consoleX, g_consoleY)
                        
                        
                    WalkFlg = False
                    StopCount = 0
                else:
                    StopCount = StopCount + 1
                    
                #print("walkFlg:False")

            timeStart = currentTime
       
        img2 = img1
    
    g_capture.release()

    cv2.destroyAllWindows()
    
    return

def execute(ExecFlg):

    if SAY_FLG_NONE == ExecFlg:
        return
    elif SAY_FLG_CAMERA_UP == ExecFlg:
        CameraMoveUp()
        
    elif SAY_FLG_CAMERA_DOWN == ExecFlg:
        CameraMoveDown()
        
    elif SAY_FLG_CAMERA_LEFT == ExecFlg: 
        CameraMoveLeft()
        
    elif SAY_FLG_CAMERA_LEFTUP == ExecFlg:
        CameraMoveLeftUp()
        
    elif SAY_FLG_CAMERA_LEFTDOWN == ExecFlg:
        CameraMoveLeftDown()
        
    elif SAY_FLG_CAMERA_RIGHT == ExecFlg:
        CameraMoveRight()
        
    elif SAY_FLG_CAMERA_RIGHTUP == ExecFlg:
        CameraMoveRightUp()
        
    elif SAY_FLG_CAMERA_RIGHTDOWN == ExecFlg:
        CameraMoveRightDown()
        
    elif SAY_FLG_MOVE_NORTH == ExecFlg:
        ZahyoMoveNorth()
        
    elif SAY_FLG_MOVE_SOUTH == ExecFlg:
        ZahyoMoveSouth()
        
    elif SAY_FLG_MOVE_WEST == ExecFlg:
        ZahyoMoveWest()
        
    elif SAY_FLG_MOVE_EAST == ExecFlg:
        ZahyoMoveEast()
        
    elif SAY_FLG_MOVE_FORWARD == ExecFlg:
        ZahyoMoveForward()
        
    elif SAY_FLG_MOVE_BACKWARD == ExecFlg:
        ZahyoMoveBackward()
        
    return

def main(): 

    Play()


    return 0
   

    
        
main()

    