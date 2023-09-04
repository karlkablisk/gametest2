import streamlit as st
import functionality

def debug_buttons():
    st.session_state.get("show_debug_buttons", False)
    if st.button("Toggle Debug Buttons"):
        st.session_state.show_debug_buttons = not st.session_state.show_debug_buttons

    if st.session_state.show_debug_buttons:
        if st.button("Add Item"):
            functionality.player.inventory.append(functionality.Item("placeholder_item_image.png", "Sword", "+10", "Attack", "A sharp sword."))
        
        if st.button("Add Dialogue"):
            functionality.dialogue.add_speaker("NPC1", "placeholder_npc1_image.png")
            functionality.dialogue.add_dialogue("NPC1", "Hello!")
