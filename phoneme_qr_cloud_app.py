
import streamlit as st
import pandas as pd
import base64
import json
from PIL import Image
from pyzbar.pyzbar import decode
from io import BytesIO
from pydub.generators import Sine

@st.cache_data
def load_phoneme_map():
    df = pd.read_csv("phoneme_map_full.csv")
    symbol_to_vector = {
        row["IPA Symbol"]: eval(row["6D Vector"])
        for _, row in df.iterrows()
    }
    reverse_map = {
        tuple(eval(row["6D Vector"])): row["IPA Symbol"]
        for _, row in df.iterrows()
    }
    return df, symbol_to_vector, reverse_map

df, phoneme_vector_map, reverse_vector_map = load_phoneme_map()

st.set_page_config(page_title="Phoneme QR Scanner", layout="wide")
st.title("📦 Streamlit QR Phoneme Decoder + 🎧 Audio Synth")

st.markdown("Upload a QR image to decode phoneme sequences and play synthetic audio tones.")

def synthesize_audio(phoneme_list):
    tone_map = {
        "/p/": 300, "/b/": 310, "/t/": 320, "/d/": 330, "/k/": 340, "/g/": 350,
        "/æ/": 360, "/s/": 370, "/m/": 380, "/n/": 390, "/ɑ/": 400, "/ð/": 410,
        "/ə/": 420, "/ʃ/": 430, "/z/": 440, "/ʒ/": 450, "/l/": 460, "/r/": 470
    }
    audio = None
    for ph in phoneme_list:
        freq = tone_map.get(ph, 250)
        tone = Sine(freq).to_audio_segment(duration=200)
        audio = tone if audio is None else audio + tone
    return audio

st.subheader("📤 Upload QR Code Image")

uploaded = st.file_uploader("Choose a QR code image (PNG, JPG)", type=["png", "jpg", "jpeg"])
if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded QR Image")

    decoded = decode(img)
    if decoded:
        base64_data = decoded[0].data.decode("utf-8")
        st.success("✅ QR Code Detected")
        st.code(base64_data, language="text")

        try:
            decoded_vectors = json.loads(base64.b64decode(base64_data))
            st.markdown("### 🔢 Decoded 6D Vectors")
            st.json(decoded_vectors)

            phonemes = []
            for vec in decoded_vectors:
                phon = reverse_vector_map.get(tuple(vec), "❓")
                phonemes.append(phon)

            st.markdown("### 🔡 Reconstructed Phonemes")
            st.markdown(" ".join(phonemes))

            if st.button("🎧 Play Synthesized Audio"):
                audio = synthesize_audio(phonemes)
                audio.export("cloud_audio.wav", format="wav")
                st.audio("cloud_audio.wav")

        except Exception as e:
            st.error(f"Error decoding base64 data: {e}")
    else:
        st.warning("⚠️ No QR code found in image.")
