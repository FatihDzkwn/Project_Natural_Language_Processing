"""
Flask Application untuk Shopee Product Category Classifier
"""
from flask import Flask, render_template, request, jsonify
import os
from config import config, Config
from utils import get_predictor, init_predictor

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(config)

# Flag untuk track inisialisasi
_initialized = False

def init_app():
    """Initialize model predictor"""
    global _initialized
    if not _initialized:
        try:
            init_predictor()
            print("✓ Aplikasi siap!")
            _initialized = True
        except Exception as e:
            print(f"✗ Error saat startup: {e}")
            _initialized = False

# Initialize pada first request
@app.before_request
def before_first_request():
    """Jalankan sebelum request pertama"""
    global _initialized
    if not _initialized:
        init_app()


# ==================== Routes ====================

@app.route('/')
def home():
    """Halaman utama"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint untuk prediksi"""
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'Request harus berisi field "text"'
            }), 400
        
        text = data['text'].strip()
        
        if not text:
            return jsonify({
                'success': False,
                'error': 'Teks tidak boleh kosong'
            }), 400
        
        # Get predictor
        predictor = get_predictor()
        
        # Make prediction
        result = predictor.predict(text)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 400
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Server error: {str(e)}'
        }), 500


@app.route('/api/v1/predict', methods=['POST'])
def api_predict():
    """API endpoint dengan format lebih lengkap"""
    try:
        data = request.get_json()
        
        if not data or 'review' not in data:
            return jsonify({
                'status': 'error',
                'message': 'Request harus berisi field "review"',
                'code': 400
            }), 400
        
        review = data['review'].strip()
        
        predictor = get_predictor()
        result = predictor.predict(review)
        
        if 'error' in result:
            return jsonify({
                'status': 'error',
                'message': result['error'],
                'code': 400
            }), 400
        
        return jsonify({
            'status': 'success',
            'prediction': {
                'category': result['category'],
                'confidence': result['confidence'],
                'probabilities': result['probabilities']
            },
            'metadata': {
                'model': result['model_info']['model_name'],
                'accuracy': result['model_info']['accuracy']
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}',
            'code': 500
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Shopee Category Classifier',
        'version': '1.0'
    }), 200


@app.route('/info', methods=['GET'])
def info():
    """Get model information"""
    try:
        predictor = get_predictor()
        return jsonify({
            'model_info': predictor.model_info,
            'categories': list(predictor.model.classes_)
        }), 200
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


# ==================== Error Handlers ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Endpoint tidak ditemukan'
    }), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Server error'
    }), 500


# ==================== Main ====================

if __name__ == '__main__':
    # Development
    app.run(
        host='0.0.0.0',
        port=int(os.getenv('FLASK_PORT', 5000)),
        debug=app.config['DEBUG']
    )
    
    # Production (uncomment untuk production):
    # from waitress import serve
    # serve(app, host='0.0.0.0', port=5000)
