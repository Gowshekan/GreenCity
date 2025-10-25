import tensorflow as tf
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
import cv2
import os
from config import Config

class WasteClassifier:
    def __init__(self):
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if os.path.exists(Config.MODEL_PATH):
                self.model = load_model(Config.MODEL_PATH)
                print("✅ Model loaded successfully")
            else:
                print("❌ Model file not found")
                self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, img_path):
        """Preprocess the image for model prediction"""
        img = image.load_img(img_path, target_size=Config.IMAGE_SIZE)
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        return img_array
    
    def predict(self, img_path):
        """Predict waste category from image"""
        try:
            if self.model is None:
                return "Model not loaded", 0.0
            
            # Preprocess image
            processed_img = self.preprocess_image(img_path)
            
            # Make prediction
            predictions = self.model.predict(processed_img, verbose=0)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            category = Config.WASTE_CATEGORIES[predicted_class]
            
            return category, confidence
            
        except Exception as e:
            print(f"Prediction error: {e}")
            return "Unknown", 0.0

# Global model instance
waste_classifier = WasteClassifier()