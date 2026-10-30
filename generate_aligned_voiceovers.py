import os
import json
import base64
import urllib.request
import time

def get_api_key():
    key = os.environ.get("ELEVENLABS_API_KEY")
    if key:
        return key
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("ELEVENLABS_API_KEY="):
                    return line.split("=", 1)[1].strip()
    return ""

API_KEY = get_api_key()
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb" # George - Warm, Captivating Storyteller
MODEL_ID = "eleven_turbo_v2_5"

AUDIO_DIR = os.path.join("app", "static", "audio")
os.makedirs(AUDIO_DIR, exist_ok=True)

SCENES = [
    {
        "id": "scene_1",
        "title": "The Sundowning Crisis",
        "text": "Every evening at sundown, millions of dementia patients experience acute neurological terror. In memory care, it’s known as Sundowning: sudden, overwhelming agitation. For decades, the standard response has been chemical sedation: dangerous antipsychotics that strip away human dignity and violate federal guidelines. What if memory care didn't require pills?"
    },
    {
        "id": "scene_2",
        "title": "Meet NeuroTaste",
        "text": "Meet NeuroTaste: the world’s first autonomous, contactless memory care de-escalation agent. Using standard RGB computer vision, NeuroTaste reads microscopic arterial blood volume pulses beneath facial skin, calculating autonomic distress without a single wire or wearable. And when agitation strikes, NeuroTaste doesn't call for sedation. It activates something infinitely more powerful."
    },
    {
        "id": "scene_3",
        "title": "The Dementia Paradox & The Qloo Taste Graph",
        "text": "Neuroscientists call it the Dementia Paradox: while degenerative illness destroys short-term episodic memory, the brain’s cultural taste cortex remains vividly alive until the end of life. NeuroTaste bridges this gap using the Qloo Taste Graph API, mapping the resident's birth decade, cultural geography, and dormant sensory anchors to surface music, cinema, and scents proven to evoke emotional calm."
    },
    {
        "id": "scene_4",
        "title": "Autonomous Live Intervention",
        "text": "Watch what happens in real time. Without a single nurse touching a syringe, NeuroTaste deploys an autonomous sensory de-escalation protocol. A 1940s acoustic recording of Nat King Cole softly fills the room, while smart lighting transitions to a soothing sunset twilight. Within two minutes, heart rate stabilizes, vagal tone rebounds, and the agitation storm dissolves peacefully."
    },
    {
        "id": "scene_5",
        "title": "Clinical Proof & Regulatory Moat",
        "text": "For healthcare facilities, NeuroTaste isn't just compassionate care—it’s an enterprise regulatory shield. Fully compliant with federal CMS F-Tag 758 mandates restricting unnecessary psychotropic medications, it reduces caregiver burnout and institutional liability through continuous, edge-computed twenty-four-seven care."
    },
    {
        "id": "scene_6",
        "title": "The Call to Action",
        "text": "Dementia steals memories. But with Qloo and NeuroTaste, we can bring their calm, their dignity, and their humanity back. NeuroTaste: Autonomous Memory Care, powered by cultural intelligence."
    }
]

def chars_to_words(characters, start_times, end_times):
    words = []
    current_word = ""
    word_start = None
    word_end = None
    
    for i, ch in enumerate(characters):
        if ch.isspace():
            if current_word:
                words.append({
                    "word": current_word,
                    "start": round(word_start, 3),
                    "end": round(word_end, 3)
                })
                current_word = ""
                word_start = None
                word_end = None
        else:
            if word_start is None:
                word_start = start_times[i]
            word_end = end_times[i]
            current_word += ch
            
    if current_word:
        words.append({
            "word": current_word,
            "start": round(word_start, 3),
            "end": round(word_end, 3)
        })
        
    return words

def generate_aligned_scene(sc_id, text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/with-timestamps"
    payload = {
        "text": text,
        "model_id": MODEL_ID,
        "voice_settings": {
            "stability": 0.55,
            "similarity_boost": 0.82,
            "style": 0.15,
            "use_speaker_boost": True
        }
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            "xi-api-key": API_KEY,
            "Content-Type": "application/json",
            "User-Agent": "NeuroTaste/1.0"
        }
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        
        # 1. Save Audio MP3
        audio_bytes = base64.b64decode(res["audio_base64"])
        audio_path = os.path.join(AUDIO_DIR, f"{sc_id}.mp3")
        with open(audio_path, "wb") as f:
            f.write(audio_bytes)
            
        # 2. Extract Alignments
        align = res.get("alignment", {})
        chars = align.get("characters", [])
        starts = align.get("character_start_times_seconds", [])
        ends = align.get("character_end_times_seconds", [])
        
        words = chars_to_words(chars, starts, ends)
        return len(audio_bytes), words

def main():
    print(f"[*] Starting Precision Alignment Generation for all 6 scenes...")
    timings_data = {}
    
    for i, sc in enumerate(SCENES):
        print(f"[{i+1}/6] Generating {sc['title']} with microsecond timestamps...")
        try:
            size, words = generate_aligned_scene(sc["id"], sc["text"])
            timings_data[sc["id"]] = words
            print(f"    [+] Saved {sc['id']}.mp3 ({size} bytes) with {len(words)} aligned words.")
            if words:
                print(f"        First word: '{words[0]['word']}' @ {words[0]['start']}s -> Last word: '{words[-1]['word']}' @ {words[-1]['end']}s")
        except Exception as e:
            print(f"    [-] Error on {sc['id']}: {e}")
        time.sleep(0.5)
        
    timings_path = os.path.join(AUDIO_DIR, "scene_timings.json")
    with open(timings_path, "w", encoding="utf-8") as f:
        json.dump(timings_data, f, indent=2)
    print(f"\n[+] SUCCESS! Word timings saved to {timings_path}")

if __name__ == "__main__":
    main()
