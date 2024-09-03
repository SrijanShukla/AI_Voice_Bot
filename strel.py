import os
from openai import OpenAI
import streamlit as st
from streamlit_chat import message
from dotenv import load_dotenv
# from utils import get_answer, text_to_speech, autoplay_audio, speech_to_text
from audio_recorder_streamlit import audio_recorder
from streamlit_float import *

load_dotenv(".env")


# Initialize the OpenAI client
client = OpenAI()

pt = """
Introduction: Hi there! I'm here to help with any questions you have. What's on your mind today?

Part 1: Exploring Business Interests

User Prompt: Feel free to share any thoughts or questions you have about businesses, whether you're just curious or thinking about starting one. 
Bot Response: Provides a supportive and relaxed conversation, offers general advice, and encourages the user to share more if they feel comfortable, without pushing for specifics. 

Part 2: Answering Business Questions
User Prompt: If you have any specific questions about business, ask away! I'm here to help. 
Bot Response: Offers tailored advice with practical examples and keeps the conversation light and informative, ensuring the user feels supported. 

Part 3: General Discussion on Business Finances
Try to understand how the user is planning on the finances.
Use subtle prompts to encourage the user to think about additional funding, 
highlight the benefits of financial security, and gently introduce the idea of taking a well-timed loan.

User Prompt: If you're curious about business finances or funding, I can share some insights. What would you like to know? Bot Strategy: Discusses various aspects of business finances in a friendly manner, introduces concepts like budgeting and funding options without assuming the user's intent to start a business. Part 4: Introducing the Aspire App
Bot Pitch: If managing business finances sounds daunting, the Aspire App can help simplify the process. It's easy to use and can assist with applying for loans and managing your business finances. Feel free to download it from www.aspire.com. Conclusion: Thank you for chatting with me today! If you have any more questions or just want to talk more about your interests, feel free to reach out through our app or website. We're here to support you, whatever your goals may be!

Chatbot Interaction Guardrails:
Focus: Allow the user to guide the conversation, responding naturally to their queries. Brevity: Encourage concise responses to keep the conversation flowing smoothly. Scope: Maintain focus on business-related topics, but allow for a relaxed approach without pushing the user towards any specific actions. Support: Provide a supportive and friendly tone throughout, catering to users who may not be proficient in English or fully decided on starting a business.
Important: Keep the bot answers short and crisp and do not stretch the conversation too much but not at the cost of it being a natural 
conversation. Naturally go into the decided flow when you feel like it being a good time to bring in costs.
Goal: Naturally make the users download the app.
"""

# def text_to_speech(input_text):
#     response = client.audio.speech.create(
#         model="tts-1",
#         voice="nova",
#         input=input_text
#     )
#     webm_file_path = "temp_audio_play.mp3"
#     with open(webm_file_path, "wb") as f:
#         response.stream_to_file(webm_file_path)
#     return webm_file_path


# def generate_response(prompt):
#     # Prepare the conversation history
#     conversation_history = [{"role": "system", "content": pt}]
#     conversation_history.extend(st.session_state['messages'])
#     conversation_history.append({"role": "user", "content": prompt})

#     chat_completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=conversation_history,
#         max_tokens=1024,
#         n=1,
#         stop=None,
#         temperature=1.2,
#     )
#     return chat_completion.choices[0].message.content

# # Creating the chatbot interface
# st.title("Aspire Bot")


# # Initialize session state for storing chat history
# if 'messages' not in st.session_state:
#     st.session_state['messages'] = []

# # Add a greeting message if chat history is empty
# if not st.session_state['messages']:
#     st.session_state['messages'].append({"role": "assistant", "content": """Hi there! I'm here to help with any 
#                                          questions you have. What's on your mind today?"""})

# # Display chat history
# for message in st.session_state['messages']:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

# # Get user input
# if prompt := st.chat_input("Ask me anything about loans..."):
#     # Add user message to chat history
#     st.session_state['messages'].append({"role": "user", "content": prompt})

#     # Generate response from the model
#     response = generate_response(prompt)

#     # Add assistant response to chat history
#     st.session_state['messages'].append({"role": "assistant", "content": response})

#     with st.chat_message("user"):
#         st.markdown(prompt)

#     # Display the latest assistant message
#     with st.chat_message("assistant"):
#         st.markdown(response)

# footer_container = st.container()
# with footer_container:
#     audio_bytes = audio_recorder()




def text_to_speech(input_text):
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=input_text
    )
    webm_file_path = "temp_audio_play.wav"
    with open(webm_file_path, "wb") as f:
        response.stream_to_file(webm_file_path)
    return webm_file_path


def speech_to_text(audio_file):
    audio_data = open(audio_file, "rb")
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_data
    )
    return transcript.text

def generate_response(prompt):
    # Check if 'conversation_history' is in st.session_state; if not, initialize it.
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []

    st.session_state['conversation_history'] = [{"role": "system", "content": pt}]
    st.session_state['conversation_history'].extend(st.session_state['messages'])
    
    # Append the current user prompt to the session's conversation history.
    st.session_state['conversation_history'].append({"role": "user", "content": prompt})
    
    # Generate a chat completion using the updated conversation history.
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=st.session_state['conversation_history'],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=1.2,
    )
    
    # Append the model's response to the conversation history.
    st.session_state['conversation_history'].append({"role": "assistant", "content": chat_completion.choices[0].message.content})
    
    # Return the model's response.
    return chat_completion.choices[0].message.content

# Creating the chatbot interface
st.title("Aspire Bot")

# Initialize session state for storing chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Add a greeting message if chat history is empty
if not st.session_state['messages']:
    st.session_state['messages'].append({"role": "assistant", "content": "Hi there! I'm here to help with any questions you have. What's on your mind today?"})

# Display chat history
for message in st.session_state['messages']:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Record audio input
audio_bytes = audio_recorder()

# Convert audio input to text
if audio_bytes:
    st.write("Audio captured!")
    with open("temp_audio_in.wav", "wb") as f:
        f.write(audio_bytes)
    prompt = speech_to_text("temp_audio_in.wav")
    st.session_state['messages'].append({"role": "user", "content": prompt})

    # Generate response from the model
    response = generate_response(prompt)

    # Add assistant response to chat history
    st.session_state['messages'].append({"role": "assistant", "content": response})

    # Display the latest assistant message
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    # Convert response text to speech and autoplay it
    audio_path = text_to_speech(response)
    st.audio(audio_path, format="audio/wav")

# If the user prefers to type
if prompt := st.chat_input("Ask me anything about loans..."):
    st.session_state['messages'].append({"role": "user", "content": prompt})

    response = generate_response(prompt)

    st.session_state['messages'].append({"role": "assistant", "content": response})

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown(response)

    audio_path = text_to_speech(response)
    st.audio(audio_path, format="audio/wav")