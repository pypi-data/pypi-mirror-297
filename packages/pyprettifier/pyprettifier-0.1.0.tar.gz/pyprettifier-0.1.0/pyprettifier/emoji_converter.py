# pyprettifier/emoji_converter.py

emoji_dict = {
    ":smile:": "😄",
    ":heart:": "❤️",
    ":thumbs_up:": "👍",
    ":cry:": "😢",
    ":laughing:": "😆",
    ":fire:": "🔥",
    ":clap:": "👏",
    ":sunglasses:": "😎",
    ":star:": "⭐",
    ":thinking:": "🤔"
    # Add more emojis
}

class EmojiConverter:
    @staticmethod
    def convert(emoji_name):
        """
        Converts an emoji name to the actual emoji character.
        
        :param emoji_name: Emoji name in the format ':emoji_name:'
        :return: Corresponding emoji character, or a message if not found
        """
        return emoji_dict.get(emoji_name, "Emoji not found")
