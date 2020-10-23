from PIL import ImageTk,Image
import tkinter as tk
import cv2
from numpy import *
from tkinter import ttk
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'


class App:
    def __init__(self, win, mode):
        # initializing needed
        self.img = None  # to store the image in a variable
        self.img1 = None
        self.img2 = None
        self.option = None
        # creating window
        self.win = win
        self.win = tk.Tk()
        self.win.title("Video_Processing")
        self.win.geometry('640x560')

        # setting mode of capture and turning on video
        self.mode = mode
        self.video_on = cv2.VideoCapture(self.mode)
        # creating button to convert

        self.button = tk.Button(self.win, text='convert', command=lambda: self.get_conv_mode())
        self.button.grid(row=2)

        # creating label at top
        self.label = tk.Label(self.win, text='Video Live', height=1)
        self.label.grid(row=0, column=0)
        self.label5 = tk.Label(self.win, text='Processed Video', height=1)
        self.label5.grid(row=0, column=1)
        self.label4 = tk.Label(self.win)
        self.label4.grid(row=3, columnspan=2)

        # creating labels for displaying video
        self.label3 = tk.Label(self.win)
        self.label3.grid(row=1, column=1)
        try:
            self.no_vid_img = cv2.resize(cv2.imread('no_video.jpg'), (600, 480))
            self.no_vid_img = ImageTk.PhotoImage(Image.fromarray(self.no_vid_img[:, 100:400]))
        except:
            self.no_vid_img = None
        self.label3.configure(image=self.no_vid_img)
        self.label2 = tk.Label(self.win)
        self.label2.grid(row=1, column=0, padx=10)

        # looping video using update_label method
        self.delay = 2
        self.update_label()

        # creating drop down
        self.n = tk.StringVar()
        self.drop_down = ttk.Combobox(self.win, width=10, textvariable=self.n)
        self.drop_down['values'] = (' No', ' Gray_scale', ' OCR', ' BGR', ' Face_identification')
        self.drop_down.grid(row=2, column=1)
        self.drop_down.current(0)

        # app's mainloop
        self.win.mainloop()

    def get_conv_mode(self,*string):
        self.option = self.drop_down.get()
        if string is None:
            self.label4.configure(text=self.option)
        else:
            self.label4.configure(text=string)

    def update_label(self):
        self.img = self.get_frame()
        self.img1 = self.no_effect(self.img)
        if self.option == ' Gray_scale':
            self.img2 = self.gray_scale(self.img)
        elif self.option == ' No':
            self.img2 = self.no_effect(self.img)
        elif self.option == ' OCR':
            try:
                pytesseract.pytesseract.get_tesseract_version()
            except:
                self.img2 = self.no_vid_img
                self.get_conv_mode('Install the tesseract OCR on your computer')
            else:
                self.img2 = self.ocr(self.img)
        elif self.option == ' BGR':
            self.img2 = self.BGR(self.img)
        elif self.option == ' Face_identification':
            self.img2 = self.face_iden(self.img)
        self.label2.configure(image=self.img1)
        self.label3.configure(image=self.img2)
        self.win.after(self.delay, self.update_label)

    def update_label_gray(self):
        self.img = self.get_frame()
        self.img1 = self.no_effect(self.img)
        self.img2 = self.gray_scale(self.img)
        self.label2.configure(image=self.img1)
        self.label3.configure(image=self.img2)
        self.win.after(self.delay, self.update_label)

    def get_frame(self):
        check, frame = self.video_on.read()
        frame = cv2.resize(frame, (600, 480))
        frame = frame[:, 100:400]
        return frame

    @staticmethod
    def no_effect(frame):
        color_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(color_img)
        imgtk = ImageTk.PhotoImage(img)
        return imgtk

    @staticmethod
    def BGR(frame):
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(img)
        return imgtk

    @staticmethod
    def gray_scale(frame):
        color_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = Image.fromarray(color_img)
        imgtk = ImageTk.PhotoImage(img)
        return imgtk

    def ocr(self,image):
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ximg, yimg = image_gray.shape
        i = pytesseract.image_to_boxes(image_gray)
        string = pytesseract.image_to_string(image_gray)
        self.get_conv_mode(string)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        for j in i.splitlines():
            j = j.split(' ')
            x = int(j[1])
            y = int(j[2])
            w = int(j[3])
            h = int(j[4])
            t = str(j[0])
            cv2.rectangle(image, (x, ximg-h), (w, ximg-y), (255, 0, 0), 1)
            cv2.putText(image, t, (x, ximg-y+20), cv2.QT_FONT_NORMAL, 1, (255, 0, 0), 1)
        imgtk = ImageTk.PhotoImage(Image.fromarray(image))
        return imgtk

    @staticmethod
    def face_iden(frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_detect = cv2.CascadeClassifier(r'C:\Users\DELL\PycharmProjects\hello\venv\Lib\site-packages\cv2\data\haarcascade_frontalface_default.xml')
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        box = face_detect.detectMultiScale(frame_gray, minNeighbors=3)
        for x,y,w,h in box:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 1)
        imgtk = ImageTk.PhotoImage(Image.fromarray(frame))
        return imgtk


App('vid', 0)

















