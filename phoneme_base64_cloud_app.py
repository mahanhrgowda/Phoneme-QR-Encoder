
import streamlit as st
import pandas as pd
import base64
import json
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

st.set_page_config(page_title="Phoneme Base64 Decoder", layout="wide")
st.title("🔓 Base64 Phoneme Decoder + 🎧 Audio Synth")

st.markdown("Paste a Base64 string containing 6D phoneme vectors. The app will decode, reconstruct IPA phonemes, and play synthetic tones.")

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

st.subheader("📋 Paste Base64 Encoded Data")

base64_input = st.text_area("Enter Base64-encoded phoneme vector list")

if base64_input:
    try:
        decoded = json.loads(base64.b64decode(base64_input.encode("utf-8")))
        st.markdown("### 🔢 Decoded 6D Vectors")
        st.json(decoded)

        reconstructed = []
        for vec in decoded:
            phon = reverse_vector_map.get(tuple(vec), "❓")
            reconstructed.append(phon)

        st.markdown("### 🔡 Reconstructed IPA Phonemes")
        st.markdown(" ".join(reconstructed))

        if st.button("🎧 Play Audio"):
            audio = synthesize_audio(reconstructed)
            audio.export("audio.wav", format="wav")
            st.audio("audio.wav")

    except Exception as e:
        st.error(f"Failed to decode: {e}")
