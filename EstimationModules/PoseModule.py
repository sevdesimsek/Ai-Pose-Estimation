import cv2
import mediapipe as mp
import time
import math

class poseDetector():
    
    def __init__(self, mode= False, upBody = False, smooth= True,
                 detectionCon =0.5, trackCon=0.5):
        
        self.mode = mode #self.pbject it is the variable-part of that object
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.detectionConBool = detectionCon > 0.5
        self.trackConBool = trackCon > 0.5


        self.mpDraw= mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, self.upBody, self.smooth,  
                                     self.detectionConBool, self.trackConBool)
        
    
    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
        self.results = self.pose.process(imgRGB)            
        if self.results.pose_landmarks:
            if draw:  
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, 
                                        self.mpPose.POSE_CONNECTIONS)
        return img
            
            
    def findPosition(self, img, draw=True):
        #draw görünürlük flag i
        self.lmList = [] #yer işaretlerimiz için bir liste, nelere eklemek istiyarsan ekle
        if self.results.pose_landmarks:    #if the results are available  
            for id, lm in enumerate(self.results.pose_landmarks.landmark): 
                    h, w, c =img.shape 
                    # print(id, lm)
                    cx, cy =int(lm.x * w), int(lm.y * h)  
                    self.lmList.append([id, cx, cy]) #id x ve y değerini görmek istedim
                    if draw:
                        cv2.circle(img, (cx,cy), 18, (255,0,0), cv2.FILLED) 
        return self.lmList
    
    
    def findAngle(self, img, p1,p2,p3, draw=True): #three points landmarks 
        
        #Get the landmarks(üç noktayı belirliyoruz (x ve y değerlerinden)  )
        x1, y1 = self.lmList[p1][1:] #parçaladık, from p1 till the end, x ve y yi alıp idyi ignorelicak
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:] 
        
        #Calculate the anlge
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        
        #Bazen değer negatif oluyor o zaman:
        # angle = abs(angle)  # Mutlak değer al
        # if angle > 180:
        #     angle = 360 - angle
        
        if angle <0:
            angle+=360
            
        # print(angle)
        
        if draw:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,255),10)
            cv2.line(img,(x3,y3),(x2,y2),(0,255,255),10)
            
            cv2.circle(img, (x1,y1),30, (255,0,200), cv2.FILLED)
            cv2.circle(img, (x1,y1), 50, (255,0,200), 2)
            
            cv2.circle(img, (x2,y2),30, (255,0,200), cv2.FILLED)
            cv2.circle(img, (x2,y2), 50, (255,0,200), 2)
            
            cv2.circle(img, (x3,y3), 30, (255,0,200), cv2.FILLED)
            cv2.circle(img, (x3,y3), 50, (255,0,200), 2) 
            
            cv2.putText(img, str(int(angle)), (x2-350, y2+150),
                        cv2.FONT_HERSHEY_PLAIN,15,(255,0,0),15) #(x2-50, y2+50) sayının yeri 
        return angle


def main():
    cap = cv2.VideoCapture('PoseVideos/5.mov')
    pTime = 0
    detector = poseDetector()
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
    

if __name__ == "__main__":
    main()