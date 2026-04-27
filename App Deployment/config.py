"""
Konfigurasi aplikasi deployment
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== Flask Config ====================
class Config:
    """Base configuration"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Model paths
    MODEL_PATH = '../Model/trained_models/svm_tfidf_model.pkl'
    VECTORIZER_PATH = '../Model/trained_models/tfidf_vectorizer.pkl'
    MODEL_INFO_PATH = '../Model/trained_models/model_info.json'
    
    # Preprocessor paths
    STEMMER_PATH = '../Model/preprocessors/stemmer.pkl'
    SLANG_DICT_PATH = '../Model/preprocessors/slang_dict.json'
    STOPWORDS_PATH = '../Model/preprocessors/stopwords.txt'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    ENV = 'production'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

# ==================== App Settings ====================
# Pilih konfigurasi sesuai environment
config_name = os.getenv('FLASK_ENV', 'development')
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}[config_name]

# ==================== Model Settings ====================
MODEL_SETTINGS = {
    'max_features': 5000,
    'preprocessing_steps': [
        'lowercase',
        'remove_punctuation',
        'remove_repeated_chars',
        'slang_normalization',
        'stemming'
    ],
    'categories': ['Elektronik', 'Kecantikan', 'Makanan', 'Otomotif']
}

# ==================== API Settings ====================
API_SETTINGS = {
    'timeout': 30,
    'max_text_length': 1000,
    'confidence_threshold': 0.5
}
