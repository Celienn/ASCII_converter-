from tkinter import *
from PIL import Image, ImageTk
import cv2 as cv
from time import *
import vlc

width = 120
height = 30

sens = 0

canvas = Canvas(width=width, height=height, bg='white')
canvas.pack(expand=YES, fill=BOTH) 

cap = cv.VideoCapture('ressources/logtrain.mp4')
cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

fps = cap.get(cv.CAP_PROP_FPS)

test = vlc.MediaPlayer("ressources/lagtrain.mp4")
test.play()

def return_frame():
    _, frame = cap.read()
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    return img


def resize_image(file, resize=None):
    img = file
 
    if resize is not None:

        img = img.resize(resize, Image.ANTIALIAS)

    return img

def toBlackAndWhite(img) :
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if(item[3] != 0) :
            var = round(((item[0] + item[1] + item[2]) / (255*3))*255)
            newData.append((var,var,var,item[3]))
        else :
            newData.append(item)

    img.putdata(newData)
    return img

def toASCII(img) :
    img = img.convert("RGBA")
    datas = img.getdata()
    moyenne = 0
    text = ''
    #charlist =  r"B8&WM#YXQO{}[]()I1i!pao;:,.    "
    #charlist = r"@%§#?/):~°',."
    charlist = r"@%#?/):~°,."
    #charlist = r"111000 "
    newData = []
    tab = []

    for x in range(0,img.size[1]) :
        for y in range(0,img.size[0]) :
            text += charlist[int(((len(charlist)-1)*(img.getpixel((y,x))[0]))/256)]
        text += ""
    return text

if(cap.isOpened() and cap.read()) :
    image = return_frame()
    image = resize_image(image, resize=(width,height) )
    image = toBlackAndWhite(image)
    fichier = open("outputs/ASCII.txt","w+")
    fichier.write(toASCII(image))
    fichier.close()
    #print(toASCII(image))
    image = ImageTk.PhotoImage(image)
else : 
    print("fail")

content = ""

while cap.isOpened() and cap.read() :

    image = return_frame()
    image = resize_image(image, resize=(width,height) )
    image = toBlackAndWhite(image)
    fichier = open("outputs/ASCII.txt","w+")
    content = content + toASCII(image) + "#"
    fichier.write(content)
    #fichier.write(lastframe + "\n\n\n" + toASCII(image))
    fichier.close()
    #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(toASCII(image))
    #sleep(0.038)
    sleep(1/fps)



#mainloop()