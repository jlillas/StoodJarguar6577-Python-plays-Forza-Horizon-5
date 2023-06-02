import math
import cv2
import numpy as np
import vgamepad as vg
from PIL import ImageGrab

gamepad = vg.VX360Gamepad()

ScreenGap = (50, 735)
Screensize = (340, 219+735)
SkipPixel = 3

GotoDirColor = (62, 237, 255)
Correction = 100
FoundCount = 0

TopX = 0
TopY = 0

font = cv2.FONT_HERSHEY_SIMPLEX

while True:

    LowerColorRange = (GotoDirColor[0] - round(Correction), GotoDirColor[1] - round(Correction), GotoDirColor[2] - round(Correction))
    UpperColorRange = (GotoDirColor[0] + round(Correction), GotoDirColor[1] + round(Correction), GotoDirColor[2] + round(Correction))

    screen = np.array(ImageGrab.grab(bbox=(ScreenGap[0], ScreenGap[1], Screensize[0], Screensize[1])))

    for y in range(150, 200, SkipPixel):
        for x in range(95, 195, SkipPixel):

            if LowerColorRange[0] < screen[y, x, 0] < UpperColorRange[0] and LowerColorRange[1] < screen[y, x, 1] < UpperColorRange[1] and LowerColorRange[2] < screen[y, x, 2] < UpperColorRange[2]:

                img = cv2.circle(screen, (x, y), 1, (255, 0, 0), 1)
                if TopX == 0 and TopY == 0:
                    if x > 145:
                        TopX = x
                    if x < 145:
                        TopX = x                        
                    TopY = y                        

                FoundCount += 1
            else:
                img = screen
    
    if FoundCount < 5:
        Correction = Correction + 1 + FoundCount / 80
    if FoundCount > 30:
        Correction = Correction - 1 - FoundCount / 80    

    cv2.rectangle(img, (95, 150), (195, 200), (255, 0, 0), 1)

    cv2.line(img, (145, 185), (TopX, 150), (255, 0, 0), 1)
    cv2.line(img, (145, 185), (145, 150), (0, 255, 0), 1)
    cv2.line(img, (145, 185), (TopX, 150), (0, 0, 255), 1)

    Hypotinuse = math.hypot(TopX - 145, 145 - 185)
    Other = -145+TopX
    Angle = 5+round(-math.degrees(math.acos(Other/Hypotinuse))+90)

    if Angle > 0:
        gamepad.left_joystick(x_value=8000+Angle*500 ,y_value=0) #values between -32768 and 32767
    if Angle > 0:
        gamepad.left_joystick(x_value=-8000 + Angle * 500 ,y_value=0) #values between -32768 and 32767

    cv2.putText(img, 'Hypo: {}'.format(Hypotinuse), (10, 50), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'TopX: {}'.format(-145+TopX), (10, 70), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(img, 'Angle: {}'.format(Angle), (10, 100), font, 0.5, (0, 255, 0), 1, cv2.LINE_AA)

    TopX = 0
    TopY = 0

    FoundCount = 0

    gamepad.update()

    cv2.imshow("Map", img)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break