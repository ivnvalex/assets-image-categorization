import json
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet_v2 import preprocess_input

from params import *

model = load_model(model_path)

with open('data.json', 'r') as f:
    data = json.load(f)

cars = []
plants = []

for item in data['test_bundle']:
    file_path = item['file']
    file_name = file_path.split('/')[1]
    img = image.load_img(file_path, target_size=(img_width, img_height))
    arr = image.img_to_array(img)
    arr = preprocess_input(arr)
    tensor = arr[None, :, :, :]
    prediction = model.predict(tensor)
    score = np.max(prediction)
    label = labels[np.argmax(prediction)]
    if label == 'Cars':
        cars.append({'file': file_name, 'probability': score})
    elif label == 'Plants':
        plants.append({'file': file_name, 'probability': score})

print('Cars list:')
for car in cars:
    print(car)

print('Plants list:')
for plant in plants:
    print(plant)
