import streamlit as st
import functionality
from debug import debug_buttons

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

# Adjusted location image size and changed caption to dynamic location name
location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
st.image(location_image, caption=functionality.location_name, width=800, output_format="PNG")


with sidebar_tabs[0]:
    # Changed player image caption to dynamic player name and included edit option
    st.image(functionality.player.image, caption=functionality.player.name, use_column_width=True)
    st.write(f"Name: {functionality.player.name}")
    st.write(f"Health: {functionality.player.stats['Health']}")
    st.write(f"Attack: {functionality.player.stats['Attack']}")
    st.write(f"Defense: {functionality.player.stats['Defense']}")

    player_details_tabs = st.sidebar.tabs(["Stats", "Equipment", "Inventory", "Thought Cabinet"])

    with player_details_tabs[0]:
        for stat, value in functionality.player.stats.items():
            # Display the total value added by equipped items in green
            additional_value = sum(item.modifier for item in functionality.player.equipment.values() if item and item.modifies == stat)
            st.write(f"{stat}: {value} {'(+ ' + str(additional_value) + ')' if additional_value else ''}")

    with player_details_tabs[1]:
        for equipment_spot, item in functionality.player.equipment.items():
            st.write(f"{equipment_spot}: {item.name if item else 'None'}")

    with player_details_tabs[2]:
        # Adjusted item display to include small images with details in grid format
        col1, col2 = st.columns(2)
        for item in functionality.player.inventory:
            with col1:
                st.image(item.image, width=50)
            with col2:
                st.write(f"{item.name}: {item.description}")

    with player_details_tabs[3]:
        # Adjusted thought cabinet display to include small images with details in grid format
        col1, col2 = st.columns(2)
        for thought in functionality.player.thought_cabinet:
            with col1:
                st.image(thought['image'], width=50)
            with col2:
                st.write(f"{thought['name']}: {thought['description']} - {thought['relevance']}")

with sidebar_tabs[1]:
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
                # Made NPC image 50% smaller
                st.image(functionality.dialogue.speakers[speaker]["image"], caption=speaker, width=300)
                for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                    st.write(f"{speaker}: {text}")
    else:
        st.write("No dialogues available.")

# Moved chat input to the bottom outside any columns as per your request
user_input = st.chat_input("Dialogue")
