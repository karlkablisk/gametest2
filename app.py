import streamlit as st
import functionality
from debug import debug_buttons

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

with sidebar_tabs[0]:
    st.image(functionality.player.image, caption="Player")
    st.write(f"Name: {functionality.player.name}")
    st.write(f"Health: {functionality.player.stats['Health']}")
    st.write(f"Attack: {functionality.player.stats['Attack']}")
    st.write(f"Defense: {functionality.player.stats['Defense']}")

    player_details_tabs = st.sidebar.tabs(["Stats", "Equipment", "Inventory", "Thought Cabinet"])

    with player_details_tabs[0]:
        for stat, value in functionality.player.stats.items():
            st.write(f"{stat}: {value}")

    with player_details_tabs[1]:
        for equipment_spot, item in functionality.player.equipment.items():
            st.write(f"{equipment_spot}: {item.name if item else 'None'}")

    with player_details_tabs[2]:
        for item in functionality.player.inventory:
            st.write(f"{item.name}: {item.description}")

    with player_details_tabs[3]:
        for thought in functionality.player.thought_cabinet:
            st.write(f"{thought['name']}: {thought['description']} - {thought['relevance']}")

with sidebar_tabs[1]:
    st.file_uploader("Upload File")

with sidebar_tabs[2]:
    debug_buttons()

# Main area with columns
col1, col2 = st.columns(2)

with col1:
    location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
    st.image(location_image, caption="Location", use_column_width=True)

with col2:
    if functionality.dialogue.speakers:
        dialogue_tabs = st.tabs(list(functionality.dialogue.speakers.keys()))  # Correct usage of st.tabs
        for i, speaker in enumerate(functionality.dialogue.speakers.keys()):
            with dialogue_tabs[i]:  # Correct way to access a tab in the tabs container
                st.image(functionality.dialogue.speakers[speaker]["image"], caption=speaker, use_column_width=True)
                for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                    st.write(f"{speaker}: {text}")
    else:
        st.write("No dialogues available.")


# Moved chat input to the bottom outside any columns as per your request
user_input = st.chat_input("Dialogue")
