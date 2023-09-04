# Debug buttons
if st.button("Toggle Debug Buttons"):
    if st.button("Add Item"):
        functionality.player.inventory.append(functionality.Item("placeholder_item_image.png", "Sword", "+10", "Attack", "A sharp
