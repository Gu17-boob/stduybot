import ollama


MODEL_NAME = "qwen2.5"


def summarize_notes(notes):
    """
    Summarize study notes using Ollama.
    """

    notes = notes.strip()

    if not notes:
        return "Please enter some notes to summarize."

    prompt = f"""
Summarize the following study notes.

Provide the result in this format:

## Summary
Give a clear and concise summary.

## Key Points
- Point 1
- Point 2
- Point 3
- Point 4
- Point 5

## Important Terms
List the important technical terms and briefly explain them.

## Quick Revision
Give 3-5 short points that a student can remember before an exam.

Study Notes:
{notes}
"""

    try:

        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are StudyBot, an academic notes "
                        "summarization assistant. Make study material "
                        "clear, accurate, and easy to revise."
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

        return f"Unable to summarize notes: {error}"