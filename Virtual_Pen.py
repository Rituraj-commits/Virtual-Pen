import cv2

import numpy as np



cap=cv2.VideoCapture(0)


blank_image=None

x1,y1=0,0


while 1:

    flag,frame=cap.read()

    if blank_image is None:
        blank_image=np.zeros_like(frame)

    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)


    low=np.array([102,109,67])

    higher=np.array([128,255,255])

    mask=cv2.inRange(hsv,low,higher)
    mask=cv2.erode(mask,(5,5),iterations=2)
    mask = cv2.dilate(mask, (5, 5), iterations=2)


    res=cv2.bitwise_and(frame,frame,mask=mask)

    median_blur=cv2.medianBlur(res,ksize=5)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #print(max(contours,key=cv2.contourArea))

    if contours and cv2.contourArea(max(contours,key=cv2.contourArea))>600:

        c=max(contours,key=cv2.contourArea)

        x2,y2,w,h=cv2.boundingRect(c)

        cv2.rectangle(frame,(x2,y2),(x2+w,y2+h),(0,0,255),2)

        if x1==0 and y1==0:
            x1,y1=x2,y2

        else:
            blank_image=cv2.line(blank_image,(x1,y1),(x2,y2),(255,0,0),3)

        x1,y1=x2,y2
    else:
        x1,y1=0,0

    #cv2.add(frame,blank_image)

    #stacked=np.hstack((blank_image,frame))

    #cv2.imshow("Trackbars",cv2.resize(stacked,None,fx=0.6,fy=0.6))




    cv2.imshow("Image",frame)
    cv2.imshow("Blank_Image",blank_image)
    #cv2.imshow("Result",res)
    #cv2.imshow("Median_blur",median_blur)

    k=cv2.waitKey(1) & 0xFF

    if k==ord('c'):
        blank_image=None

    if k==27:
        break

cap.release()
cv2.destroyAllWindows()
