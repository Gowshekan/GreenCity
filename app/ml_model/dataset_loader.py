import os
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf

class TrashNetLoader:
    def __init__(self, dataset_path, image_size=(224, 224)):
        self.dataset_path = dataset_path
        self.image_size = image_size
        self.classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
        self.class_indices = {cls: idx for idx, cls in enumerate(self.classes)}
    
    def load_dataset(self, validation_split=0.2, batch_size=32):
        """Load and preprocess the TrashNet dataset"""
        
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest',
            validation_split=validation_split
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(
            rescale=1./255,
            validation_split=validation_split
        )
        
        # Create data generators
        train_generator = train_datagen.flow_from_directory(
            self.dataset_path,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='training',
            shuffle=True
        )
        
        val_generator = val_datagen.flow_from_directory(
            self.dataset_path,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical',
            subset='validation',
            shuffle=False
        )
        
        return train_generator, val_generator
    
    def get_class_distribution(self):
        """Get the distribution of classes in the dataset"""
        class_counts = {}
        
        for class_name in self.classes:
            class_path = os.path.join(self.dataset_path, class_name)
            if os.path.exists(class_path):
                num_images = len([f for f in os.listdir(class_path) 
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                class_counts[class_name] = num_images
        
        return class_counts
    
    def analyze_dataset(self):
        """Analyze the dataset and print statistics"""
        print("Dataset Analysis:")
        print(f"Dataset path: {self.dataset_path}")
        print(f"Classes: {self.classes}")
        
        class_counts = self.get_class_distribution()
        total_images = sum(class_counts.values())
        
        print("\nClass Distribution:")
        for class_name, count in class_counts.items():
            percentage = (count / total_images) * 100
            print(f"  {class_name}: {count} images ({percentage:.1f}%)")
        
        print(f"\nTotal images: {total_images}")
        
        return class_counts, total_images

# Example usage
if __name__ == "__main__":
    # Initialize dataset loader
    # Note: Update the path to your actual TrashNet dataset location
    dataset_path = "path/to/your/trashnet/dataset"
    
    if os.path.exists(dataset_path):
        loader = TrashNetLoader(dataset_path)
        
        # Analyze dataset
        class_counts, total_images = loader.analyze_dataset()
        
        # Load dataset generators
        train_gen, val_gen = loader.load_dataset()
        
        print(f"\nTraining batches: {len(train_gen)}")
        print(f"Validation batches: {len(val_gen)}")
    else:
        print(f"Dataset path {dataset_path} does not exist.")
        print("Please download the TrashNet dataset and update the path.")