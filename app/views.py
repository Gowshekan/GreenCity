from flask import Blueprint, render_template, request, jsonify
import os
from werkzeug.utils import secure_filename
import base64
from app.models import waste_classifier
from config import Config

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@main.route('/')
def index():
    # Pass config to template
    return render_template('index.html', config=Config)

@main.route('/classify', methods=['POST'])
def classify_waste():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        try:
            # Get prediction
            category, confidence = waste_classifier.predict(filepath)
            
            # Get recycling info
            recycling_info = Config.RECYCLING_INFO.get(category, {})
            
            # Convert image to base64 for display
            with open(filepath, "rb") as img_file:
                img_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            
            # Clean up uploaded file
            os.remove(filepath)
            
            return jsonify({
                'success': True,
                'category': category,
                'confidence': round(float(confidence) * 100, 2),
                'recycling_info': recycling_info,
                'image': img_base64
            })
            
        except Exception as e:
            # Clean up file in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Processing error: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file type. Please upload PNG, JPG, or JPEG.'}), 400

@main.route('/about')
def about():
    return render_template('about.html', config=Config)

@main.route('/result')
def result():
    # This would need to get the result data from session or database
    # For now, we'll redirect to home since we're showing results on the same page
    return render_template('index.html')

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main.app_errorhandler(500)
def internal_error(error):
    return render_template('404.html'), 500