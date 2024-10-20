import streamlit as st
import moviepy.editor as mp
import speech_recognition as sr
import pyttsx3
import os

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

def extract_audio_from_video(video_file):
    """Extract audio from the video file."""
    video = mp.VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file)
    return audio_file

def transcribe_audio(audio_file):
    """Transcribe audio to text."""
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # read the entire audio file
        try:
            text = recognizer.recognize_google(audio_data)
            return text
        except sr.UnknownValueError:
            st.error("Audio not understood")
            return None
        except sr.RequestError as e:
            st.error(f"Could not request results from Google Speech Recognition service; {e}")
            return None

def correct_transcription(text):
    """Simulate correction of transcription (you can integrate GPT model here)."""
    return text  # Replace this with GPT-4 API call if needed.

def text_to_speech(text, output_audio_file):
    """Convert corrected text to speech."""
    engine.save_to_file(text, output_audio_file)
    engine.runAndWait()

def replace_audio_in_video(video_file, audio_file):
    """Replace the audio in the original video file with the new audio."""
    video = mp.VideoFileClip(video_file)
    new_audio = mp.AudioFileClip(audio_file)
    final_video = video.set_audio(new_audio)
    final_video.write_videofile("final_video.mp4", codec="libx264")

def main():
    st.title("Video Audio Replacement App")

    # Step 1: Upload video file
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4"])
    
    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        video_file = "uploaded_video.mp4"
        with open(video_file, "wb") as f:
            f.write(uploaded_file.read())

        st.video(video_file)  # Display uploaded video

        # Step 1: Extract audio from video
        st.info("Extracting audio from the video...")
        audio_file = extract_audio_from_video(video_file)

        # Step 2: Transcribe the extracted audio
        st.info("Transcribing audio...")
        transcription = transcribe_audio(audio_file)
        
        if transcription:
            st.write("Original Transcription:", transcription)

            # Step 3: Correct transcription (optional)
            corrected_transcription = correct_transcription(transcription)
            st.write("Corrected Transcription:", corrected_transcription)

            # Step 4: Convert corrected transcription to speech
            st.info("Converting corrected text to speech...")
            new_audio_file = "corrected_audio.wav"
            text_to_speech(corrected_transcription, new_audio_file)

            # Step 5: Replace audio in video
            st.info("Replacing audio in the video...")
            replace_audio_in_video(video_file, new_audio_file)

            # Display the processed video
            st.video("final_video.mp4")

            # Clean up temporary files
            os.remove(audio_file)
            os.remove(new_audio_file)
        else:
            st.error("Transcription failed.")

if __name__ == "__main__":
    main()
