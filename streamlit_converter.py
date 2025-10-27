import os
import logging
from pathlib import Path
import streamlit as st
from pydub import AudioSegment
import tempfile

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

def convert_to_mono(input_file: Path) -> tuple[bool, bytes]:
    """
    Convert stereo MP3 to mono WAV by keeping only left channel.
    
    Args:
        input_file: Path to input MP3 file
        
    Returns:
        tuple: (success boolean, wav_bytes or None)
    """
    try:
        # Load MP3 file
        logging.info(f"Loading {input_file}")
        audio = AudioSegment.from_mp3(input_file)
        
        # Split channels
        channels = audio.split_to_mono()
        
        # Keep only left channel
        left_channel = channels[0]
        
        # Export as mono WAV to bytes
        with tempfile.NamedTemporaryFile(suffix='.wav') as temp_wav:
            left_channel.export(temp_wav.name, format="wav")
            wav_bytes = open(temp_wav.name, 'rb').read()
            
        return True, wav_bytes
        
    except Exception as e:
        logging.error(f"Error converting file: {str(e)}")
        return False, None

def main():
    st.set_page_config(page_title="MP3 to Mono WAV Converter")
    
    st.title("MP3 to Mono WAV Converter")
    st.write("Convert stereo MP3 files to mono WAV (left channel only)")
    
    uploaded_files = st.file_uploader(
        "Choose MP3 files", 
        type=['mp3'], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        st.write("---")
        st.write(f"Processing {len(uploaded_files)} files...")
        
        for uploaded_file in uploaded_files:
            st.write(f"\nProcessing: {uploaded_file.name}")
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix='.mp3') as temp_mp3:
                temp_mp3.write(uploaded_file.getvalue())
                temp_mp3.flush()
                
                # Convert to mono WAV
                success, wav_bytes = convert_to_mono(Path(temp_mp3.name))
                
                if success:
                    output_filename = f"{Path(uploaded_file.name).stem}_mono.wav"
                    st.success(f"Successfully converted: {uploaded_file.name}")
                    
                    # Add download button
                    st.download_button(
                        label=f"Download {output_filename}",
                        data=wav_bytes,
                        file_name=output_filename,
                        mime="audio/wav"
                    )
                else:
                    st.error(f"Failed to convert: {uploaded_file.name}")

if __name__ == "__main__":
    main()