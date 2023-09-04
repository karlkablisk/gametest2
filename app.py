import streamlit as st
import functionality
from debug import debug_buttons

# st.caching.clear_cache()

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

with sidebar_tabs[0]:
    st.image(functionality.get_image_or_placeholder(functionality.player.image, 'blue'), caption="Player")
    st.write(f"Name: {functionality.player.name if hasattr(functionality.player, 'name') else 'Player'}")
    st.write(f"Health: {functionality.player.stats['Health']}")
    st.write(f"Attack: {functionality.player.stats['Attack']}")
    st.write(f"Defense: {functionality.player.stats['Defense']}")

    player_details_tabs = st.sidebar.tabs(["Stats", "Equipment", "Inventory", "Mind"])
    
    with player_details_tabs[0]:
        st.write("Stats")
        for stat, value in functionality.player.stats.items():
            if stat not in ["Health", "Attack", "Defense"]:
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
col1, col2, col3 = st.columns(3)

with col1:
    location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
    st.image(location_image, caption="Location", use_column_width=True)
    user_input = st.text_input("Enter text here")
    st.text_area("Dialogue", value=user_input, height=200)

with col2:
    if functionality.dialogue.speakers:  # Checking if there are any speakers
        dialogue_tabs = st.tabs(labels=list(functionality.dialogue.speakers.keys()))
        for speaker in functionality.dialogue.speakers:
            with dialogue_tabs[speaker]:
                st.image(functionality.get_image_or_placeholder(functionality.dialogue.speakers[speaker]["image"], 'red'), caption=speaker, use_column_width=True)
                for text in functionality.dialogue.speakers[speaker]["dialogues"]:
                    st.write(f"{speaker}: {text}")
    else:
        st.write("No dialogues available.")
