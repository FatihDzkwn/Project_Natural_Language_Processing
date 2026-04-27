# Model Directory

Folder ini menyimpan semua model dan preprocessor yang telah dilatih.

## Struktur

```
Model/
├── trained_models/          # Menyimpan model yang telah dilatih
│   ├── svm_tfidf_model.pkl  # Model SVM yang sudah trained
│   ├── tfidf_vectorizer.pkl # TF-IDF Vectorizer
│   └── model_info.json      # Metadata model (accuracy, waktu training, dll)
│
├── preprocessors/           # Menyimpan preprocessor tools
│   ├── stemmer.pkl          # Sastrawi Stemmer (serialized)
│   ├── slang_dict.json      # Kamus slang untuk normalisasi
│   └── stopwords.txt        # Daftar stopwords bahasa Indonesia
│
└── README.md                # File dokumentasi ini
```

## Cara Menyimpan Model (dari Notebook)

```python
import pickle
import json

# 1. Simpan SVM Model
with open('Model/trained_models/svm_tfidf_model.pkl', 'wb') as f:
    pickle.dump(svm_tfidf, f)

# 2. Simpan TF-IDF Vectorizer
with open('Model/trained_models/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(tfidf_vec, f)

# 3. Simpan Stemmer
with open('Model/preprocessors/stemmer.pkl', 'wb') as f:
    pickle.dump(stemmer, f)

# 4. Simpan Slang Dictionary
with open('Model/preprocessors/slang_dict.json', 'w', encoding='utf-8') as f:
    json.dump(slang_dict, f, ensure_ascii=False, indent=2)

# 5. Simpan Model Info
model_info = {
    "model_name": "SVM + TF-IDF",
    "accuracy": 0.85,  # Ganti dengan accuracy dari training
    "training_date": "2024-04-27",
    "model_type": "SVM (Support Vector Machine)",
    "feature_extraction": "TF-IDF",
    "classes": list(svm_tfidf.classes_),
    "max_features": 5000
}
with open('Model/trained_models/model_info.json', 'w') as f:
    json.dump(model_info, f, indent=2)
```

## Cara Memuat Model (di App Deployment)

```python
import pickle
import json

# 1. Load SVM Model
with open('Model/trained_models/svm_tfidf_model.pkl', 'rb') as f:
    svm_model = pickle.load(f)

# 2. Load TF-IDF Vectorizer
with open('Model/trained_models/tfidf_vectorizer.pkl', 'rb') as f:
    tfidf_vec = pickle.load(f)

# 3. Load Stemmer
with open('Model/preprocessors/stemmer.pkl', 'rb') as f:
    stemmer = pickle.load(f)

# 4. Load Slang Dictionary
with open('Model/preprocessors/slang_dict.json', 'r', encoding='utf-8') as f:
    slang_dict = json.load(f)

# 5. Load Model Info
with open('Model/trained_models/model_info.json', 'r') as f:
    model_info = json.load(f)
```

## File yang Harus Ada

- [ ] `trained_models/svm_tfidf_model.pkl` - Model utama
- [ ] `trained_models/tfidf_vectorizer.pkl` - Vectorizer
- [ ] `trained_models/model_info.json` - Metadata
- [ ] `preprocessors/stemmer.pkl` - Stemmer
- [ ] `preprocessors/slang_dict.json` - Slang dictionary
- [ ] `preprocessors/stopwords.txt` - Stopwords (opsional)

## Notes

- Semua file `.pkl` adalah serialized Python objects
- File `.json` adalah text files yang bisa dibuka dengan text editor
- Pastikan struktur preprocessing di app deployment sama dengan training
