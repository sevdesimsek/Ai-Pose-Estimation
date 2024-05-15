import cv2
import time
import PoseModule as pm
#modülümüzü importladık, ve aynı dosyada olmaları gerekir



cap = cv2.VideoCapture('PoseVideos/4.mp4')
pTime = 0
detector = pm.poseDetector()
while True:
    success, img = cap.read() 
    img = detector.findPose(img)
    lmList = detector.findPosition(img, draw = False)
    if len(lmList) !=0:
        print(lmList[14])
        cv2.circle(img, (lmList[14][1], lmList[14][2]), 17, (0,0,255), cv2.FILLED) #exatly istediğimiz noktaları belirginleştirdik

        
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    screen_width = 800
    screen_height = 600
    if frame_width > screen_width or frame_height > screen_height:
        scaling_factor = min(screen_width / frame_width, screen_height / frame_height)
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

            
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3,
                                        (255, 255, 255,), 3 )
    cv2.imshow("Image", img)
    
    key = cv2.waitKey(1)
    if key != -1:
        break
