# 📦 Phoneme QR Decoder Web App (Streamlit Cloud-Compatible)

This Streamlit app lets you upload a QR code image containing Base64-encoded phoneme data. It decodes the data into phoneme vectors, reconstructs the phonemes, and plays them as synthetic audio tones.

## ✅ Features

- Upload QR image (PNG/JPG)
- Decode Base64 → 6D Vector → IPA Phonemes
- Play synthesized tones from phonemes
- Designed to run on [Streamlit Cloud](https://streamlit.io/cloud)

## 🚀 Getting Started

```bash
git clone https://github.com/YOUR_USERNAME/phoneme-qr-cloud
cd phoneme-qr-cloud
pip install -r requirements.txt
streamlit run phoneme_qr_cloud_app.py
```

## 📁 Files

- `phoneme_qr_cloud_app.py` — Main Streamlit app
- `phoneme_map_full.csv` — Dataset for phoneme vector mapping
- `requirements.txt` — Python dependencies
