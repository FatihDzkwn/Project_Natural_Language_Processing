// ==================== DOM Elements ====================
const predictForm = document.getElementById('predictForm');
const reviewText = document.getElementById('reviewText');
const resultSection = document.getElementById('resultSection');
const resultContent = document.getElementById('resultContent');
const loadingSpinner = document.getElementById('loadingSpinner');
const exampleButtons = document.querySelectorAll('.example-btn');

// ==================== Event Listeners ====================

// Handle form submission
predictForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    await makePrediction();
});

// Handle example button clicks
exampleButtons.forEach(btn => {
    btn.addEventListener('click', () => {
        reviewText.value = btn.dataset.text;
        reviewText.focus();
    });
});

// ==================== Functions ====================

async function makePrediction() {
    const text = reviewText.value.trim();

    // Validation
    if (!text) {
        showError('Silakan masukkan ulasan terlebih dahulu');
        return;
    }

    if (text.length > 1000) {
        showError('Ulasan terlalu panjang (maksimal 1000 karakter)');
        return;
    }

    try {
        // Show loading spinner
        loadingSpinner.style.display = 'flex';
        resultSection.style.display = 'none';

        // Make API call
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });

        const data = await response.json();

        // Hide loading spinner
        loadingSpinner.style.display = 'none';

        if (!response.ok || !data.success) {
            showError(data.error || 'Terjadi kesalahan saat prediksi');
            return;
        }

        // Display results
        displayResults(data.data);

    } catch (error) {
        loadingSpinner.style.display = 'none';
        showError(`Kesalahan: ${error.message}`);
    }
}

function displayResults(data) {
    const categoryEmoji = {
        'Elektronik': '⚡',
        'Makanan': '🍲',
        'Kecantikan': '💄',
        'Otomotif': '🏍️'
    };

    const emoji = categoryEmoji[data.category] || '📦';

    // Format confidence as percentage
    const confidencePercent = Math.round(data.confidence * 100);

    // Build HTML
    let html = `
        <div class="prediction-card">
            <div class="prediction-category">
                ${emoji} ${data.category}
            </div>
            
            <div class="prediction-confidence">
                <span class="confidence-label">Confidence:</span>
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: 0%">
                        <span>${confidencePercent}%</span>
                    </div>
                </div>
            </div>

            <div class="probabilities">
                <h4>Probabilitas per Kategori</h4>
    `;

    // Sort probabilities by value (descending)
    const sortedProbs = Object.entries(data.probabilities)
        .sort((a, b) => b[1] - a[1]);

    sortedProbs.forEach(([category, prob]) => {
        const probPercent = Math.round(prob * 100);
        html += `
            <div class="probability-item">
                <span class="probability-name">${category}</span>
                <span class="probability-value">${probPercent}%</span>
            </div>
        `;
    });

    html += `
            </div>

            <div class="processed-text">
                <strong>📝 Teks setelah preprocessing:</strong><br>
                ${escapeHtml(data.processed_text)}
            </div>
        </div>
    `;

    resultContent.innerHTML = html;
    resultSection.style.display = 'block';

    // Animate confidence bar
    const confidenceFill = document.querySelector('.confidence-fill');
    setTimeout(() => {
        confidenceFill.style.width = confidencePercent + '%';
    }, 100);

    // Scroll to results
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function showError(message) {
    resultContent.innerHTML = `
        <div class="error-message">
            ⚠️ ${escapeHtml(message)}
        </div>
    `;
    resultSection.style.display = 'block';
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// ==================== Initialization ====================

// Log when page is ready
document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ Application loaded successfully');
    
    // Optional: Check if API is healthy
    fetch('/health')
        .then(response => response.json())
        .then(data => console.log('✓ API Status:', data.status))
        .catch(error => console.warn('⚠️ Could not connect to API:', error));
});
