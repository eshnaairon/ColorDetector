import cv2
import numpy as np
import pandas as pd
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', required=True, help="Image Path")
args = vars(ap.parse_args())
img_path = args['image']

img = cv2.imread(img_path)
if img.shape[1]>900 or img.shape[0]>900:
   if img.shape[1]<img.shape[0]:
       scale_percent = 15
   else:
       scale_percent = 50

   width = int(img.shape[1] * scale_percent / 100)
   height = int(img.shape[0] * scale_percent / 100)
   dim = (width, height)
   img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

clicked = False
r = g = b = xpos = ypos = 0

index=["color","color_name","hex","R","G","B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

def getColorName(R,G,B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R- int(csv.loc[i,"R"])) + abs(G- int(csv.loc[i,"G"]))+ abs(B- int(csv.loc[i,"B"]))
        if(d<=minimum):
            minimum = d
            cname = csv.loc[i,"color_name"]
    return cname

def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b,g,r,xpos,ypos, clicked
        clicked = True
        xpos = x
        ypos = y
        b = int(img[y,x,0])
        g = int(img[y,x,1])
        r = int(img[y,x,2])
       
cv2.namedWindow('image')
cv2.setMouseCallback('image',draw_function)

while(1):
   
    cv2.imshow("image",img)
    if (clicked):
       
        cv2.rectangle(img,(20,20), (350,60), (b,g,r), -1)

        text = getColorName(r,g,b)
        
        cv2.putText(img, text,(50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)

        if(r+g+b>=600):
            cv2.putText(img, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
            
        clicked=False

    #Break the loop when user hits 'esc' key    
    if cv2.waitKey(20) & 0xFF ==27:
        break
    
cv2.destroyAllWindows()
