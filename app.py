import streamlit as st
import functionality
from debug import debug_buttons

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings"])
with sidebar_tabs[0]:
    st.image(functionality.player.image, caption="Player")
    st.write("Stats")
    for stat, value in functionality.player.stats.items():
        st.write(f"{stat}: {value}")

    st.write("Equipment")
    for part, equipment in functionality.player.equipment.items():
        st.write(f"{part}: {equipment}")

    st.write("Inventory")
    for item in functionality.player.inventory:
        st.image(item.image)
        st.write(f"Name: {item.name}")
        st.write(f"Modifier: {item.modifier}")
        st.write(f"Modifies: {item.modifies}")
        st.write(f"Description: {item.description}")

with sidebar_tabs[1]:
    st.file_uploader("Upload File")

# Main area with tabs
main_tabs = st.tabs(["Location", "Dialogue"])
with main_tabs[0]:
    st.image(functionality.get_image_or_placeholder("placeholder_location_image.png", "yellow"), caption="Location")
    
st.chat_input("Enter text here") 

with main_tabs[1]:
    dialogue_tabs = st.tabs(list(functionality.dialogue.speakers.keys()))
    for speaker in functionality.dialogue.speakers:
        with dialogue_tabs[speaker]:
            st.image(functionality.dialogue.speakers[speaker]["image"], caption=speaker)
            for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                st.write(text)


debug_buttons()