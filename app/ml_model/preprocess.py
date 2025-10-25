import cv2
import numpy as np
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

class ImagePreprocessor:
    def __init__(self, target_size=(224, 224)):
        self.target_size = target_size
    
    def preprocess_image(self, image_path):
        """Preprocess a single image for model prediction"""
        try:
            # Load image
            img = image.load_img(image_path, target_size=self.target_size)
            img_array = image.img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)
            return img_array
        except Exception as e:
            print(f"Error preprocessing image {image_path}: {e}")
            return None
    
    def preprocess_batch(self, image_paths):
        """Preprocess a batch of images"""
        processed_images = []
        valid_paths = []
        
        for path in image_paths:
            processed_img = self.preprocess_image(path)
            if processed_img is not None:
                processed_images.append(processed_img)
                valid_paths.append(path)
        
        if processed_images:
            return np.vstack(processed_images), valid_paths
        else:
            return None, []
    
    def enhance_image(self, image_path):
        """Enhance image quality using OpenCV"""
        try:
            # Read image
            img = cv2.imread(image_path)
            if img is None:
                return None
            
            # Convert to RGB
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Apply enhancement techniques
            # 1. Contrast Limited Adaptive Histogram Equalization
            lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
            lab[:,:,0] = cv2.createCLAHE(clipLimit=2.0).apply(lab[:,:,0])
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            
            # 2. Gaussian blur for noise reduction
            enhanced = cv2.GaussianBlur(enhanced, (3, 3), 0)
            
            return enhanced
        except Exception as e:
            print(f"Error enhancing image {image_path}: {e}")
            return None