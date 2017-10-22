#Project : Flying-Seal
#File	 : colours.py
#Author  : Remi Ratajczak
#Contact : Remi.Ratajczak@gmail.com

from random import randint

numberOfColors = 14

black   = (  0,  0,  0) #0
white   = (255,255,255) #1
red     = (255,  0,  0) #2
blue    = (  0,  0,255) #3
yellow  = (255,255,  0) #4
cyan    = (  0,255,255) #5
green   = (  0,128,  0) #6
purple  = (128,  0,128) #7
grey    = (128,128,128) #8
maroon  = (128,  0,  0) #9
pink    = (255,105,180) #10
silver  = (192,192,192) #11
brown   = (139, 69, 19) #12
skyblue = (  0,191,255) #13

def getRandColor():
    val = randint(0,numberOfColors-1)
    return getColor(val)

def getColor(val):
    if val == 0:
        return black
    if val == 1:
        return white
    if val == 2:
        return red
    if val == 3:
        return blue
    if val == 4:
        return yellow
    if val == 5:
        return cyan
    if val == 6:
        return green
    if val == 7:
        return purple
    if val == 8:
        return grey
    if val == 9:
        return maroon
    if val == 10:
        return pink
    if val == 11:
        return silver
    if val == 12:
        return brown
    if val == 13:
        return skyblue