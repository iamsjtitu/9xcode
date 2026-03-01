"""
9xCodes Promotional Video Generator - Hindi
Generates 5 short clips for combining into 1:30 min video
"""
import os, sys
from dotenv import load_dotenv
load_dotenv('/app/backend/.env')

from emergentintegrations.llm.openai.video_generation import OpenAIVideoGeneration

OUTPUT_DIR = '/app/videos'
os.makedirs(OUTPUT_DIR, exist_ok=True)

CLIPS = [
    {
        "name": "01_intro",
        "prompt": "Cinematic tech intro animation: A glowing neon blue code terminal screen appears in the center of a dark room. Hindi text '9xCodes' materializes in bold futuristic font with electric blue and purple glow effects. Code lines cascade down in the background like Matrix rain. Camera slowly zooms in. Professional, modern, dark tech aesthetic. 4K quality.",
        "duration": 12,
    },
    {
        "name": "02_problem",
        "prompt": "A young Indian developer sitting at his desk late at night, looking frustrated and stressed. Multiple browser tabs open with error messages on his screen. He holds his head in his hands. The room is dimly lit with monitor glow. Realistic, cinematic lighting, Indian office setting. The mood shifts from stress to hope as he discovers something on his screen.",
        "duration": 12,
    },
    {
        "name": "03_solution",
        "prompt": "Close-up of a laptop screen showing a beautiful modern website with code snippets and tutorials. An Indian developer's hands typing on keyboard, copy-pasting commands from the website. The screen shows clean, organized code tutorials with step-by-step instructions. Green checkmarks appear as each step completes successfully. Bright, optimistic lighting. Modern workspace with plants.",
        "duration": 12,
    },
    {
        "name": "04_features",
        "prompt": "Dynamic split-screen montage showing: server racks with blinking lights, Linux terminal commands running successfully, Docker containers deploying, SSL certificates being installed, database backups completing. Each scene transitions with smooth slide animation. Professional tech b-roll footage style. Blue and teal color grading. Fast-paced and energetic.",
        "duration": 12,
    },
    {
        "name": "05_cta",
        "prompt": "Cinematic ending shot: A confident young Indian developer smiling at camera with a modern workspace behind him. The text '9xCodes.com' appears in large glowing letters with the tagline below in Hindi. Background transitions to a beautiful gradient of blue and purple with subtle particle effects. Call-to-action style, professional and inviting. 4K cinematic.",
        "duration": 12,
    },
]

def generate_clip(clip):
    print(f"\n{'='*50}")
    print(f"Generating: {clip['name']} ({clip['duration']}s)")
    print(f"{'='*50}")
    
    output_path = f"{OUTPUT_DIR}/{clip['name']}.mp4"
    
    if os.path.exists(output_path):
        print(f"Already exists, skipping: {output_path}")
        return output_path
    
    video_gen = OpenAIVideoGeneration(api_key=os.environ['EMERGENT_LLM_KEY'])
    
    video_bytes = video_gen.text_to_video(
        prompt=clip['prompt'],
        model="sora-2",
        size="1280x720",
        duration=clip['duration'],
        max_wait_time=900
    )
    
    if video_bytes:
        video_gen.save_video(video_bytes, output_path)
        print(f"Saved: {output_path}")
        return output_path
    else:
        print(f"FAILED: {clip['name']}")
        return None

if __name__ == "__main__":
    print("9xCodes Video Generator - Starting...")
    results = []
    for clip in CLIPS:
        result = generate_clip(clip)
        results.append((clip['name'], result))
    
    print(f"\n{'='*50}")
    print("RESULTS:")
    print(f"{'='*50}")
    for name, path in results:
        status = "OK" if path else "FAILED"
        print(f"  [{status}] {name}: {path or 'N/A'}")
    print(f"\nTotal: {sum(1 for _, p in results if p)}/{len(results)} clips generated")
    print(f"Output directory: {OUTPUT_DIR}")
