#app.py - main app to start things and all streamlit interface
import streamlit as st
import os

#Langchain
from langchain.callbacks.base import BaseCallbackHandler
from langchain.memory.chat_message_histories import StreamlitChatMessageHistory
from langchain.schema import ChatMessage
from langchain.tools import BaseTool, StructuredTool, Tool, tool

#chars
import importlib
folder_name = "chars"
for filename in os.listdir(folder_name):
    if filename.endswith(".py") and not filename.startswith("__"):
        module_name = filename[:-3]  # remove the .py extension
        module = importlib.import_module(f"{folder_name}.{module_name}")
#Chars all imported

#file import
from debug import debug_buttons
from card_template import CardTemplate
import functionality


class StreamHandler(BaseCallbackHandler):

    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text
        self.should_stream = False
        self.word_count = 0
        self.ignore_flag = False
        self.last_flash = time.time()

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.word_count += len(token.split())

        # Display a flashing line bar while waiting for a decision
        if time.time() - self.last_flash >= 0.5:
            self.last_flash = time.time()
            self.container.write("|")
        
        if self.word_count >= 2:
            if self.text.startswith("Action Input:") or self.text.startswith("Observation:") or self.text.startswith("Thought:") or self.text.startswith("Thoughts:"):
                self.ignore_flag = True

            if "Final Answer:" in self.text:
                self.ignore_flag = False
                self.should_stream = True

            elif ":" not in self.text:
                self.should_stream = True

            if self.should_stream and not self.ignore_flag:
                final_text = self.text.split("Final Answer:")[-1].split("Alice:")[-1].strip()
                self.container.write(final_text)



if 'jump_to' not in st.session_state:
    st.session_state['jump_to'] = None

st.markdown("<div id='Title'></div>", unsafe_allow_html=True)
st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

# Adjusted location image and caption
st.markdown("<div id='location_image' style='height: 300px; overflow: hidden;'>", unsafe_allow_html=True)
location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
st.markdown("""
<div class='location-image-container' style='border: 2px solid #000; border-radius: 15px; overflow: hidden; height: 300px; display: flex; align-items: center; justify-content: center; background-color: #f8f8f8;'>
    <img src="{location_image}" alt="Location Image" style='object-fit: contain; width: 100%; max-height: 100%;'>
</div>
""", unsafe_allow_html=True)

with sidebar_tabs[0]:
    st.markdown("<div id='player_image' style='height: 300px; overflow: hidden;'>", unsafe_allow_html=True)
    st.image(functionality.player.image, caption=functionality.player.name)  
    st.markdown("</div>", unsafe_allow_html=True)
    st.write(f"Name: {functionality.player.name}")
    st.write(f"Health: {functionality.player.stats['Health']}")
    st.write(f"Attack: {functionality.player.stats['Attack']}")
    st.write(f"Defense: {functionality.player.stats['Defense']}")

    player_details_tabs = st.sidebar.tabs(["Stats", "Equipment", "Inventory", "Thought Cabinet"])

    with player_details_tabs[0]:
        st.markdown("<div id='Player_Stats'></div>", unsafe_allow_html=True)
        for stat, value in functionality.player.stats.items():
            additional_value = sum(item.modifier for item in functionality.player.equipment.values() if item and item.modifies == stat)
            st.write(f"{stat}: {value} {'(+ ' + str(additional_value) + ')' if additional_value else ''}")

    with player_details_tabs[1]:
        st.markdown("<div id='Player_Equipment'></div>", unsafe_allow_html=True)
        for equipment_spot, item in functionality.player.equipment.items():
            st.write(f"{equipment_spot}: {item.name if item else 'None'}")

    with player_details_tabs[2]:
        st.markdown("<div id='Player_Inventory'></div>", unsafe_allow_html=True)
        items_data = [{'image': item.image, 'name': item.name, 'description': item.description} for item in functionality.player.inventory]
        CardTemplate.generate_cards_html(items_data)

    with player_details_tabs[3]:
        st.markdown("<div id='Player_Thought_Cabinet'></div>", unsafe_allow_html=True)
        thought_data = [{'image': thought['image'], 'name': thought['name'], 'description': thought['description'], 'relevance': thought['relevance']} for thought in functionality.player.thought_cabinet]
        cards_html = CardTemplate.generate_cards_html(thought_data)
        st.markdown(cards_html, unsafe_allow_html=True)

with sidebar_tabs[1]:
    st.markdown("<div id='Upload_File'></div>", unsafe_allow_html=True)
    st.file_uploader("Upload File")

with sidebar_tabs[2]:
    debug_buttons()

# Main area with columns
col1, col2 = st.columns(2)

with col1:
    pass  

with col2:
    if functionality.dialogue.speakers:
        dialogue_tabs = st.tabs(list(functionality.dialogue.speakers.keys()))
        for i, speaker in enumerate(functionality.dialogue.speakers.keys()):
            with dialogue_tabs[i]:
                st.image(functionality.dialogue.speakers[speaker]["image"], caption=speaker, width=300)
                for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                    st.write(f"{speaker}: {text}")
    else:
        st.write("No dialogues available.")

# Moved chat input to the bottom outside any columns
st.markdown("<div id='Dialogue_Area'></div>", unsafe_allow_html=True)
#prompt = st.chat_input("Type here!")

user_avatar = "https://ai-scool.com/sites/default/files/styles/thumbnail/public/pictures/2023-08/geahtr%201.png?itok=onQcEWJF"
ai_avatar = "https://ai-scool.com/sites/default/files/2023-08/ai-generated-gddd745293_1280_0.png"


  
    # Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'msg_containers' not in st.session_state:
    st.session_state.msg_containers = []

    #for loop for chat history
for message in st.session_state.messages:
    with st.chat_message(message["type"], avatar=message["avatar"]):
        st.write(message["content"])


if prompt:= st.chat_input(placeholder="Type here!!"):
    st.session_state.messages.append({"type": "user", "content": prompt, "avatar": user_avatar})

        # Display user's message immediately
    with st.chat_message("user", avatar=user_avatar):
        st.write(prompt)

    with st.chat_message("assistant", avatar=ai_avatar):
            stream_handler = StreamHandler(st.empty())
            #stream_handler = StreamHandler(ai_placeholder)
            st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
            # Capture the streaming text
            response = chefbot(prompt, callbacks=[stream_handler, st_cb])
            # Extract the 'output' value from new_response after streaming
            new_result = response['output']

             # Append AI's message to st.session_state.messages
            st.session_state.messages.append({"type": "assistant", "content": new_result, "avatar": ai_avatar})
