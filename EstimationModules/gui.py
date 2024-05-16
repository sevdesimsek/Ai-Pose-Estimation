import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import PoseModule as pm
import time
import numpy as np
 
class TkinterApp:
    def __init__(self, window, window_title, background_image):
        self.window = window
        self.window.title(window_title)
        
        # Load the background image
        self.background_image = Image.open(background_image)
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        # Create a canvas that can fit the above video source size
        self.canvas = tk.Canvas(window, width=self.background_image.width, height=self.background_image.height)
        self.canvas.pack()

        # Display the background image
        self.canvas.create_image(0, 0, image=self.background_photo, anchor=tk.NW)
    
        
        # Button that lets the user to start video by selecting an image
        self.btn_start = tk.Button(window, text="Start", command=self.start_video, bg="brown", fg="black", font=("Arial", 12), height=1, width=10)
        self.btn_start.pack(anchor=tk.CENTER, expand=True, pady=5)

        # Button that lets the user to stop video
        self.btn_stop = tk.Button(window, text="Stop", command=self.stop_video, bg="lightcoral", fg="black", font=("Arial", 12), height=1, width=10)
        self.btn_stop.pack(anchor=tk.CENTER, expand=True, pady=5)

        self.detector = pm.poseDetector()
        self.vid = None
        self.delay = 15

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.vid = cv2.VideoCapture(file_path)
            self.update()
            
    def resize_image(self, frame, max_width, max_height):
        height, width, channels = frame.shape
        scaling_factor = min(max_width / width, max_height / height)
        new_width = int(width * scaling_factor)
        new_height = int(height * scaling_factor)
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_frame


    def start_video(self):
        self.load_image()

    def stop_video(self):
        if self.vid:
            self.vid.release()
    def update(self):
        # Get a frame from the video source
        if self.vid and self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                frame = self.detector.findPose(frame)
                frame = self.resize_image(frame, self.canvas.winfo_width(), self.canvas.winfo_height())
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                
                # Calculate position to center the image
                x_position = (self.canvas.winfo_width() - self.photo.width()) // 2
                y_position = (self.canvas.winfo_height() - self.photo.height()) // 2
                
                # Clear the canvas and remove the background image
                self.canvas.delete("all")  # Removes all items, including the background
                
                # Create image on the canvas
                self.canvas.create_image(x_position, y_position, image=self.photo, anchor=tk.NW, tags="bg_img")
        
        self.window.after(self.delay, self.update)



    def run(self):
        self.window.mainloop()

def main():
    root = tk.Tk()
    app = TkinterApp(root, "Yoga Pose Estimation", "Gui-Images/Healing.png")
    app.run()
    

if __name__ == '__main__':
    main()
