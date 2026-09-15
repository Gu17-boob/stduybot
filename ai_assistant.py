import ollama


MODEL_NAME = "qwen2.5"


def ask_ai(question, chat_history=None):
    """
    Send a question to Ollama with previous conversation context.
    """

    question = question.strip()

    if not question:
        return "Please enter a question."

    if chat_history is None:
        chat_history = []

    try:

        messages = [
            {
                "role": "system",
                "content": (
                    "You are StudyBot, a helpful academic AI assistant. "
                    "Explain concepts clearly and simply. "
                    "Use examples when useful. "
                    "Help students understand concepts rather than "
                    "only giving short answers."
                )
            }
        ]

        # Add previous conversation
        for chat in chat_history:

            messages.append(
                {
                    "role": "user",
                    "content": chat["user"]
                }
            )

            messages.append(
                {
                    "role": "assistant",
                    "content": chat["assistant"]
                }
            )

        # Add current question
        messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        response = ollama.chat(
            model=MODEL_NAME,
            messages=messages
        )

        return response["message"]["content"]

    except Exception as error:

        return (
            "Unable to connect to the AI model.\n\n"
            f"Error: {error}\n\n"
            f"Make sure Ollama is running and '{MODEL_NAME}' "
            "is installed."
        )