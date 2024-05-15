import cv2
import mediapipe as mp
import time

 #işlemci üzerinde cpu calışıyor yani bunu çalıştımak için gpu grafik
 #işlemci kullanmıyor


mpDraw= mp.solutions.drawing_utils
mpPose = mp.solutions.pose
pose = mpPose.Pose()




cap = cv2.VideoCapture('PoseVideos/5.mov')

pTime = 0
# Video çerçevesinin genişliği ve yüksekliği
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while True:
    success, img = cap.read() #burdaki img gbr 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #ama mediapipe frameworkü rgb kullanıyor
   #uyumlu hale getirmek için dönüştürdük
    results = pose.process(imgRGB)
    print(results.pose_landmarks) #were getting actual landmarks
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark): #landmark koordinatlarını print ediyoruz ama hangi landmark hangi numaraya ait bilmiyoruz o yüzden bu for döngsünü yaratıyoruz
            h, w, c =img.shape #h görüntünün yükseklik, w görüntünün genişliği
            print(id, lm)
            cx, cy =int(lm.x * w), int(lm.y * h)  
            cv2.circle(img, (cx,cy), 12, (255,0,0), cv2.FILLED) #noktaları blue yaptık ve doğtu pixel valuelara yerleştirdik
    #GBR (Blue-Green-Red) ve RGB (Red-Green-Blue), 
    #kodlama sisteminde, bir pikselin rengini belirlemek için
    # renkleri temsil etmek için kullanılan iki 
    # farklı renk kodlama sistemidir. Bunlar, dijital 
    # görüntülerde ve renkli ekranlarda renkleri tanımlamak 
    # için kullanılır. 
    # İşlevsel olarak aynıdırlar, 
    # ancak sıralamaları farklıdır.
    
    
    # Ekranın genişliği ve yüksekliğini al
    screen_width = 800
    screen_height = 600

    # Eğer video ekran boyutundan büyükse, ekran boyutuna göre boyutlandır
    if frame_width > screen_width or frame_height > screen_height:
        scaling_factor = min(screen_width / frame_width, screen_height / frame_height)
        img = cv2.resize(img, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)

    
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    
    cv2.putText(img, str(int(fps)), (70,50), cv2.FONT_HERSHEY_PLAIN, 3,
                                            (255, 255, 255,), 3 )
    cv2.imshow("Image", img)

    # Bekleme süresi 1ms olarak ayarlandı.
    cv2.waitKey(1) 
        


