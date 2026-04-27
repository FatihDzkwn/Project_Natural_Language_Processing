# App Deployment - Shopee Product Category Classifier

Aplikasi web untuk memprediksi kategori produk berdasarkan ulasan pelanggan menggunakan model SVM + TF-IDF.

## 📋 Struktur Folder

```
App Deployment/
├── app.py                 # Flask aplikasi utama
├── config.py              # Konfigurasi aplikasi
├── utils.py               # Fungsi utility dan preprocessing
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html         # Template HTML
├── static/
│   ├── style.css          # Stylesheet
│   └── script.js          # JavaScript
├── .env                   # Environment variables (opsional)
└── README.md              # Dokumentasi ini
```

## 🚀 Persiapan Awal

### 1. Install Dependencies

```bash
cd "App Deployment"
pip install -r requirements.txt
```

### 2. Siapkan Model Files

Pastikan file-file berikut sudah ada di folder `Model/`:

```
Model/
├── trained_models/
│   ├── svm_tfidf_model.pkl
│   ├── tfidf_vectorizer.pkl
│   └── model_info.json
└── preprocessors/
    ├── stemmer.pkl
    └── slang_dict.json
```

Jika belum ada, jalankan code di notebook untuk export model (lihat `Model/README.md`).

### 3. Ubah Path Konfigurasi (jika diperlukan)

Edit `config.py` dan sesuaikan path relatif jika struktur folder berbeda:

```python
MODEL_PATH = '../Model/trained_models/svm_tfidf_model.pkl'
VECTORIZER_PATH = '../Model/trained_models/tfidf_vectorizer.pkl'
# ... dst
```

## 🏃 Menjalankan Aplikasi

### Development Mode

```bash
python app.py
```

Aplikasi akan berjalan di: `http://localhost:5000`

### Production Mode (dengan Gunicorn)

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📡 API Endpoints

### 1. Health Check
```
GET /health

Response:
{
    "status": "healthy",
    "service": "Shopee Category Classifier",
    "version": "1.0"
}
```

### 2. Model Info
```
GET /info

Response:
{
    "model_info": {
        "model_name": "SVM + TF-IDF",
        "accuracy": 0.85,
        ...
    },
    "categories": ["Elektronik", "Kecantikan", "Makanan", "Otomotif"]
}
```

### 3. Prediksi (Web Interface)
```
POST /predict

Request Body:
{
    "text": "Kabel terminal ini sangat aman"
}

Response:
{
    "success": true,
    "data": {
        "category": "Elektronik",
        "confidence": 0.95,
        "probabilities": {
            "Elektronik": 0.95,
            "Kecantikan": 0.03,
            "Makanan": 0.01,
            "Otomotif": 0.01
        },
        "processed_text": "kabel terminal aman"
    }
}
```

### 4. Prediksi (API)
```
POST /api/v1/predict

Request Body:
{
    "review": "Kabel terminal ini sangat aman"
}

Response:
{
    "status": "success",
    "prediction": {
        "category": "Elektronik",
        "confidence": 0.95,
        "probabilities": {...}
    },
    "metadata": {
        "model": "SVM + TF-IDF",
        "accuracy": 0.85
    }
}
```

## 🎨 Fitur Aplikasi

### Web Interface
- **Input ulasan**: Textarea untuk menginput ulasan produk
- **Tombol Analisis**: Memproses ulasan dan menampilkan prediksi
- **Contoh Ulasan**: Quick examples untuk kategori berbeda
- **Hasil Prediksi**: Menampilkan:
  - Kategori yang diprediksi dengan emoji
  - Confidence score dengan progress bar
  - Probabilitas untuk semua kategori
  - Teks setelah preprocessing

### Fitur Lainnya
- Loading spinner saat proses
- Error handling yang baik
- Responsive design (mobile-friendly)
- Validasi input

## 🛠️ Pengembangan

### Struktur Code

**utils.py** menyediakan 2 class utama:

```python
# Preprocessing
preprocessor = TextPreprocessor()
cleaned = preprocessor.preprocess("text...")

# Prediksi
predictor = ModelPredictor()
result = predictor.predict("text...")
```

### Menambah Fitur

1. Modifikasi `app.py` untuk menambah endpoint
2. Update `utils.py` untuk preprocessing tambahan
3. Modifikasi `templates/index.html` untuk UI
4. Update `static/style.css` dan `static/script.js` untuk styling/interaksi

### Custom Preprocessing

Edit fungsi `clean_text()` di `utils.py`:

```python
def clean_text(self, text):
    # Tambahkan step preprocessing di sini
    text = text.lower()
    # ... tambahan steps
    return text
```

## 📦 Environment Variables (.env)

Buat file `.env` untuk konfigurasi yang sensitive:

```
FLASK_ENV=development
FLASK_PORT=5000
SECRET_KEY=your-secret-key-here
```

Kemudian load di `config.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

## 🧪 Testing

### Test API dengan cURL

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Kabel terminal ini sangat aman"}'
```

### Test API dengan Python

```python
import requests

response = requests.post('http://localhost:5000/predict', 
    json={"text": "Kabel terminal ini sangat aman"}
)
print(response.json())
```

## 📝 Debugging

### Cek koneksi model

```python
from utils import ModelPredictor
predictor = ModelPredictor()
print(predictor.model_info)
print(predictor.model.classes_)
```

### Cek preprocessing

```python
from utils import TextPreprocessor
preprocessor = TextPreprocessor()
print(preprocessor.preprocess("Kabel terminal aman"))
```

## 🐛 Troubleshooting

### ModuleNotFoundError

```bash
pip install -r requirements.txt
```

### Model file not found

- Pastikan path di `config.py` benar
- Gunakan absolute path jika perlu:
  ```python
  import os
  MODEL_PATH = os.path.join(os.path.dirname(__file__), '../Model/...')
  ```

### Port 5000 already in use

```bash
python app.py --port 8000
# atau
flask run --port 8000
```

## 📚 Referensi

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn Documentation](https://scikit-learn.org/)
- [Sastrawi Documentation](https://github.com/har07/PyTextPreprocessing)

## 👥 Authors

Naga Group - Natural Language Processing Project 2024

## 📄 License

MIT License
