import argparse
import logging
import os
import uuid
from vosk import Model, SetLogLevel
from sharetape import Sharetape

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--video", type=str, required=False, default="")
    parser.add_argument("-a", "--audio", type=str, required=False, default="")
    args = parser.parse_args()

    # Check for valid arguments
    if not (args.video or args.audio):
        parser.error("No action requested, add --video or --audio")
    elif args.video and args.audio:
        parser.error("Only select one action --video or --audio")

    # Set log level for vosk
    SetLogLevel(-1)
    
    # Load Vosk model for speech-to-text
    model = Model(model_path="vosk-model-en-us-0.42-gigaspeech")
    logging.info("sp2t setup")

    # Generate a unique identifier for the video processing
    video_id = str(uuid.uuid4())
    
    # Create a directory to store processing results
    os.makedirs(f"{video_id}")

    # Determine the source of audio input
    if args.audio != "":
        audio = args.audio
    else:
        audio = f"{video_id}/audio.wav"

    # Initialize ShareTape object for video processing
    shartape = Sharetape(
        args.video,
        audio,
        f"{video_id}/mono_audio.wav",
        f"{video_id}/transcript.txt",
        f"{video_id}/words.json",
        f"{video_id}/captions.srt",
        model,
    )
    
    # Extract transcript from the audio or video
    shartape.extract_transcript()

if __name__ == "__main__":
    main()
