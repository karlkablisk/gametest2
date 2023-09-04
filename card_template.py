class CardTemplate:
    CARD_CSS = """
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: 10px;
    }
    .card {
        border: 1px solid #000;
        padding: 10px;
        background-color: #f8f8f8;
        text-align: center;
    }
    .card img {
        max-width: 100%;
        border-bottom: 1px solid #000;
        margin-bottom: 10px;
    }
    .card .name {
        font-weight: bold;
        margin-bottom: 5px;
    }
    .card .description {
        font-size: 0.9em;
    }
    .location-image-container {
        border: 2px solid #000;
        border-radius: 15px;
        overflow: hidden;
        height: 300px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #f8f8f8;
    }
    .location-image-container img {
        object-fit: contain;
        width: 100%;
        max-height: 100%;
    }
    """

    @staticmethod
    def generate_card_html(item_or_thought):
        return f"""
        <div class="card">
            <img src="{item_or_thought['image']}" alt="{item_or_thought['name']}" />
            <div class="name">{item_or_thought['name']}</div>
            <div class="description">{item_or_thought['description']}{' - ' + item_or_thought['relevance'] if 'relevance' in item_or_thought else ''}</div>
        </div>
        """

    @classmethod
    def generate_cards_html(cls, items_or_thoughts):
        cards_html = "".join(cls.generate_card_html(item_or_thought) for item_or_thought in items_or_thoughts)
        return f"<style>{cls.CARD_CSS}</style><div class='card-container'>{cards_html}</div>"
