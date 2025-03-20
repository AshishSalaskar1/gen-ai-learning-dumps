import streamlit as st
from utils import download_image, generate_audio

import os
import requests
import json
import ollama
from moviepy import *
from PIL import Image
from moviepy import *
from PIL import ImageFont



# CONSTANTS
model_name = 'llama3.2:latest'  


# Chat Section
st.title("Youtube Shorts Generator")
st.write("Enter the idea for your Youtube Short")

input_prompt = st.text_area(
    "Enter your youtube short idea here...."
)

submit_btn = st.button("Generate YT Short")

if submit_btn:
    with st.spinner("Generating your awesome video for you...", show_time=True):
        prompt = f"""
       You are a **YouTube Shorts content creator**.  
        Your task is to **write a simple 30-second video script** based on the provided details.  

        ### **TOPIC:** {input_prompt}  

        ### 🎥 **Script Instructions:**  
        - **Divide the script into sections** (at most **5 sections**, ideally **3-5**).  
        - Each section must have:  
            - A **timestamp** in `start_time-end_time` format (e.g., `0s-5s`).  
            - A **text description** that appears on the screen.  
        - Clearly define the **time duration** each section's text should remain on screen.  

        ### 🎨 **Image Generation Instructions:**  
        - For each section, generate an **image prompt** capturing the visual essence of the content.  
        - The image prompt should be:  
            - **Descriptive and detailed** (specify scenery, mood, and style).  
            - Unique for each section.  

        ---

        ### 🛑 **Output Format (STRICT JSON format)**:
        - Return the output **strictly in JSON format**.  
        - Wrap the JSON in triple backticks (```) without any extra symbols or text. Make sure there are only 2 ('```') one at start and another at end of JSON snippet  
        - **DO NOT include explanations, comments, or extra text**—only the JSON inside the backticks.  
        {{
            "start_time-end_time": {{
                "text" : content_of_the_script,
                "image_prompt" : img_prompt
            }}
        }}

        Example for reference and not for actual usage:
        {{
            '0s-3s': {{
                'text': "Get ready for breathtaking views! Let's explore the top highest places on Earth",
                'image_prompt': 'Aerial view of a majestic mountain range with snow-capped peaks, sun rising behind it'
            }},
            '4s-7s': {{
                'text': "From Mount Everest to Kilimanjaro, we'll take you on a journey to the roof of the world",
                'image_prompt': "Close-up shot of Mount Everest's summit with a flag waving in the wind"
            }}
        }}

        ---
        

        Make sure the **script is engaging, concise, and easy to visualize**. 
        ALSO IT HAS TO BE IN JSON FORMAT. Enclose the json output needed in set of ``` ( backticks showing start and end of json, and everything between them should be valid JSON without any other uselss symbols)
        """

        # Send the to Olama
        response = ollama.chat(model=model_name, messages=[{"role": "user", "content": prompt}])
        print(response["message"]["content"])
        print("=====*=======")
        script_data = json.loads(response['message']['content'].replace("\n","").replace("json","").split("```")[1].split("```")[0])
        print(script_data)


        # print(0/0)
        # Parsing response -. generate audio and images
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

        # generate video and save
        # Parameters
        output_file = "output.mp4"
        fps = 24  # Frame rate
        transition_duration = 1  # Transition duration in seconds

        # Function to extract timestamps
        def get_time_range(timestamp):
            """Extract start, end, and duration from the timestamp."""
            start, end = timestamp.split('-')
            start_sec = int(start[:-1])
            end_sec = int(end[:-1])
            duration = end_sec - start_sec
            return start_sec, end_sec, duration

        # Create list to hold the clips
        clips = []

        # Generate video clips from the images
        for timestamp, data in script_data.items():
            image_path = f"files/{timestamp}.jpg"  # Image filename based on timestamp
            audio_path = f"files/{timestamp}.mp3"
            start, end, duration = get_time_range(timestamp)

            if not os.path.exists(image_path):
                print(f"⚠️ Warning: {image_path} not found.")
                continue

            # Create image clip
            
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration + 1
            img_clip = ImageClip(image_path).with_duration(duration).with_duration(duration)

            print(timestamp, duration)

            # Add text overlay
            txt_clip = TextClip(
                method = "caption",
                text=data['text'],
                transparent = True,
                font_size=40,
                margin = (0, 10),
                color='white',
                bg_color="black",
                size=(img_clip.w-100, None),
                font="./arial.ttf",
                text_align="center",
            ).with_duration(duration).with_position(('center', 'bottom'))

            # Combine image and text into one clip
            final_clip = CompositeVideoClip([img_clip, txt_clip]).with_duration(duration).with_audio(audio_clip)

            # Append the clip to the list
            clips.append(final_clip)

        # Apply crossfade transitions between clips
        # Using padding to create a crossfade effect
        final_video = concatenate_videoclips(clips, padding=-transition_duration, method="compose")

        # Export the final video
        # final_video.write_videofile(output_file, fps=fps, codec='libx264')
        final_video.write_videofile(
            output_file,
            fps=fps,
            codec='libx264',
            audio_codec='aac',  # Use AAC codec to avoid compatibility issues
            threads=1  # Disable multithreading for stability
        )

        print(f"✅ Video saved as {output_file}")

        video_file = open("output.mp4", "rb")
        video_bytes = video_file.read()

        st.video(video_bytes)
                



# video_file = open("output.mp4", "rb")
# video_bytes = video_file.read()

# st.video(video_bytes)