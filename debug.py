import streamlit as st
import functionality

def debug_buttons():
    st.write("## Debug Tools")
   
    if st.button("Clear Cache"):
        st.caching.clear_cache()

    # Add NPC
    with st.expander("Add NPC"):
        npc_name = st.text_input("NPC Name")
        npc_image = st.text_input("NPC Image Path (e.g., 'path/to/image.png')")
        npc_color = st.color_picker("NPC Image Placeholder Color", '#808080')
        if st.button("Add NPC"):
            functionality.dialogue.add_speaker(npc_name, functionality.get_image_or_placeholder(npc_image, npc_color))
    
    # Make NPC talk
    with st.expander("Make NPC Talk"):
        speaker_name = st.selectbox("Select NPC", list(functionality.dialogue.speakers.keys()))
        text_to_add = st.text_input("Dialogue Text")
        if st.button("Add Dialogue"):
            functionality.dialogue.add_dialogue(speaker_name, text_to_add)
    
    # Modify Stats
    with st.expander("Modify Stats"):
        stat_to_modify = st.selectbox("Select Stat to Modify", list(functionality.player.stats.keys()))
        value_to_add = st.number_input("Value to Add/Subtract", value=0)
        if st.button("Modify Stat"):
            functionality.player.stats[stat_to_modify] += value_to_add

    # Load New Location
    with st.expander("Load New Location"):
        new_location_path = st.text_input("New Location Image Path (e.g., 'path/to/image.png')")
        new_location_color = st.color_picker("New Location Image Placeholder Color", '#808080')
        if st.button("Load New Location"):
            st.image(functionality.get_image_or_placeholder(new_location_path, new_location_color), caption="Location", use_column_width=True)

    # Set Player Image
    with st.expander("Set Player Image"):
        new_image_path = st.text_input("New Player Image Path (e.g., 'path/to/image.png')")
        new_image_color = st.color_picker("New Player Image Placeholder Color", '#808080')
        if st.button("Set New Player Image"):
            functionality.player.image = functionality.get_image_or_placeholder(new_image_path, new_image_color)
            st.image(functionality.player.image, caption="Player", use_column_width=True)

    # Add Item
    with st.expander("Add Item"):
        item_image_path = st.text_input("Item Image Path (e.g., 'path/to/image.png')")
        item_image_color = st.color_picker("Item Image Placeholder Color", '#808080')
        item_name = st.text_input("Item Name")
        item_modifier = st.number_input("Item Modifier", value=0)
        modifies = st.text_input("Modifies")
        description = st.text_input("Description")
        if st.button("Add Item"):
            new_item = functionality.Item(functionality.get_image_or_placeholder(item_image_path, item_image_color), item_name, item_modifier, modifies, description)
            functionality.player.inventory.append(new_item)

    # Equip Item
    with st.expander("Equip Item"):
        equipment_spot = st.selectbox("Select Equipment Spot", list(functionality.player.equipment.keys()))
        item_to_equip = st.selectbox("Select Item to Equip", [item.name for item in functionality.player.inventory])
        if st.button("Equip Item"):
            functionality.player.equipment[equipment_spot] = next(item for item in functionality.player.inventory if item.name == item_to_equip)

    with st.expander("Add to Thought Cabinet"):
        thought_name = st.text_input("Thought Name")
        thought_description = st.text_input("Thought Description")
        thought_relevance = st.text_input("Thought Relevance")
        if st.button("Add Thought"):
            new_thought = {'name': thought_name, 'description': thought_description, 'relevance': thought_relevance}
            functionality.player.thought_cabinet.append(new_thought)