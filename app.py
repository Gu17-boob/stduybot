import streamlit as st
from datetime import datetime

from calculator import solve_expression
from study_qa import answer_question
from ai_assistant import ask_ai
from quiz_generator import generate_quiz
from summarizer import summarize_notes


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="StudyBot",
    page_icon="🤖",
    layout="centered"
)
# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🤖 StudyBot")

    st.write("Your AI-powered study assistant.")

    st.divider()

    st.subheader("📚 Features")

    feature = st.radio(
        "Choose a feature",
        [
            "🏠 Home",
            "🧮 Mathematics Solver",
            "📚 Study Q&A",
            "🤖 AI Study Assistant",
            "📝 Quiz Generator",
            "📄 Notes Summarizer"
        ]
    )

    st.divider()

    st.subheader("ℹ️ About")

    st.write(
        "StudyBot is a student-focused AI application "
        "designed to help with learning, problem solving, "
        "revision, quizzes, and study notes."
    )
# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ============================================================
# TITLE
# ============================================================

st.title("🤖 StudyBot")
st.caption("Your AI-powered personal study assistant")

st.write(
    "Your personal study assistant."
)


# ============================================================
# CURRENT DATE & TIME
# ============================================================

st.divider()

st.subheader("🕐 Current Date & Time")

current_time = datetime.now()

st.info(
    current_time.strftime("%d-%m-%Y | %I:%M:%S %p")
)


# ============================================================
# WELCOME SECTION
# ============================================================

st.divider()

st.subheader("📚 Welcome!")

st.write(
    "StudyBot will help you with mathematics, "
    "academic questions, explanations, quizzes, "
    "and more."
)


# ============================================================
# MATHEMATICS SOLVER
# ============================================================

st.divider()

st.subheader("🧮 Mathematics Solver")

expression = st.text_input(
    "Enter a mathematical expression",
    placeholder="Example: 2*x + 5 = 15"
)


if st.button("Solve", key="solve_button"):

    if expression.strip():

        result, error = solve_expression(expression)

        if error:

            st.error(error)

        else:

            st.success(f"Answer: {result}")

    else:

        st.warning(
            "Please enter a mathematical expression."
        )
        # ============================================================
# STUDY Q&A
# ============================================================

st.divider()

st.subheader("📚 Study Q&A")

question = st.text_area(
    "Ask your academic question",
    placeholder="Example: What is Machine Learning?"
)

if st.button("Get Answer", key="qa_button"):

    if question.strip():

        answer = answer_question(question)

        st.success("📖 StudyBot Answer")

        st.write(answer)

    else:

        st.warning("Please enter a question.")
        # ============================================================
# AI STUDY ASSISTANT
# ============================================================

st.divider()

st.subheader("🤖 AI Study Assistant")

ai_question = st.text_area(
    "Ask StudyBot anything",
    placeholder="Example: Explain supervised learning with an example."
)

if st.button("🤖 Ask AI", key="ai_button"):

    if ai_question.strip():

        with st.spinner("🤖 StudyBot is thinking..."):

            answer = ask_ai(
    ai_question,
    st.session_state.chat_history
)


        st.success("📚 StudyBot Answer")

        st.write(answer)

    else:

        st.warning("Please enter a question.")
  
        # ============================================================
# CHAT HISTORY
# ============================================================

st.divider()

st.subheader("💬 Chat History")

if st.session_state.chat_history:

    for chat in st.session_state.chat_history:

        st.markdown("### 👤 You")
        st.write(chat["user"])

        st.markdown("### 🤖 StudyBot")
        st.write(chat["assistant"])

        st.divider()

else:

    st.info(
        "No conversations yet. Ask StudyBot a question!"
    )
    # ============================================================
# CLEAR CHAT
# ============================================================

if st.button("🗑️ Clear Chat", key="clear_chat_button"):

    st.session_state.chat_history = []

    st.rerun()
    # ============================================================
# QUIZ GENERATOR
# ============================================================

st.divider()

st.subheader("📝 Quiz Generator")

quiz_topic = st.text_input(
    "Enter a topic for your quiz",
    placeholder="Example: Machine Learning"
)

number_of_questions = st.number_input(
    "Number of Questions",
    min_value=1,
    max_value=10,
    value=5,
    step=1
)

if st.button("📝 Generate Quiz", key="quiz_button"):

    if quiz_topic.strip():

        with st.spinner("🤖 Generating your quiz..."):

            quiz = generate_quiz(
                quiz_topic,
                int(number_of_questions)
            )

        st.success("✅ Quiz Generated")

        st.markdown(quiz)

    else:

        st.warning("Please enter a topic.")
        # ============================================================
# NOTES SUMMARIZER
# ============================================================

st.divider()

st.subheader("📄 AI Notes Summarizer")

notes = st.text_area(
    "Paste your study notes here",
    placeholder="Example: Machine Learning is a branch of Artificial Intelligence...",
    height=250,
    key="notes_input"
)

if st.button("📄 Summarize Notes", key="summarize_button"):

    if notes.strip():

        with st.spinner("🤖 Summarizing your notes..."):

            summary = summarize_notes(notes)

        st.success("✅ Notes Summary")

        st.markdown(summary)

    else:

        st.warning("Please enter some notes first.")