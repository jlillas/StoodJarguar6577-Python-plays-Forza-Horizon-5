import math
import cv2
import numpy as np
import vgamepad as vg
from PIL import ImageGrab

Debug = True

gamepad = vg.VX360Gamepad()

screengap = (50, 735)
screensize = (290+50, 219+735)
SkipPixel = 3

MapDirColor = (62, 237, 255)
Correction = 100
FoundCount = 0

TopX = 0
TopY = 0
TopX2 = 0
TopY2 = 0

font = cv2.FONT_HERSHEY_SIMPLEX

Throttle = 0

def clamp(Value, min, max):
    if Value > min and Value < max:
        return Value
    if Value < min and Value < max:
        return min
    if Value > min and Value > max:
        return max

while True:

    LowerColorRange = (MapDirColor[0] - round(Correction), MapDirColor[1] - round(Correction), MapDirColor[2] - round(Correction))
    UpperColorRange = (MapDirColor[0] + round(Correction), MapDirColor[1] + round(Correction), MapDirColor[2] + round(Correction))

    screen = np.array(ImageGrab.grab(bbox=(screengap[0], screengap[1], screensize[0], screensize[1])))


    for y in range(50, 150, SkipPixel):
        for x in range(95, 195, SkipPixel):
            if LowerColorRange[0] < screen[y, x, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x, 2] < UpperColorRange[2]:
                img = cv2.circle(screen, (x, y), 1, (255, 0, 0), 1)
                if TopX2 == 0:
                    TopX2 = x
                if TopY2 == 0:
                    TopY2 = y              
     

    # Trottle math
    Hypotinuse2 = math.hypot(TopX2 - 145, 145 - 185)
    Other2 = -145+TopX2
    Angle2 = 5 + round(-math.degrees(math.acos(Other2/Hypotinuse2)))+90


    # look for color
    for y in range(150, 200, SkipPixel):
        for x in range(95, 195, SkipPixel):

            if LowerColorRange[0] < screen[y, x, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x, 2] < UpperColorRange[2]:
                img = cv2.circle(screen, (x, y), 1, (255, 0, 0), 1)
                if TopX == 0:
                    TopX = x
                if TopY == 0:
                    TopY = y

                FoundCount += 1
            else:
                img = screen
    
    
    # auto correction
    if FoundCount < 5:
        Correction = Correction + 1 + FoundCount / 80
    if FoundCount > 30:
        Correction = Correction - 1 - FoundCount / 80


    #steering math
    Hypotinuse = math.hypot(TopX - 145, 145 - 185)
    Other = -145+TopX
    Angle = 2+round(-math.degrees(math.acos(Other/Hypotinuse))*1.2+90)

    # Throttle
    Throttle = abs(round(Hypotinuse2 - TopX2))
    if Throttle < 20:
        gamepad.left_trigger(value=150) # value between 0 and 255
        gamepad.right_trigger(value=0)
    if Throttle > 20:
        gamepad.right_trigger(value=abs(round(Hypotinuse2 - TopX2))) # value between 0 and 255

    # steering output
    if Angle > 0:
        gamepad.left_joystick(x_value=clamp(8000 + Angle * 1200, -32000, 32000), y_value=0) #values between -32768 and 32767
    if Angle < 0:
        gamepad.left_joystick(x_value=clamp(-8000 + Angle * 1200, -32000, 32000), y_value=0) #values between -32768 and 32767

    # debug
    if Debug == True:   
        cv2.putText(screen, 'TopX2: {}'.format(TopX2), (150, 10), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(screen, 'TopY2: {}'.format(TopY2), (150, 30), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(screen, 'Angle2: {}'.format(Angle2), (10, 50), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.putText(screen, 'Trt: {}'.format(Throttle), (10, 70), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        cv2.rectangle(screen, (95, 150), (195, 200), (255, 0, 0), 1)
        cv2.line(screen, (145, 185), (TopX, 150), (255, 0, 0), 1)
        cv2.line(screen, (145, 185), (145, 150), (0, 255, 0), 1)    
        cv2.line(screen, (145, 150), (TopX, 150), (0, 0, 255), 1)
        cv2.line(screen, (145, 150), (TopX2, TopY2), (255, 0, 0), 1)
        cv2.line(screen, (145, 150), (145, TopY2), (0, 255, 0), 1)    
        cv2.line(screen, (145, 150), (TopX2, TopY2), (0, 0, 255), 1) 
        cv2.rectangle(screen, (95, 50), (195, 200), (255, 0, 255), 1)


    # reset / updates
    TopX = 0
    TopY = 0
    TopX2 = 0
    TopY2 = 0

    FoundCount = 0

    gamepad.update()

    cv2.imshow("Map", screen)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

