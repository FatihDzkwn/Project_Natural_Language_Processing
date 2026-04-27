# 🛍️ Shopee Product Category Classifier

Aplikasi machine learning untuk memprediksi kategori produk berdasarkan ulasan pelanggan dari Shopee menggunakan Natural Language Processing (NLP).

**Kelompok:** 5 Naga  
**Mata Kuliah:** Natural Language Processing  
**Institusi:** STT Terpadu Nurul Fikri

---

## 👥 Tim Pengembang

| Nama | Role |
|------|------|
| Fatih Dzakwan Susilo | Data Collection |
| Amaya Eshia | Text Preprocessing |
| Arya Nuryawan | Feature Extraction |
| Muhammad Rojali | Modelling |
| Sultan Nabil Al Hakim | Comparison Model |

---

## 📊 Fitur Utama

- **Prediksi Kategori Produk**: Klasifikasi otomatis ke 4 kategori (Elektronik, Makanan, Kecantikan, Otomotif)
- **Model ML**: SVM + TF-IDF dengan accuracy ~85%
- **Web Interface**: UI interaktif untuk testing
- **REST API**: Endpoint untuk integrasi sistem lain
- **Text Preprocessing**: Stemming, slang normalization, tokenization

---

## 🏗️ Struktur Project

```
Project_Natural_Language_Processing/
├── README.md                               # File ini
├── Notebook/
│   └── Praktikum_Kelompok_5_Naga.ipynb    # Jupyter notebook (data, training, testing)
├── Model/
│   ├── trained_models/                    # Model yang sudah dilatih
│   ├── preprocessors/                     # Preprocessor tools
│   └── README.md                          # Dokumentasi model
├── App Deployment/
│   ├── app.py                             # Flask aplikasi
│   ├── config.py                          # Konfigurasi
│   ├── utils.py                           # Preprocessing & prediksi
│   ├── requirements.txt                   # Dependencies
│   ├── templates/index.html               # Web UI
│   ├── static/                            # CSS & JavaScript
│   └── README.md                          # Dokumentasi app
└── Data/
    ├── Elektronik_Terminal.csv
    ├── Kecantikan_Serum.csv
    ├── Makanan_Cilok.csv
    ├── Otomotif_Helm.csv
    └── shopee_reviews_master.csv          # Master dataset
```

---

## 🚀 Quick Start

### 1. Persiapan (dari Notebook)

Jalankan semua cell di notebook sampai selesai training.

Kemudian, tambahkan cell baru dan jalankan ini untuk export model:

```python
import pickle, json, os
from datetime import datetime
from sklearn.metrics import accuracy_score

os.makedirs('../Model/trained_models', exist_ok=True)
os.makedirs('../Model/preprocessors', exist_ok=True)

# Save Model
with open('../Model/trained_models/svm_tfidf_model.pkl', 'wb') as f:
    pickle.dump(svm_tfidf, f)
with open('../Model/trained_models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vec, f)

# Save Preprocessors
with open('../Model/preprocessors/stemmer.pkl', 'wb') as f:
    pickle.dump(stemmer, f)
with open('../Model/preprocessors/slang_dict.json', 'w', encoding='utf-8') as f:
    json.dump(slang_dict, f, ensure_ascii=False, indent=2)

# Save Model Info
accuracy = accuracy_score(y_test, y_pred_svm_tfidf)
model_info = {
    "model_name": "SVM + TF-IDF",
    "accuracy": float(accuracy),
    "training_date": datetime.now().strftime("%Y-%m-%d"),
    "classes": list(svm_tfidf.classes_)
}
with open('../Model/trained_models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)

print("✓ Model exported!")
```

### 2. Install Dependencies

```bash
cd "App Deployment"
pip install -r requirements.txt
```

### 3. Jalankan Aplikasi

```bash
python app.py
```

Buka: **http://localhost:5000**

---

## 💻 Cara Menggunakan

### Web Interface
1. Buka `http://localhost:5000`
2. Masukkan ulasan produk
3. Klik "Analisis"
4. Lihat hasil prediksi

### API Request

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Kabel terminal ini sangat aman"}'
```

**Response:**
```json
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
        }
    }
}
```

---

## 📊 Dataset & Model

**Dataset:**
- Sumber: Ulasan produk Shopee
- Total: ~1000+ ulasan
- Kategori: Elektronik, Makanan, Kecantikan, Otomotif
- Split: 80% train, 20% test

**Model:**
- Algorithm: Support Vector Machine (SVM)
- Features: TF-IDF Vectorizer
- Accuracy: ~85%
- Preprocessing: Lowercase → Remove punctuation → Stemming → Normalisasi slang

---

## 🔧 Troubleshooting

| Error | Solusi |
|-------|--------|
| Model file not found | Export model dari notebook terlebih dahulu |
| Port 5000 already in use | `python app.py --port 8000` |
| Dependencies error | `pip install --upgrade pip setuptools && pip install -r requirements.txt` |

---

## 📚 Dokumentasi Lengkap

- **Model**: Lihat `Model/README.md`
- **App**: Lihat `App Deployment/README.md`

---

## 🛠️ Tech Stack

Python 3.8+ | Flask | Scikit-learn | Sastrawi | Pandas | Spacy | Gensim

---

**Status**: ✅ Production Ready  
**Last Updated**: April 2024