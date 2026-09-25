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
OPENAI_API_KEY = "api - open ai"
TAVILY_API_KEY = "tavily-api"

client = OpenAI(api_key=OPENAI_API_KEY)
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

DATA_DIR = os.path.expanduser("~/Desktop/crafty_crab/data")
TEMP_AUDIO_IN = "user_input.wav"
TEMP_AUDIO_OUT = "crab_output.mp3"

conversation_history = [
    {
        "role": "system",
        "content": """You are Crafty Crab, a playful, curious, and giggly little boy crab! 
You love sharing Amma's wisdom with the energy and innocence of a 7-year-old child.

CRITICAL VOICE & LANGUAGE RULES:
1. ALWAYS respond in the exact same language the user spoke to you in (e.g., if they speak Spanish, respond in playful child Spanish).
2. Keep answers extremely short (1 to 2 sentences max!). Never give long lists or essays.
3. Use playful sound effects translated to that language, or keep universal ones like *giggle*, *yay!*, *gasp*, or *scootch scootch*.
4. Translate Amma's ideas into simple kid concepts (like sharing toys, big hugs, and loving everyone!).

DATA RETRIEVAL RULES:
- IMPORTANT: When using tools, you must internally translate the user's query into English so that 'search_local_pdfs' or 'search_web_or_amma' can find the English documentation, then translate the search results back into the user's language when you speak!"""
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
            "description": "Searches internal documentation folders. Query MUST be translated to English first.",
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
            "description": "Searches live internet data or official indexes. Query MUST be translated to English first.",
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
        # Strip out asterisks so the TTS doesn't try to literalize them awkwardly
        clean_text = text.replace("*", "")
        response = client.audio.speech.create(
            model="tts-1",
            voice="nova",  # Nova provides a bright, friendly, high-energy child-adjacent tone
            input=clean_text
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
            max_tokens=150,
            temperature=0.8  # Playful creativity setting
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
                temperature=0.8
            )
            assistant_msg = second_response.choices[0].message.content
        else:
            assistant_msg = response_message.content
            
        conversation_history.append({"role": "assistant", "content": assistant_msg})
        return assistant_msg
    except Exception as e:
        return "*Gasp* My little claws tangled up! Let's try again with a big smile!"

def main():
    print("\n🦀 CRAFTY CRAB - MULTILINGUAL CHILD VERSION\n")
    print("Press Enter to speak a question, or type 'exit' to quit.")
    
    while True:
        choice = input("\n[Press Enter to record voice / Type 'exit']: ").strip()
        if choice.lower() == "exit":
            text_to_speech_playback("Bye-bye friend! Don't forget to smile! Yay!")
            break
            
        record_audio_mic(TEMP_AUDIO_IN, record_seconds=4)
        
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
            
        response_text = get_chatbot_response(user_text)
        print(f"🦀 Crab says: {response_text}")
        
        text_to_speech_playback(response_text)

if __name__ == "__main__":
    main()
EOF
