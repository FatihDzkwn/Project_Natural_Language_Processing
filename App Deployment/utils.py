"""
Utility functions untuk preprocessing dan prediction
"""
import re
import json
import pickle
from config import Config, MODEL_SETTINGS

class TextPreprocessor:
    """Class untuk preprocessing teks"""
    
    def __init__(self):
        """Initialize preprocessor dengan load semua resource yang diperlukan"""
        self.load_resources()
    
    def load_resources(self):
        """Load stemmer dan slang dictionary"""
        try:
            # Load Stemmer
            with open(Config.STEMMER_PATH, 'rb') as f:
                self.stemmer = pickle.load(f)
        except Exception as e:
            print(f"Warning: Tidak bisa load stemmer: {e}")
            self.stemmer = None
        
        try:
            # Load Slang Dictionary
            with open(Config.SLANG_DICT_PATH, 'r', encoding='utf-8') as f:
                self.slang_dict = json.load(f)
        except Exception as e:
            print(f"Warning: Tidak bisa load slang dictionary: {e}")
            self.slang_dict = {}
    
    def clean_text(self, text):
        """
        Pipeline preprocessing lengkap sesuai training data
        
        Steps:
        1. Lowercase
        2. Remove punctuation
        3. Remove repeated characters
        4. Slang normalization
        5. Stemming
        """
        # 1. Lowercase
        text = text.lower()
        
        # 2. Remove punctuation
        text = re.sub(r'[^\w\s]', '', text)
        
        # 3. Remove repeated characters
        text = re.sub(r'(.)\1{2,}', r'\1', text)
        
        words = text.split()
        
        # 4. Slang normalization
        if self.slang_dict:
            words = [self.slang_dict.get(word, word) for word in words]
        
        text = " ".join(words)
        
        # 5. Stemming
        if self.stemmer:
            text = self.stemmer.stem(text)
        
        return text
    
    def preprocess(self, text):
        """Public method untuk preprocessing"""
        if not text or not isinstance(text, str):
            raise ValueError("Text harus berupa string yang tidak kosong")
        
        # Validasi panjang teks
        from config import API_SETTINGS
        if len(text) > API_SETTINGS['max_text_length']:
            raise ValueError(f"Teks terlalu panjang (max {API_SETTINGS['max_text_length']} karakter)")
        
        return self.clean_text(text)


class ModelPredictor:
    """Class untuk melakukan prediksi"""
    
    def __init__(self):
        """Initialize model dan vectorizer"""
        self.load_model()
        self.preprocessor = TextPreprocessor()
    
    def load_model(self):
        """Load trained model dan vectorizer"""
        try:
            # Load SVM Model
            with open(Config.MODEL_PATH, 'rb') as f:
                self.model = pickle.load(f)
            
            # Load TF-IDF Vectorizer
            with open(Config.VECTORIZER_PATH, 'rb') as f:
                self.vectorizer = pickle.load(f)
            
            # Load Model Info
            with open(Config.MODEL_INFO_PATH, 'r') as f:
                self.model_info = json.load(f)
            
            print("✓ Model berhasil dimuat")
        except FileNotFoundError as e:
            raise Exception(f"Model file tidak ditemukan: {e}")
        except Exception as e:
            raise Exception(f"Error saat load model: {e}")
    
    def predict(self, text):
        """
        Lakukan prediksi kategori untuk teks input
        
        Args:
            text (str): Teks ulasan yang akan diprediksi
        
        Returns:
            dict: {
                'category': predicted_category,
                'confidence': confidence_score,
                'probabilities': {class_name: probability, ...},
                'processed_text': preprocessed_text
            }
        """
        try:
            # Preprocessing
            processed_text = self.preprocessor.preprocess(text)
            
            # Vectorize
            vectorized = self.vectorizer.transform([processed_text])
            
            # Predict
            prediction = self.model.predict(vectorized)[0]
            probabilities = self.model.predict_proba(vectorized)[0]
            
            # Build result
            classes = self.model.classes_
            result = {
                'category': prediction,
                'confidence': float(max(probabilities)),
                'probabilities': {classes[i]: float(probabilities[i]) for i in range(len(classes))},
                'processed_text': processed_text,
                'model_info': self.model_info
            }
            
            return result
        
        except ValueError as e:
            return {'error': str(e), 'status': 'validation_error'}
        except Exception as e:
            return {'error': str(e), 'status': 'prediction_error'}


# Global instance untuk digunakan di app
predictor = None

def init_predictor():
    """Initialize global predictor"""
    global predictor
    predictor = ModelPredictor()
    return predictor

def get_predictor():
    """Get global predictor instance"""
    global predictor
    if predictor is None:
        predictor = init_predictor()
    return predictor
