from tkinter import Label,Tk,Canvas,Button
import cv2
import os
import threading
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
from tensorflow import keras
import time


global inactive_color
global active_color
inactive_color="#53555E"
active_color="#3A7530"

class App:
    def __init__(self,vs,model):
        self.vs=vs
        self.model=model
        self.frame=None
        self.thread=None
        self.stopEvent=None

        self.root=Tk()
        self.root.configure(bg = "#181a17")
        canvas = Canvas(
        self.root,
        bg = "#181a17",
        height = 770,
        width = 1440,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge")
        canvas.place(x = 0, y = 0)
        canvas.pack()
        self.panel=None
        self.confidence_text=None
        self.c0_lb=None
        self.c1_lb=None
        self.c2_lb=None
        self.c3_lb=None
        self.c4_lb=None
        self.c5_lb=None
        self.c6_lb=None
        self.c7_lb=None
        self.c8_lb=None
        self.c9_lb=None
        btn =Button(self.root, text="Stop",command=self.onClose,bg="#ff0000",fg="#ffffff",font = ("Roboto-Medium", int(17.0)))
        btn.place(x = 315, y = 581, width = 170,height = 50)
        self.stopEvent=threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_title("distracted driver")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)

    def onClose(self):
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        print("[INFO] closing...")
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                success,self.frame=vs.read()
                if success:
                    self.frame=cv2.flip(self.frame,1)
                    cv2image= cv2.cvtColor((self.frame),cv2.COLOR_BGR2RGB)
                    image = Image.fromarray(cv2image)
                    image = ImageTk.PhotoImage(image)
                    model_input=cv2.resize((self.frame), dsize=(224,224))
                    pred=model.predict(np.array([model_input]).reshape(-1,224,224,3))
                    class_pred=np.argmax(pred[0])
                    print("class pred:",class_pred)
                    confidence=(pred[0][class_pred])*100

                    if self.panel==None or self.confidence_text==None or self.c0_lb==None or self.c1_lb==None or self.c2_lb==None or self.c3_lb==None or self.c4_lb==None or self.c5_lb==None or self.c6_lb==None or self.c7_lb==None or self.c8_lb==None or self.c9_lb==None:
                        self.panel=Label(self.root,image=image,height=436,width=730)
                        self.panel.image=image
                        self.panel.place(x=40,y=91)

                        self.confidence_text=Label(self.root,text = f"confidence:{confidence}",font = ("Roboto-Medium", int(24.0)),bg="#181a17",fg='#ffff00')
                        self.confidence_text.text=f"confidence:{confidence}"
                        self.confidence_text.place(x=40,y=21)

                        self.c0_lb=Label(self.root,text = "c0: normal driving",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c0_lb.bg=inactive_color
                        self.c0_lb.place(x=795,y=21)

                        self.c1_lb=Label(self.root,text = "c1: texting-left",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c1_lb.bg=inactive_color
                        self.c1_lb.place(x=795,y=91)

                        self.c2_lb=Label(self.root,text = "c2: talking on phone-left",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c2_lb.bg=inactive_color
                        self.c2_lb.place(x=795,y=161)

                        self.c3_lb=Label(self.root,text = "c3: texting-right",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c3_lb.bg=inactive_color
                        self.c3_lb.place(x=795,y=231)

                        self.c4_lb=Label(self.root,text = "c4: talking on phone-right",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c4_lb.bg=inactive_color
                        self.c4_lb.place(x=795,y=301)

                        self.c5_lb=Label(self.root,text = "c5: operating on radio",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c5_lb.bg=inactive_color
                        self.c5_lb.place(x=795,y=371)

                        self.c6_lb=Label(self.root,text = "c6: drinking",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c6_lb.bg=inactive_color
                        self.c6_lb.place(x=795,y=441)

                        self.c7_lb=Label(self.root,text = "c7: reaching behind",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c7_lb.bg=inactive_color
                        self.c7_lb.place(x=795,y=511)

                        self.c8_lb=Label(self.root,text = "c8: hair and makeup",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c8_lb.bg=inactive_color
                        self.c8_lb.place(x=795,y=581)

                        self.c9_lb=Label(self.root,text = "c9: talkin to passenger",font = ("Roboto-Medium", int(17.0)),bg=inactive_color,height=2,width=43)
                        self.c9_lb.bg=inactive_color
                        self.c9_lb.place(x=795,y=651)

                    else:
                        self.panel.configure(image=image)
                        self.panel.image=image

                        self.confidence_text.configure(text=f"confidence:{confidence:.2f}%")
                        self.confidence_text.text=f"confidence:{confidence:.2f}%"

                        if class_pred==0:
                            self.c0_lb.configure(bg=active_color)
                            self.c0_lb.bg=active_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==1:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=active_color)
                            self.c1_lb.bg=active_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==2:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=active_color)
                            self.c2_lb.bg=active_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==3:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=active_color)
                            self.c3_lb.bg=active_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==4:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=active_color)
                            self.c4_lb.bg=active_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==5:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=active_color)
                            self.c5_lb.bg=active_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==6:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=active_color)
                            self.c6_lb.bg=active_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==7:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=active_color)
                            self.c7_lb.bg=active_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==8:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=active_color)
                            self.c8_lb.bg=active_color
                            self.c9_lb.configure(bg=inactive_color)
                            self.c9_lb.bg=inactive_color

                        elif class_pred==9:
                            self.c0_lb.configure(bg=inactive_color)
                            self.c0_lb.bg=inactive_color
                            self.c1_lb.configure(bg=inactive_color)
                            self.c1_lb.bg=inactive_color
                            self.c2_lb.configure(bg=inactive_color)
                            self.c2_lb.bg=inactive_color
                            self.c3_lb.configure(bg=inactive_color)
                            self.c3_lb.bg=inactive_color
                            self.c4_lb.configure(bg=inactive_color)
                            self.c4_lb.bg=inactive_color
                            self.c5_lb.configure(bg=inactive_color)
                            self.c5_lb.bg=inactive_color
                            self.c6_lb.configure(bg=inactive_color)
                            self.c6_lb.bg=inactive_color
                            self.c7_lb.configure(bg=inactive_color)
                            self.c7_lb.bg=inactive_color
                            self.c8_lb.configure(bg=inactive_color)
                            self.c8_lb.bg=inactive_color
                            self.c9_lb.configure(bg=active_color)
                            self.c9_lb.bg=active_color

        except RuntimeError:
            print("[INFO] caught a RuntimeError")


if __name__=="__main__":
    print("loading model...")
    parent_path= os.path.abspath(os.pardir) #path of parent directory
    mobile_net_path=os.path.join(parent_path,"mobilenet")
    model = keras.models.load_model(mobile_net_path+"\\mobilenet_base_sgd.hdf5")
    print("model loaded")

    print("reading video...")
    vs=cv2.VideoCapture("input_video.mp4")
    print("video read complete")
    time.sleep(2.0)
    app=App(vs,model)
    app.root.mainloop()