#!/usr/bin/env python
# coding: utf-8

# In[1]:


from keras.models import load_model
from time import sleep
from tensorflow.keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import webbrowser


# In[4]:


face_classifier = cv2.CascadeClassifier(r'C:\Users\namra\OneDrive\Desktop\final year project files\Emotion_Detection_CNN-main\Emotion_Detection_CNN-main\haarcascade_frontalface_default.xml')
classifier =load_model(r'C:\Users\namra\OneDrive\Desktop\final year project files\Emotion_Detection_CNN-main\Emotion_Detection_CNN-main\model.h5')

emotion_labels = ['Angry','Disgust','Fear','Happy','Neutral', 'Sad', 'Surprise']
negative_emo = ['Angry','Disgust','Fear', 'Sad']
positive_emo = ['Happy', 'Surprise']
counter=0
n_counter=0
cap = cv2.VideoCapture(0)



while True:
    _, frame = cap.read()
    labels = []
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)



        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            if label in negative_emo:
                counter+=1
                if(counter>10):
                    
                    url = "file://C:/Users/namra/OneDrive/Desktop/final year project files/FreeTheMind-main/FreeTheMind-main/practice.html"
                    webbrowser.open(url)
                    
                    cap.release()
                    cv2.destroyAllWindows()
            
            elif label == 'Neutral':
                n_counter+=1
                if(n_counter>20):
                    url = "file://C:/Users/namra/OneDrive/Desktop/final year project files/FreeTheMind-main/FreeTheMind-main/practice.html"
                    webbrowser.open(url)
                    
                    cap.release()
                    cv2.destroyAllWindows()
            
            elif label in positive_emo:
                counter-=1
                n_counter-=1
                
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


# In[ ]:




