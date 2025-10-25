import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'ecosort-ai-secret-key-2025'
    UPLOAD_FOLDER = 'app/static/uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    
    # Model configuration
    MODEL_PATH = 'app/ml_model/saved_model.h5'
    IMAGE_SIZE = (224, 224)
    
    # Waste categories
    WASTE_CATEGORIES = {
        0: 'Cardboard',
        1: 'Glass',
        2: 'Metal',
        3: 'Paper',
        4: 'Plastic',
        5: 'Organic/Trash'
    }
    
    # Recycling information
    RECYCLING_INFO = {
        'Cardboard': {
            'description': 'Cardboard can be recycled into new cardboard products.',
            'tips': ['Flatten boxes before recycling', 'Remove any non-paper packing material'],
            'color': '#8B4513'
        },
        'Glass': {
            'description': 'Glass is 100% recyclable and can be recycled endlessly without loss in quality.',
            'tips': ['Rinse containers before recycling', 'Remove lids and caps'],
            'color': '#1E90FF'
        },
        'Metal': {
            'description': 'Metals like aluminum and steel are highly recyclable.',
            'tips': ['Rinse cans before recycling', 'Separate aluminum from steel if possible'],
            'color': '#A9A9A9'
        },
        'Paper': {
            'description': 'Paper recycling helps save trees and reduce landfill waste.',
            'tips': ['Keep paper dry and clean', 'Remove any plastic windows from envelopes'],
            'color': '#FFD700'
        },
        'Plastic': {
            'description': 'Many plastics can be recycled, but check local guidelines for specific types.',
            'tips': ['Check resin codes (1-7)', 'Rinse containers before recycling'],
            'color': '#FF6347'
        },
        'Organic/Trash': {
            'description': 'Organic waste can be composted to create nutrient-rich soil.',
            'tips': ['Compost fruit and vegetable scraps', 'Avoid composting meat or dairy products'],
            'color': '#228B22'
        }
    }