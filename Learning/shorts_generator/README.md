### Docs
- https://medium.com/@oluyaled/generate-youtube-video-using-ai-ml-python-c9ba9c86f9ea
- https://github.com/pollinations/pollinations


## Steps Implemented

### Step 1: Using LLM to convert the prompt into a YT Short script and adding prompts for image generation
- Used `Ollama` along with `llama3.2:latest` model locally
```py
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

```

### Step 2: Image Generation
- Here we use the `TextToimage` generator based on Dall-E provided at https://github.com/pollinations/pollinations

### Step 3: Audio Generation
- Option 1: Using Eleven labs for TTS: https://elevenlabs.io/app/speech-synthesis/text-to-speech
- Option 2: TTS service provided by pollination.ai https://github.com/pollinations/pollinations ( Very strongly rate limited)
- Opiont 2: Local packages like ChatTTS, Google TTS ( but very robotic sounding)

### Step 4: Stich Image+Audio+Subtitles 
- Package used: https://zulko.github.io/moviepy/


## Demo Video
[![Watch the video](https://img.youtube.com/vi/qeE6xSKNpVU/maxresdefault.jpg)](https://youtu.be/qeE6xSKNpVU)
