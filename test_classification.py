import requests
import os

def test_classification():
    # Test different categories
    test_images = [
        "dataset/cardboard/cardboard1.jpg",
        "dataset/glass/glass1.jpg", 
        "dataset/metal/metal1.jpg",
        "dataset/paper/paper1.jpg",
        "dataset/plastic/plastic1.jpg"
    ]
    
    # Flask app URL
    url = "http://127.0.0.1:5000/classify"
    
    for test_image in test_images:
        if not os.path.exists(test_image):
            print(f"⚠️ Test image not found: {test_image}")
            continue
            
        print(f"\n🧪 Testing: {test_image}")
        
        try:
            # Send POST request with image
            with open(test_image, 'rb') as f:
                files = {'file': f}
                response = requests.post(url, files=files)
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Classification successful!")
                print(f"Category: {result.get('category')}")
                print(f"Confidence: {result.get('confidence')}%")
                print(f"Description: {result.get('recycling_info', {}).get('description', 'No description')}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_classification()