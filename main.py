# import speech_recognition as sr
# import pyttsx3
# from openai import OpenAI

# # Initialize TTS engine
# engine = pyttsx3.init()

# def speak(text):
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("🎤 Listening...")
#         audio = recognizer.listen(source)
#     try:
#         print("🗣️ Recognizing...")
#         return recognizer.recognize_google(audio)
#     except sr.UnknownValueError:
#         return "Sorry, I didn't catch that."
#     except sr.RequestError:
#         return "Speech recognition service error."

# # GPT Setup
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",
#     api_key="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"
# )

# def chat_with_gpt(prompt):
#     completion = client.chat.completions.create(
#         extra_headers={
#             "HTTP-Referer": "http://localhost",  # You can customize this
#             "X-Title": "VoiceBot",
#         },
#         model="openai/gpt-4o",
#         messages=[
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=2048
#     )
#     return completion.choices[0].message.content

# # 🔁 Main loop
# while True:
#     user_input = listen()
#     if user_input.lower() in ["exit", "quit", "stop"]:
#         speak("Goodbye!")
#         break

#     print(f"User: {user_input}")
#     response = chat_with_gpt(user_input)
#     print(f"GPT: {response}")
#     speak(response)

import tkinter as tk
import threading
import speech_recognition as sr
import pyttsx3
from openai import OpenAI

# Set up OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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"
)

# Set up TTS engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Chat function using OpenRouter GPT
def chat_with_gpt(prompt):
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "http://localhost",
                "X-Title": "VoiceBot"
            },
            model="openai/gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2048
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Voice listening
def listen_and_respond():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        chat_log.insert(tk.END, "🎤 Listening...\n")
        app.update()
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        chat_log.insert(tk.END, f"You: {user_input}\n")
        app.update()
        response = chat_with_gpt(user_input)
        chat_log.insert(tk.END, f"GPT: {response}\n\n")
        speak(response)
    except sr.UnknownValueError:
        chat_log.insert(tk.END, "Could not understand audio\n")
    except sr.RequestError:
        chat_log.insert(tk.END, "Speech recognition service error\n")

# Threaded call to avoid GUI freeze
def start_listening():
    threading.Thread(target=listen_and_respond).start()

# GUI Setup
app = tk.Tk()
app.title("🎙️ VoiceBot - GPT-4o")
app.geometry("500x500")

chat_log = tk.Text(app, wrap=tk.WORD, font=("Arial", 12))
chat_log.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

listen_button = tk.Button(app, text="🎤 Speak", font=("Arial", 14), command=start_listening)
listen_button.pack(pady=10)

exit_button = tk.Button(app, text="❌ Exit", font=("Arial", 12), command=app.quit)
exit_button.pack(pady=5)

app.mainloop()
