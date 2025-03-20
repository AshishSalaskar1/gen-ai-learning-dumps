# from pydub import AudioSegment
from PIL import Image, ImageOps
import requests
from io import BytesIO
# from pydub import AudioSegment
import os
import requests
import json
import ffmpeg




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

        print(f"✅ Image downloaded and resized to {target_width}x{target_height} at {quality}% quality: {output_path}")
    
    else:
        print(f"⚠️ Failed to download image. Status code: {response.status_code}")


# Base URL
BASE_URL = "https://text.pollinations.ai"


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
        prompt = f"JUST REPEAT THE FOLLOWING CONTENT: {prompt}"
        url = f"{BASE_URL}/{prompt}?model=openai-audio&voice={voice}"
        try:
            response = requests.get(url)

            if response.status_code == 200:
                with open(output_file, "wb") as f:
                    f.write(response.content)
                
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



script_data =  {'0s-3s': {'text': "Get ready for breathtaking views! Let's explore the top highest places on Earth",
  'image_prompt': 'Aerial view of a majestic mountain range with snow-capped peaks, sun rising behind it'},
 '4s-7s': {'text': "From Mount Everest to Kilimanjaro, we'll take you on a journey to the roof of the world",
  'image_prompt': "Close-up shot of Mount Everest's summit with a flag waving in the wind"},
 '8s-11s': {'text': 'Number 5: Mount Aconcagua, Argentina - The highest peak outside Asia at 22,841ft',
  'image_prompt': 'Panoramic view of Mount Aconcagua, with a snow-capped summit and surrounding mountains'},
 '12s-15s': {'text': 'Number 4: K2, Pakistan/China - The second-highest peak in the world at 28,251ft',
  'image_prompt': "Dramatic shot of K2's rugged terrain, with snow and ice-covered peaks"},
 '16s-20s': {'text': 'Number 3: Kangchenjunga, Nepal/India - The third-highest peak in the world at 28,169ft',
  'image_prompt': 'Lush green forests and towering mountains of Kangchenjunga, with a misty atmosphere'},
 '21s-25s': {'text': 'Number 2: Mount Denali, Alaska/USA - The highest peak in North America at 20,310ft',
  'image_prompt': 'Snowy landscape of Mount Denali, with a majestic glacier and surrounding peaks'},
 '26s-30s': {'text': 'And the number one spot goes to... Mount Everest! The highest peak in the world at 29,029ft',
  'image_prompt': "Iconic shot of Mount Everest's summit, with a flag waving in the wind and a breathtaking view"}}


for ts, val in script_data.items():
    text, img_caption = val["text"], val["image_prompt"]
    print(ts, text, img_caption)

    download_image(
        prompt=img_caption,
        fname=ts
    )

    generate_audio(
        text, 
        voice="alloy", 
        method="GET", 
        output_file=f"files/{ts}_temp.mp3"
    )

    
