# Phoneme QR Streamlit App

This is a fully deployable Streamlit app for:
- Encoding sentences into IPA phonemes
- Mapping phonemes to 6D vectors
- Encoding as Base64
- Generating + scanning QR codes
- Reconstructing and playing phoneme audio

## 🚀 To Run Locally

```bash
git clone <this-repo>
cd phoneme_qr_streamlit_app
pip install -r requirements.txt
streamlit run phoneme_qr_realtime_app.py
```

Ensure your webcam is functional and permission is granted.

## 📁 Included Files

- `phoneme_qr_realtime_app.py` — Main Streamlit app
- `phoneme_map_full.csv` — Full IPA phoneme → 6D vector dataset
- `requirements.txt` — All required Python libraries
