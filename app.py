import streamlit as st
import functionality
from debug import debug_buttons


#Image placeholder
location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
st.image(location_image, caption="Location", use_column_width=True)

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
# Add a new tab labeled "Mind" in the sidebar.
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

with sidebar_tabs[0]:
    st.image(functionality.get_image_or_placeholder(functionality.player.image, 'blue'), caption="Player")
    
    player_details_tabs = st.sidebar.tabs(["Stats", "Equipment", "Inventory", "Mind"])
    
    with player_details_tabs[0]:
        st.write("Stats")
        for stat, value in functionality.player.stats.items():
            st.write(f"{stat}: {value}")

    with player_details_tabs[1]:
        st.write("Equipment")
        for part, equipment in functionality.player.equipment.items():
            st.write(f"{part}: {equipment}")

    with player_details_tabs[2]:
        st.write("Inventory")
        for item in functionality.player.inventory:
            st.image(functionality.get_image_or_placeholder(item.image, 'green'))
            st.write(f"Name: {item.name}")
            st.write(f"Modifier: {item.modifier}")
            st.write(f"Modifies: {item.modifies}")
            st.write(f"Description: {item.description}")
            
    with player_details_tabs[3]:
        st.write("Thought Cabinet")
        for thought in functionality.player.thought_cabinet:
            st.write(f"Name: {thought['name']}")
            st.write(f"Description: {thought['description']}")
            st.write(f"Relevance: {thought['relevance']}")


with sidebar_tabs[1]:
    st.file_uploader("Upload File")

with sidebar_tabs[2]:
    debug_buttons()

# Main area with columns
col1, col2 = st.columns(2)

with col1:
    user_input = st.text_input("Enter text here")
    st.text_area("Dialogue", value=user_input, height=200)

with col2:
    if functionality.dialogue.speakers:  # Checking if there are any speakers
        dialogue_tabs = st.tabs(list(functionality.dialogue.speakers.keys()))
        for speaker in functionality.dialogue.speakers:
            with dialogue_tabs[speaker]:
                st.image(functionality.get_image_or_placeholder(functionality.dialogue.speakers[speaker]["image"], 'red'), caption=speaker, use_column_width=True)
                for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                    st.write(text)
    else:
        st.write("No dialogues available.")

