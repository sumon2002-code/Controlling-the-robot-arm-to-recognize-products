
import os
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

data_dir = 'E:/IOT/nhandiendo/Train'
 
classes = ['vat1', 'vat2', 'vat3']

data = []
labels = []

# Đọc dữ liệu từ thư mục
for idx, category in enumerate(classes):
    folder_path = os.path.join(data_dir, category)
    img_list = os.listdir(folder_path)
    
    for img in img_list:
        img_path = os.path.join(folder_path, img)
        image = cv2.imread(img_path)
        image = cv2.resize(image, (64, 64)) 
        data.append(image)
        labels.append(idx)

# Chuyển đổi danh sách thành mảng numpy
data = np.array(data)
labels = np.array(labels)

# Chuẩn hóa dữ liệu
data = data.astype('float32') / 255.0

# Chia dữ liệu thành tập train và tập validation
X_train, X_val, y_train, y_val = train_test_split(data, labels, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(len(classes), activation='softmax'))  


model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_val, y_val))


model.save('object_detection_model.h5')
