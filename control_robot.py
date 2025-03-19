import cv2
import numpy as np
from keras.models import load_model
import serial
import time

model = load_model('object_detection_model.h5')  

classes = ['vat1', 'vat2', 'vat3', 'no items']  

# chuẩn bị đầu vào cho mô hình
def preprocess_image(image):
    resized_img = cv2.resize(image, (64, 64))  # Resize ảnh về kích thước mà mô hình yêu cầu
    processed_img = resized_img.astype('float32') / 255.0
    processed_img = np.expand_dims(processed_img, axis=0)
    return processed_img


cap = cv2.VideoCapture(0)  
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 

ser = serial.Serial('COM3', 9600)  

detected_objects = set()  

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    if not detected_objects:
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        
        processed_frame = preprocess_image(frame)
        predictions = model.predict(processed_frame)
        predicted_class = np.argmax(predictions)
        predicted_label = classes[predicted_class]

        
        if len(faces) == 0 or (predicted_label == 'no items' and np.max(predictions) < 0.5):
            cv2.putText(frame, 'No items ', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            text = f'Predicted class: {predicted_label}'
            cv2.putText(frame, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Lưu trữ các vật thể đã nhận diện
            detected_objects.add(predicted_label)

            if predicted_label == 'vat1':
                ser.write(b'vat1_command')
            elif predicted_label == 'vat2':
                ser.write(b'vat2_command')
            else :
                ser.write(b'vat3_command')
    
    else:
        
        time.sleep(2)
        detected_objects.clear()  

    
    cv2.imshow('Object Detection', frame)

    
    if len(faces) == 0 or (predicted_label == 'no items' and np.max(predictions) < 0.5):
        print('No items ')
    else:
        print(f'Predicted class: {predicted_label}')
        for i, prob in enumerate(predictions[0]):
            print(f'{classes[i]}: {prob:.2f}')  

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    

cap.release()
cv2.destroyAllWindows()
ser.close()
