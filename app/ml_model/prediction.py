import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from config import Config

class WastePredictor:
    def __init__(self, model_path=None):
        self.model_path = model_path or Config.MODEL_PATH
        self.model = None
        self.load_model()
    
    def load_model(self):
        """Load the trained model"""
        try:
            if tf.io.gfile.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print("✅ Model loaded successfully")
                return True
            else:
                print("❌ Model file not found")
                return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False
    
    def preprocess_image(self, image_path):
        """Preprocess image for prediction"""
        try:
            img = image.load_img(image_path, target_size=Config.IMAGE_SIZE)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            return img_array
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path):
        """Make prediction on image"""
        if self.model is None:
            return None, 0.0
        
        processed_image = self.preprocess_image(image_path)
        if processed_image is None:
            return None, 0.0
        
        try:
            predictions = self.model.predict(processed_image)
            predicted_class = np.argmax(predictions[0])
            confidence = np.max(predictions[0])
            
            category = Config.WASTE_CATEGORIES.get(predicted_class, "Unknown")
            return category, float(confidence)
            
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return None, 0.0

# Global instance
waste_predictor = WastePredictor()