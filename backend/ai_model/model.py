import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing import image
import numpy as np

model = MobileNetV2(weights='imagenet')

def analyze_meal(image_path):
    img = image.load_img(image_path, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    preds = model.predict(x)
    decoded = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=1)[0][0]
    meal_name = decoded[1]
    calories = estimate_calories(meal_name)
    return {'name': meal_name, 'calories': calories}

def estimate_calories(meal_name):
    calorie_dict = {
        'pizza': 285,
        'sushi': 200,
        'burger': 354,
        'salad': 152,
        'pasta': 131
    }
    return calorie_dict.get(meal_name, 250)
