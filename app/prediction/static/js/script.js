document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('results-section');
    const categoryBadge = document.getElementById('category-badge');
    const confidence = document.getElementById('confidence');
    const resultImage = document.getElementById('result-image');
    const recyclingDescription = document.getElementById('recycling-description');
    const recyclingTips = document.getElementById('recycling-tips');
    
    // Color mapping for categories
    const categoryColors = {
        'Cardboard': '#8B4513',
        'Glass': '#1E90FF',
        'Metal': '#A9A9A9',
        'Paper': '#FFD700',
        'Plastic': '#FF6347',
        'Organic/Trash': '#228B22'
    };
    
    // Upload area click event
    if (uploadArea) {
        uploadArea.addEventListener('click', function() {
            fileInput.click();
        });
    }
    
    if (uploadBtn) {
        uploadBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            fileInput.click();
        });
    }
    
    // File input change event
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files && this.files[0]) {
                const file = this.files[0];
                
                // Validate file size (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size too large. Please upload an image smaller than 10MB.');
                    return;
                }
                
                // Show loading animation
                loading.style.display = 'block';
                if (resultsSection) resultsSection.style.display = 'none';
                
                // Create FormData and send to server
                const formData = new FormData();
                formData.append('file', file);
                
                fetch('/classify', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    // Hide loading animation
                    loading.style.display = 'none';
                    
                    if (data.error) {
                        alert('Error: ' + data.error);
                        return;
                    }
                    
                    // Update results section with received data
                    if (categoryBadge) {
                        categoryBadge.textContent = data.category;
                        categoryBadge.style.backgroundColor = categoryColors[data.category] || '#777';
                    }
                    
                    if (confidence) confidence.textContent = data.confidence + '% Confidence';
                    if (resultImage) resultImage.src = 'data:image/jpeg;base64,' + data.image;
                    if (recyclingDescription) recyclingDescription.textContent = data.recycling_info.description;
                    
                    // Update recycling tips
                    if (recyclingTips) {
                        recyclingTips.innerHTML = '';
                        data.recycling_info.tips.forEach(tip => {
                            const li = document.createElement('li');
                            li.innerHTML = `<i class="fas fa-check-circle"></i> ${tip}`;
                            recyclingTips.appendChild(li);
                        });
                    }
                    
                    // Show results section with animation
                    if (resultsSection) resultsSection.style.display = 'block';
                    
                    // Scroll to results
                    resultsSection.scrollIntoView({ behavior: 'smooth' });
                })
                .catch(error => {
                    console.error('Error:', error);
                    loading.style.display = 'none';
                    alert('An error occurred while processing your image. Please try again.');
                });
            }
        });
    }
    
    // Add some interactive animations to category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});