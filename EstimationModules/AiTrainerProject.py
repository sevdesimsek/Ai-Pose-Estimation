import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture("AiTrainer/curls.mp4")

detector = pm.poseDetector()
count=0 #hareket sayısı
direction=0
pTime = 0
screen_width = 1920  # Örnek bir ekran genişliği
screen_height = 1080  # Örnek bir ekran yüksekliği


while True:
    success, img = cap.read()
    # img = cv2.imread("AiTrainer/testimg.jpg") #image için
    img= detector.findPose(img,False)
    lmList = detector.findPosition(img, False)
    # print(lmList)
    if len(lmList) !=0:
        
        # #Right arm
        # detector.findAngle(img,12,14,16)             
        # #Left arm
        angle = detector.findAngle(img,11,13,15)
        #not : uzuvların net görünmediği açılara güvenemezsin
        per = np.interp(angle, (210,300),(0,100)) 
        bar = np.interp(angle, (220,300), (650,100)) #bar değişkeni, kullanıcının performansına bağlı olarak değişir 
        #ve bu değişken np.interp fonksiyonu ile hesaplanır:
        # print(angle, per)
        
        #Check for the dumbbell curls
        color = (255,0,255)
        if per == 100:
            color = (0,255,0)
            if direction == 0:
                count += 0.5
                direction = 1
        if per == 0:
            color = (0,255,0)
            if direction == 1:
                count += 0.5
                direction = 0
                
        print(count)
        # cv2.putText(img, str(int(count)), (50,250),cv2.FONT_HERSHEY_PLAIN,15,
        #             (255,0,0),15 )
        
        
        #Draw bar
        cv2.rectangle(img, (1100,100), (1175,650), color, 3)
        cv2.rectangle(img, (1100, int(bar)), (1175,650), color, cv2.FILLED)
        cv2.putText(img, f'{int(per)} %', (1100,75), cv2.FONT_HERSHEY_PLAIN, 4,
                    color, 4) #yüzdelik dilimini yazar
         
        
        #Draw curl count
        cv2.rectangle(img,(0,450),(250,720),(0,255,0),cv2.FILLED)
        cv2.putText(img,str(int(count)),(45,670),cv2.FONT_HERSHEY_PLAIN,15,
                    (255,0,0),25)
         
         
    # screen_width = 800 
    # screen_height = 600
    # if img is not None:
    #     frame_width = img.shape[1]
    #     frame_height = img.shape[0]

    #     if frame_width > screen_width or frame_height > screen_height:
    #         scaling_factor = min(screen_width / frame_width, screen_height / frame_height)
    #         img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50,100),cv2.FONT_HERSHEY_PLAIN,5,
                    (255,0,0),5 )
         
    scaling_factor = min(screen_width / img.shape[1], screen_height / img.shape[0])
    img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    
    # Görüntüyü pencerenin ortasında yerleştir
    x_offset = int((screen_width - img.shape[1]) / 2)
    y_offset = int((screen_height - img.shape[0]) / 2)
    canvas = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    canvas[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
 
    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key != -1:
        break