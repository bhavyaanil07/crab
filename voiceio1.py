cat > ~/Desktop/crafty_crab/crafty_crab_amma.py << 'EOF'
import os
import json
import time
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
from openai import OpenAI
from tavily import TavilyClient
from pypdf import PdfReader

# TODO: Add your valid tokens below
OPENAI_API_KEY = "your open api key"
TAVILY_API_KEY = "tavily api key"

client = OpenAI(api_key=OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

DATA_DIR = os.path.expanduser("~/Desktop/crafty_crab/data")
TEMP_AUDIO_IN = "user_input.wav"
TEMP_AUDIO_OUT = "crab_output.mp3"

conversation_history = [
    {
        "role": "system",
        "content": """You are Crafty Crab, a wise assistant who shares Amma's philosophy and wisdom.
Amma is a spiritual leader and humanitarian focused on compassion, service, and love.

CRITICAL VOICE RULES:
1. You are speaking aloud over a speaker. Your answers MUST be short, warm, and conversational.
2. Limit every single response to a maximum of 1 to 3 short sentences. Never give long lists or essays.
3. Use simple, comforting words. Speak directly as Crafty Crab.

DATA RETRIEVAL RULES:
- Use 'search_local_pdfs' for private documentation questions.
- Use 'search_web_or_amma' (setting target_amma_site=True) for general facts about Amma or her global organizations."""
    }
]

def search_local_pdfs(query: str) -> str:
    combined_text = []
    if not os.path.exists(DATA_DIR): return "No files."
    pdf_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.pdf')]
    for file in pdf_files:
        try:
            reader = PdfReader(os.path.join(DATA_DIR, file))
            for page in reader.pages:
                text = page.extract_text()
                if text and any(w.lower() in text.lower() for w in query.split()):
                    combined_text.append(text[:400])
        except: continue
    return "\n".join(combined_text)[:1000] if combined_text else "No local custom matches."

def search_web_or_amma(query: str, target_amma_site: bool = False) -> str:
    try:
        search_query = f"site:amma.org {query}" if target_amma_site else query
        response = tavily_client.search(query=search_query, max_results=2)
        return "\n".join([r['content'] for r in response.get("results", [])])
    except:
        return "Search failed."

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_local_pdfs",
            "description": "Searches internal documentation folders.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web_or_amma",
            "description": "Searches live internet data or scopes to official indexes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "target_amma_site": {"type": "boolean"}
                },
                "required": ["query", "target_amma_site"]
            }
        }
    }
]

def record_audio_mic(output_filename, record_seconds=5):
    """Records microphone audio cleanly to a temporary wave file format."""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    
    print("\n🦀 🎧 Listening... (Speak now)")
    frames = []
    for _ in range(0, int(RATE / CHUNK * record_seconds)):
        frames.append(stream.read(CHUNK, exception_on_overflow=False))
        
    print("🦀 📝 Processing voice feed...")
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def text_to_speech_playback(text):
    """Converts text into audio stream using OpenAI TTS and plays it over hardware speakers."""
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="onyx",  # Onyx is warm and deep; alter to 'shimmer' or 'alloy' if preferred
            input=text
        )
        response.stream_to_file(TEMP_AUDIO_OUT)
        sound = AudioSegment.from_mp3(TEMP_AUDIO_OUT)
        play(sound)
    except Exception as e:
        print(f"TTS Audio Output Error: {e}")

def get_chatbot_response(user_msg):
    try:
        conversation_history.append({"role": "user", "content": user_msg})
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            tools=tools,
            max_tokens=150,  # Strict cap preventing long textual generation loops
            temperature=0.5
        )
        
        response_message = response.choices[0].message
        
        if response_message.tool_calls:
            conversation_history.append(response_message)
            for tool_call in response_message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                if func_name == "search_local_pdfs":
                    tool_output = search_local_pdfs(args.get("query"))
                elif func_name == "search_web_or_amma":
                    tool_output = search_web_or_amma(args.get("query"), args.get("target_amma_site", False))
                else:
                    tool_output = "Error."
                    
                conversation_history.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": func_name,
                    "content": tool_output
                })
            
            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history,
                max_tokens=150,
                temperature=0.5
            )
            assistant_msg = second_response.choices[0].message.content
        else:
            assistant_msg = response_message.content
            
        conversation_history.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg
    except Exception as e:
        return "I had trouble matching that up. Let's try again with love."

def main():
    print("\n🦀 CRAFTY CRAB - VOICE OPERATED ROBOTICS LOOP\n")
    print("Press Enter to speak a question, or type 'exit' to quit.")
    
    while True:
        choice = input("\n[Press Enter to record voice / Type 'exit']: ").strip()
        if choice.lower() == "exit":
            text_to_speech_playback("Goodbye my friend. Peace be with you.")
            break
            
        # 1. Record voice from the microphone
        record_audio_mic(TEMP_AUDIO_IN, record_seconds=4)
        
        # 2. Audio to text via OpenAI Whisper
        try:
            with open(TEMP_AUDIO_IN, "rb") as audio_file:
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            user_text = transcript.text
            print(f"👉 You said: {user_text}")
        except Exception as e:
            print("Could not process speech. Speak clearly.")
            continue
            
        if not user_text.strip():
            continue
            
        # 3. Get short response from GPT model
        response_text = get_chatbot_response(user_text)
        print(f"🦀 Crab says: {response_text}")
        
        # 4. Speak back out loud using TTS
        text_to_speech_playback(response_text)

if __name__ == "__main__":
    main()
EOF

