import streamlit as st
from functionality import player, dialogue, Item

st.title('Text-based Tabletop RPG')

# Sidebar with tabs
sidebar_tabs = st.sidebar.tabs(["Profile", "Settings"])
with sidebar_tabs[0]:
    st.image(player.image, caption="Player")
    st.write("Stats")
    for stat, value in player.stats.items():
        st.write(f"{stat}: {value}")

    st.write("Equipment")
    for part, equipment in player.equipment.items():
        st.write(f"{part}: {equipment}")

    st.write("Inventory")
    for item in player.inventory:
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
    st.image("placeholder_location_image.png", caption="Location")
    st.chat_input("Enter text here")

with main_tabs[1]:
    dialogue_tabs = st.tabs(list(dialogue.speakers.keys()))
    for speaker in dialogue.speakers:
        with dialogue_tabs[speaker]:
            st.image(dialogue.speakers[speaker]["image"], caption=speaker)
            for text in dialogue.speakers[speaker]["dialogues"]:
                st.write(text)

# Debug buttons
if st.button("Toggle Debug Buttons"):
    if st.button("Add Item"):
        player.inventory.append(Item("placeholder_item_image.png", "Sword", "+10", "Attack", "A sharp sword."))
    if st.button("Add Dialogue"):
        dialogue.add_speaker("NPC1", "placeholder_npc1_image.png")
        dialogue.add_dialogue("NPC1", "Hello!")
