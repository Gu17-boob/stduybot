import ollama


MODEL_NAME = "qwen2.5"


def generate_quiz(topic, number_of_questions=5):
    """
    Generate a multiple-choice quiz using Ollama.
    """

    topic = topic.strip()

    if not topic:
        return "Please enter a topic."

    prompt = f"""
Create a {number_of_questions}-question multiple-choice quiz
about {topic}.

For every question provide:

Question:
A)
B)
C)
D)
Correct Answer:
Explanation:

Keep the questions suitable for a college student.
Make the answers accurate and easy to understand.
"""

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StudyBot, an academic quiz generator. "
                        "Create accurate educational quizzes."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as error:

        return f"Unable to generate quiz: {error}"