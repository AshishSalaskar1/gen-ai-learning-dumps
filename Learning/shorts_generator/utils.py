# from pydub import AudioSegment
from PIL import Image, ImageOps
import requests
from io import BytesIO
# from pydub import AudioSegment
import os
import requests
import json
import ffmpeg
import time
BASE_URL = "https://text.pollinations.ai"
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play ,save

load_dotenv()

client = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)



def download_image(prompt, fname, target_width=720, target_height=1280, quality=40):
    """
    Downloads and downsizes an image to YouTube Shorts dimensions, maintaining aspect ratio.

    Parameters:
    - prompt (str): The image prompt for the URL.
    - fname (str): The filename to save the image as.
    - target_width (int): Desired width for YouTube Shorts (default: 720).
    - target_height (int): Desired height for YouTube Shorts (default: 1280).
    - quality (int): Image quality percentage (1-100, default: 75).
    """
    
    # Download image
    url = f"https://pollinations.ai/p/{prompt}"
    response = requests.get(url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))

        # Resize while maintaining aspect ratio
        img.thumbnail((target_width, target_height), Image.LANCZOS)

        # Add black padding to fit exact Shorts dimensions
        # img_with_padding = ImageOps.pad(img, (target_width, target_height), color=(0, 0, 0))

        # Save the image with reduced quality
        output_path = f'f:\\Gen_AI\\git_gen_ai\\Learning\\shorts_generator\\files\\{fname}.jpg'
        img.save(output_path, format='JPEG', quality=quality)
        time.sleep(2)

        print(f"✅ Image downloaded and resized to {target_width}x{target_height} at {quality}% quality: {output_path}")
    
    else:
        print(f"⚠️ Failed to download image. Status code: {response.status_code}")


# Base URL


def generate_audio(prompt, voice="alloy", method="GET", output_file="generated_audio.mp3"):
    """
    Generate audio using the Audio Generation API.

    Args:
    - prompt (str): Text to be converted to audio.
    - voice (str): Voice for the audio (default: "alloy").
    - method (str): HTTP method ("GET" or "POST").
    - output_file (str): Filename for the generated audio.

    Returns:
    - str: Path to the saved audio file or error message.
    """
    
    if method.upper() == "GET":
        # prompt = f"JUST REPEAT THE FOLLOWING CONTENT: {prompt}"
        url = f"{BASE_URL}/{prompt}?model=openai-audio&voice={voice}"
        try:
            response = requests.get(url)

            audio = client.text_to_speech.convert(
                text=prompt,
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                model_id="eleven_multilingual_v2",
                output_format="mp3_44100_128",
            )
            
            save( audio, output_file)
            compressed_output_file = output_file.replace("_temp", "")
            if os.path.exists(compressed_output_file):
                # print(":eA")
                os.remove(compressed_output_file)
            # sound = AudioSegment.from_file(output_file).export(output_file, format="mp3", bitrate="2k")
            ffmpeg.input(output_file).output(compressed_output_file, audio_bitrate="8k").run()

            return 

            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                    print(f"✅ Audio saved as '{output_file}'")
                time.sleep(2)

                
                compressed_output_file = output_file.replace("_temp", "")
                if os.path.exists(compressed_output_file):
                    # print(":eA")
                    os.remove(compressed_output_file)
                # sound = AudioSegment.from_file(output_file).export(output_file, format="mp3", bitrate="2k")
                ffmpeg.input(output_file).output(compressed_output_file, audio_bitrate="8k").run()
                print(f"✅ Audio saved as '{output_file}'")

                return output_file
            else:
                print(f"❌ Error: {response.status_code}")
                return response.text

        except Exception as e:
            print(f"❌ Exception: {e}")
            return str(e)

    else:
        print("❌ Invalid method. Use 'GET' or 'POST'")
        return "Invalid method"



    
