import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np
import os

class WasteClassificationModel:
    def __init__(self, image_size=(224, 224), num_classes=6):
        self.image_size = image_size
        self.num_classes = num_classes
        self.model = None
        self.history = None
    
    def build_model(self):
        """Build the CNN model using transfer learning"""
        # Load pre-trained MobileNetV2
        base_model = MobileNetV2(
            weights='imagenet',
            include_top=False,
            input_shape=(*self.image_size, 3)
        )
        
        # Freeze base model layers
        base_model.trainable = False
        
        # Add custom layers
        model = models.Sequential([
            base_model,
            layers.GlobalAveragePooling2D(),
            layers.Dense(128, activation='relu'),
            layers.Dropout(0.3),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        self.model = model
        return model
    
    def compile_model(self, learning_rate=0.001):
        """Compile the model"""
        self.model.compile(
            optimizer=Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
    
    def train(self, train_dir, val_dir, epochs=20, batch_size=32):
        """Train the model"""
        # Data augmentation for training
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            horizontal_flip=True,
            zoom_range=0.2,
            shear_range=0.2,
            fill_mode='nearest'
        )
        
        # Only rescaling for validation
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        # Create data generators
        train_generator = train_datagen.flow_from_directory(
            train_dir,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        val_generator = val_datagen.flow_from_directory(
            val_dir,
            target_size=self.image_size,
            batch_size=batch_size,
            class_mode='categorical'
        )
        
        # Train the model
        self.history = self.model.fit(
            train_generator,
            epochs=epochs,
            validation_data=val_generator,
            verbose=1
        )
        
        return self.history
    
    def save_model(self, filepath):
        """Save the trained model"""
        self.model.save(filepath)
        print(f"Model saved to {filepath}")
    
    def plot_training_history(self):
        """Plot training history"""
        if self.history is None:
            print("No training history available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
        
        # Plot accuracy
        ax1.plot(self.history.history['accuracy'], label='Training Accuracy')
        ax1.plot(self.history.history['val_accuracy'], label='Validation Accuracy')
        ax1.set_title('Model Accuracy')
        ax1.set_xlabel('Epoch')
        ax1.set_ylabel('Accuracy')
        ax1.legend()
        
        # Plot loss
        ax2.plot(self.history.history['loss'], label='Training Loss')
        ax2.plot(self.history.history['val_loss'], label='Validation Loss')
        ax2.set_title('Model Loss')
        ax2.set_xlabel('Epoch')
        ax2.set_ylabel('Loss')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()

def main():
    # Initialize model
    model = WasteClassificationModel()
    
    # Build and compile model
    model.build_model()
    model.compile_model()
    
    # Print model summary
    model.model.summary()
    
    # Set up dataset directories
    dataset_dir = 'dataset'
    
    if os.path.exists(dataset_dir):
        print("Dataset found! Starting training...")
        
        # Use the dataset loader
        from dataset_loader import TrashNetLoader
        loader = TrashNetLoader(dataset_dir)
        
        # Analyze dataset
        loader.analyze_dataset()
        
        # Load dataset generators
        train_gen, val_gen = loader.load_dataset(validation_split=0.2, batch_size=16)
        
        # Train the model with fewer epochs for faster training
        print("Starting model training...")
        history = model.model.fit(
            train_gen,
            epochs=10,  # Reduced epochs for faster training
            validation_data=val_gen,
            verbose=1
        )
        
        # Save the model
        model.save_model('app/ml_model/saved_model.h5')
        print("Model training completed and saved!")
        
    else:
        print(f"Dataset directory '{dataset_dir}' not found!")
        print("Please ensure the dataset is in the correct location.")

if __name__ == "__main__":
    main()