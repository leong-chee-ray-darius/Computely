#Importing modules
from openai import OpenAI
from data import STATIONERY_DATA
import streamlit as st
import pandas as pd
import json
#Setting page title
st.set_page_config(page_title="Computely", layout="wide")

#Define constants and Data
JSON_PATH = "/content/gdrive/My Drive/Computing/textbook_data.json"
TEXTBOOK_DRIVE_LINK = "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing"
#Define functions
def load_textbook_data():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def get_filtered_context(selected_topic, data_source):
    if not data_source:
        return ""
    search_terms = STATIONERY_DATA[selected_topic].get("keywords", []) + [selected_topic]
    matches = []
    for page in data_source:
        content = str(page)
        if any(term.lower() in content.lower() for term in search_terms):
            matches.append(content)
    return "\n\n".join(matches[:10])
def display_nested_notes(notes, level=0):
    for key, value in notes.items():
        if isinstance(value, dict):
            # Calculate header level
            header_level = min(level + 1, 4)
            hashes = "#" * header_level
            st.markdown(f"{hashes} {key}")
            display_nested_notes(value, level + 1)

        elif isinstance(value, list):
            st.markdown(f"**{key}:**")
            if len(value) <= 6 and all(isinstance(i, str) for i in value):
                st.markdown(" | ".join(value))
            else:
                df = pd.DataFrame(value, columns=["Value"])
                st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.markdown(f"**{key}:** {value}")
def display_value(value):
    if isinstance(value, list):
        df = pd.DataFrame(value, columns=["Value"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    elif isinstance(value, dict):
        df = pd.DataFrame(value.items(), columns=["Item", "Description"])
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.write(value)
#Load data and initialise session state
raw_data = load_textbook_data()

if "selected_topic" not in st.session_state:
    st.session_state["selected_topic"] = "Computer Architecture"

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Review"

if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {topic: 0 for topic in STATIONERY_DATA.keys()}

#Sidebar
st.sidebar.title("🔍 Computely")

search_query = st.sidebar.text_input("Quick search (e.g., 'Two's Complement')")
if search_query:
    st.sidebar.subheader("Results:")
    for t_name, t_data in STATIONERY_DATA.items():
        if search_query.lower() in t_name.lower() or search_query.lower() in str(t_data).lower():
            if st.sidebar.button(f"Go to {t_name}", key=f"search_{t_name}"):
                st.session_state.selected_topic = t_name

topic_list = list(STATIONERY_DATA.keys())
topic_index = topic_list.index(st.session_state.selected_topic)
topic = st.sidebar.selectbox("Select Chapter:", topic_list, index=topic_index)
st.session_state.selected_topic = topic

modes = ["Review", "AI bot", "Quiz"]
mode_index = modes.index(st.session_state.current_mode)
selected_mode = st.sidebar.radio("Activity:", modes, index=mode_index)

if selected_mode != st.session_state.current_mode:
    st.session_state.current_mode = selected_mode
    st.rerun()
#Fetch content for AI bot
mode = st.session_state.current_mode

if mode == "Review":
    st.markdown(f"# 📘 {topic}")
    st.caption("GCE O-Level Computing • Structured Study Notes")
    st.success(f"📖 **Chapter Summary:** {STATIONERY_DATA[topic]['summary']}")

    tab_notes, tab_glossary, tab_resources = st.tabs([
    "📝 Learn",
    "📚 Key Terms",
    "📂 Resources"
    ])

    with tab_notes:
        display_nested_notes(STATIONERY_DATA[topic].get("detailed_notes", {}))

    with tab_glossary:
        st.subheader("📚 Glossary")
        glossary = STATIONERY_DATA[topic].get("glossary", {})
        if glossary:
            df = pd.DataFrame(glossary.items(), columns=["Term", "Definition"])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.warning("No glossary available.")

    with tab_resources:
        col_ref, col_quiz = st.columns(2)
        with col_ref:
            st.subheader("Reference")
            st.link_button("📂 Open Full PDF", "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing")

        with col_quiz:
            st.subheader("Assessment")
            if st.button("🏁 Start Quiz Now", use_container_width=True):
                st.session_state.current_mode = "Quiz"
                st.rerun()
elif mode == "AI bot":
    st.title("🤖 AI Computing Tutor")

    #Get filtered textbook context
    tb_content = get_filtered_context(
        st.session_state.selected_topic,
        raw_data
    )

    system_message_content = f"""
ROLE: Robotic GCE O-Level Computing Assistant.
TONE: Highly technical, neutral, and precise. Avoid conversational filler.

---
RESOURCES:
1. TEXTBOOK CONTENT (PRIORITY 1):
{tb_content}

2. STRUCTURED DATA (PRIORITY 2):
{json.dumps(STATIONERY_DATA[st.session_state.selected_topic], indent=2)}
---

STRICT OPERATING RULES:
1. SOURCE HIERARCHY: Answer using the TEXTBOOK first. If the information is missing, use the STRUCTURED DATA.
2. SCOPE: If a query is about software, logic, hardware, or development but doesn't match your database keywords, DO NOT reject it. Instead, search for the most relevant concept.
3. FORMATTING:
   - Use Markdown bolding for key terms.
   - Use Bullet Points for processes/lists.
   - Use LaTeX for binary/denary math (e.g., $1010_2$).
4. FUZZY MATCHING: Actively bridge the gap between student terminology and the syllabus.
   - "How to make an app" -> Explain the 'waterfall model'
   - "Code steps" -> Explain Analysis, Design, Coding, and Testing.
5. NO HALLUCINATION: If the information is not in either resource, state: "Information not available in provided syllabus materials."
EXAMPLES OF CORRECT MAPPING:
- User: "What are the steps for software engineering?"
- Assistant: "The five stages in developing a program are: 1. Gather requirements, 2. Design solutions, 3. Write code, 4. Test & Refine Code, 5. Deploy code. This is the traditional 'waterfall model', where progress flows
through multiple stages in a sequential manner and each stage is completed before moving on to the next stage.

- User: "How to print?"
- Assistant: "Please specify: Are you asking about the (1) Python 'print()' function or (2) the mechanical operation of Laser/Inkjet printers?"

- User: "Explain printing."
- Assistant: "In Computing, this refers to two areas:
  1. Output: The `print()` function in Python sends data to the standard output device (monitor).
     Example: `print('Hello World')`.
  2. Hardware: The mechanical process of transferring data to paper.
     - Inkjet: Uses piezoelectric crystals or thermal bubbles to spray liquid ink.
     - Laser: Uses a rotating drum, static electricity, and a fuser to bond toner to paper."
"""

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_message_content}
        ]

    #Display chat history
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("Ask a computing question..."):
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages,
                temperature=0
            )

            answer = response.choices[0].message.content
            st.markdown(answer)

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
elif mode == "Quiz":
    st.header(f"AI Generated Quiz: {topic}")

    # Quiz settings
    st.sidebar.divider()
    st.sidebar.subheader("Quiz Settings")
    num_questions = st.sidebar.slider("Number of questions", 1, 10, 3)
    difficulty = st.sidebar.select_slider("Difficulty", options=["Easy", "Medium", "Hard(Out of syllabus)"])
    quiz_type = st.sidebar.selectbox("Question Type", ["Multiple Choice", "True/False"])

    quiz_key = f"quiz_questions_{topic}"

    # Button to generate the quiz
    if st.button("Generate New Quiz"):
        with st.spinner(f"Generating {difficulty} {quiz_type} questions..."):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # Adjust prompt based on settings
            type_instruction = "multiple-choice questions with 4 options" if quiz_type == "Multiple Choice" else "True/False questions with exactly 2 options (True and False)"

            prompt = f"""
            Generate {num_questions} {difficulty} level {type_instruction} for the computing topic: {topic}.
            Context summary: {STATIONERY_DATA[topic]['summary']}

            Return ONLY a JSON object with a key "questions" containing a list of objects.
            Each object must have:
            - "question": The question text
            - "options": A list of strings for the choices
            - "answer": The exact string from "options" that is correct.
            """

            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )

                content = json.loads(response.choices[0].message.content)
                st.session_state[quiz_key] = content.get("questions", [])
                st.rerun()
            except Exception as e:
                st.error(f"Failed to generate quiz: {e}")

    # Display quiz
    if st.session_state.get(quiz_key):
        quiz = st.session_state[quiz_key]

        with st.form(key=f"form_{topic}"):
            user_answers = []
            for i, q in enumerate(quiz):
                st.write(f"### Q{i+1}: {q['question']}")
                choice = st.radio("Select your answer:", q['options'], key=f"radio_{topic}_{i}")
                user_answers.append(choice)

            submitted = st.form_submit_button("Submit Results")

            if submitted:
                score = 0
                for i, q in enumerate(quiz):
                    if user_answers[i] == q['answer']:
                        score += 1
                        st.success(f"**Q{i+1}: Correct!**")
                    else:
                        st.error(f"**Q{i+1}: Incorrect.** Correct: {q['answer']}")

                st.metric("Final Score", f"{score} / {len(quiz)}")
                if score == len(quiz):
                    st.balloons()
    else:
        st.info("Adjust settings in the sidebar and click 'Generate' to start.")
