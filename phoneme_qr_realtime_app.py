
import streamlit as st
import pandas as pd
import base64
import json
import cv2
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

st.set_page_config(page_title="📹 Real-time QR Phoneme Scanner", layout="wide")
st.title("📹 Real-Time QR Code Phoneme Scanner + 🎧 Audio Synth")

st.markdown("This app reads QR codes from webcam feed, decodes phoneme vectors, and plays them as synthetic tones.")

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

st.subheader("📷 Press 'Start Camera' to Scan QR Code")

start = st.button("Start Camera")
frame_placeholder = st.empty()
result_placeholder = st.empty()

if start:
    cap = cv2.VideoCapture(0)

    with st.spinner("Scanning for QR codes... Press 'Stop Camera' to end."):
        stop = st.button("Stop Camera")
        while cap.isOpened() and not stop:
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to grab frame from camera.")
                break

            # Convert to RGB for display
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_placeholder.image(rgb_frame, channels="RGB")

            decoded_objs = decode(Image.fromarray(rgb_frame))
            if decoded_objs:
                data = decoded_objs[0].data.decode("utf-8")
                result_placeholder.success("📦 QR Code Detected!")
                result_placeholder.code(data, language="text")

                try:
                    decoded_vectors = json.loads(base64.b64decode(data))
                    st.markdown("### 🔢 Decoded Vectors")
                    st.json(decoded_vectors)

                    phonemes = []
                    for vec in decoded_vectors:
                        phon = reverse_vector_map.get(tuple(vec), "❓")
                        phonemes.append(phon)

                    st.markdown("### 🔡 Reconstructed Phonemes")
                    st.markdown(" ".join(phonemes))

                    if st.button("🎧 Play Audio"):
                        audio = synthesize_audio(phonemes)
                        audio.export("live_audio.wav", format="wav")
                        st.audio("live_audio.wav")

                    break  # Stop after first successful scan

                except Exception as e:
                    st.error(f"Decoding error: {e}")
                    break

        cap.release()
        cv2.destroyAllWindows()
