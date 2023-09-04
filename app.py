import streamlit as st
import functionality
from debug import debug_buttons
from card_template import CardTemplate

if 'jump_to' not in st.session_state:
    st.session_state['jump_to'] = None

st.markdown("<div id='Title'></div>", unsafe_allow_html=True)
st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings", "Debug"])

# Adjusted location image and caption
location_image = functionality.get_image_or_placeholder('placeholder_location_image.png', 'yellow')
st.image(location_image, caption=functionality.location_name, height=300, output_format="PNG")

with sidebar_tabs[0]:
    st.image(functionality.player.image, caption=functionality.player.name)  # Updated caption to dynamic player name
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
        cards_html = CardTemplate.generate_cards_html(items_data)
        st.markdown(cards_html, unsafe_allow_html=True)

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
user_input = st.chat_input("Dialogue")
