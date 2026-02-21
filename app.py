from openai import OpenAI
import streamlit as st
import pandas as pd
import io
import time
import json
st.set_page_config(page_title="Computing Companion", layout="wide")
JSON_PATH = "/content/gdrive/My Drive/Computing/textbook_data.json"
TEXTBOOK_DRIVE_LINK = "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing"
def load_textbook_data():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []
raw_data = load_textbook_data()
if "selected_topic" not in st.session_state:
    st.session_state["selected_topic"] = "Computer Architecture"
STATIONERY_DATA = {
    "Computer Architecture": {
        "summary": "Describes how a computer is designed, built, and organized, focusing on processing units and connectivity[cite: 1].",
        "detailed_notes": {
            "Units of Data": {
                "Bit": "Smallest unit of data (0 or 1)[cite: 1].",
                "Byte": "8 bits[cite: 1].",
                "Measurement Units": {
                    "SI Prefixes (Power 1000)": ["Kilobyte (kB)", "Megabyte (MB)", "Gigabyte (GB)", "Terabyte (TB)"],
                    "Binary Prefixes (Power 1024)": ["Kibibyte (KiB)", "Mebibyte (MiB)", "Gibibyte (GiB)", "Tebibyte (TiB)"]
                }
            },
            "Key Components": {
                "CPU": "Processes data and executes instructions (measured in MHz/GHz)[cite: 2].",
                "RAM": "Volatile memory storing data with unique addresses[cite: 3].",
                "Buses": "Data Bus (bi-directional) and Address Bus (uni-directional)[cite: 6]."
            }
        },
        "glossary": {
            "CPU": "Central Processing Unit; the 'brain' that executes instructions[cite: 2].",
            "Volatile": "Memory that loses its contents when power is lost (e.g., RAM)[cite: 3].",
            "Address Bus": "A uni-directional bus used to transport memory addresses[cite: 6].",
            "Solid State": "A storage type with no moving parts, known for speed and durability[cite: 4]."
        },
        "keywords": ["CPU", "RAM", "Bit", "Byte", "Data Bus", "Address Bus"]
    },
    "Data Representation": {
        "summary": "The method of representing all information using electronic switches called bits[cite: 7].",
        "detailed_notes": {
            "Number Systems": {
                "Binary": "Base-2 system using 0 and 1[cite: 9].",
                "Hexadecimal": "Base-16 system (0-9, A-F); 1 hex digit = 4 bits[cite: 11]."
            },
            "Negative Numbers": {
                "Two's Complement": "Standard method for signed integers; flip bits and add 1[cite: 12].",
                "Overflow": "Error when a calculation exceeds the bit-length limits[cite: 13]."
            },
            "Text": {
                "ASCII": "7-bit (128 chars) or 8-bit (256 chars) encoding[cite: 14].",
                "Unicode": "Supports global languages using 8–32 bits[cite: 15]."
            }
        },
        "glossary": {
            "Hexadecimal": "A base-16 number system used for compact binary representation[cite: 11].",
            "Two's Complement": "A system used by computers to represent negative numbers[cite: 12].",
            "Unicode": "A universal character encoding standard supporting global languages[cite: 15].",
            "MSB": "Most Significant Bit; the leftmost bit in a binary number[cite: 12]."
        },
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode"]
    },
    "Boolean Logic": {
        "summary": "Boolean values and logic gates used by the processor to perform operations[cite: 16].",
        "detailed_notes": {
            "Truth Tables": "Shows output for every input combination (Rows = 2^n)[cite: 16].",
            "Logic Gates": ["AND (Q = A·B)", "OR (Q = A+B)", "NOT (Q = ¬A)", "NAND", "NOR", "XOR [cite: 17-22]"],
            "Laws": {
                "Double Negation": "¬(¬A) = A[cite: 24].",
                "De Morgan's Theorem": ["¬(A·B) = ¬A + ¬B", "¬(A+B) = ¬A·¬B [cite: 24]"]
            }
        },
        "glossary": {
            "Truth Table": "A table showing the output for all possible combinations of inputs[cite: 16].",
            "XOR": "Exclusive OR; output is 1 only if exactly one input is 1[cite: 22].",
            "NAND": "Not AND; output is 0 only when both inputs are 1[cite: 20].",
            "De Morgan's": "Theorems used to simplify complex Boolean expressions[cite: 24]."
        },
        "keywords": ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "De Morgan"]
    }
}

# --- SESSION STATE INITIALIZATION ---
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {topic: 0 for topic in STATIONERY_DATA.keys()}

if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Computer Architecture"

# --- SIDEBAR ---
st.sidebar.title("🔍 Computing Companion")

# Search Logic
search_query = st.sidebar.text_input("Search term (e.g., 'Two's Complement')")
if search_query:
    st.sidebar.subheader("Results:")
    for t_name, t_data in STATIONERY_DATA.items():
        if search_query.lower() in t_name.lower() or search_query.lower() in str(t_data).lower():
            if st.sidebar.button(f"Go to {t_name}", key=f"search_{t_name}"):
                st.session_state.selected_topic = t_name

# Topic Selection
topic_list = list(STATIONERY_DATA.keys())
topic_index = topic_list.index(st.session_state.selected_topic)
topic = st.sidebar.selectbox("Select Chapter:", topic_list, index=topic_index)
st.session_state.selected_topic = topic

# Activity Selection (Using 'key' to allow remote updates from buttons)
mode = st.sidebar.radio("Activity:", ["Review", "AI bot", "Quiz"], key="activity_mode")

# --- UTILITY FUNCTIONS ---
def display_nested_notes(data, level=0):
    """Recursively displays dictionary content as nested markdown[cite: 1, 101]."""
    if isinstance(data, dict):
        for key, value in data.items():
            if level == 0:
                st.subheader(f"📍 {key}")
            else:
                st.markdown(f"{'  ' * level}**{key}:**")
            display_nested_notes(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            st.markdown(f"{'  ' * level}- {item}")
    else:
        st.markdown(f"{'  ' * level}{data}")

# --- MAIN INTERFACE ---

if mode == "Review":
    st.title("🚀 Study Companion")
    st.header(f"Notes: {topic}")
    st.info(STATIONERY_DATA[topic]["summary"])
    
    # --- DYNAMIC MASTERY PROGRESS ---
    score = st.session_state.quiz_scores.get(topic, 0)
    st.write(f"**Current Mastery:** {score}%")
    st.progress(score / 100)
    
    tab_notes, tab_glossary, tab_resources = st.tabs(["📝 Detailed Notes", "🔍 Key Terms", "📂 Resources"])

    with tab_notes:
        display_nested_notes(STATIONERY_DATA[topic].get("detailed_notes", {}))

    with tab_glossary:
        st.subheader("Interactive Glossary")
        st.write("Click a term to see its textbook definition[cite: 164].")
        glossary = STATIONERY_DATA[topic].get("glossary", {})
        if glossary:
            # Display terms in a grid using columns
            cols = st.columns(3)
            for i, (term, definition) in enumerate(glossary.items()):
                with cols[i % 3]:
                    # Clickable Popover
                    with st.popover(term, use_container_width=True):
                        st.write(definition)
        else:
            st.warning("No glossary terms available.")

    with tab_resources:
        col_ref, col_quiz = st.columns(2)
        with col_ref:
            st.subheader("Textbook")
            st.link_button("📂 Open PDF in Drive", "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing")
        
        with col_quiz:
            st.subheader("Mastery")
            # --- WORKING QUIZ BUTTON ---
            if st.button("🏁 Start Topic Quiz", use_container_width=True):
                st.session_state.activity_mode = "Quiz"
                st.rerun()
elif mode == "AI bot":
    st.title("Ai bot")
    system_message_content= f"""

    You are a robotic, highly efficient GCE Computing assistant.
    Your goal is to provide precise, technical answers based on the provided textbook context.

    TEXTBOOK CONTEXT:
    {tb_content}

    List of content:
    {STATIONERY_DATA}

    RULES:
    Use the exact keywords from the context and content to answer the user's question.
    1. Use the provided context to answer the user's question.
    2. Maintain a robotic, neutral tone. No emotions, no fluff.
    3. Keep answers concise and structured (use bullet points for processes).
    5. Primary Source: Use the provided textbook context and the list of content.
    6. Secondary Source: If the topic is clearly about Computing (e.g., Privacy, Hardware, Internet) but not in the context, use your general knowledge to answer.
    7. Decline: Only decline if the user asks about non-computing topics (e.g., "How do I bake a cake?").

    EXAMPLES:

    <Examples>
    User: What is a bit?
    Assistant: A bit is the smallest unit of data in a computer, representing a binary value of 0 or 1.
    </Examples>
    """
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "openai_model" not in st.session_state:
      st.session_state["openai_model"] = "gpt-4o-mini"

    if "messages" not in st.session_state:
      st.session_state.messages = []
      st.session_state.messages.append({"role": "system", "content": system_message_content})

    for message in st.session_state.messages:
      if message["role"] in ["user", "assistant"]:
          with st.chat_message(message["role"]):
              st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
      st.session_state.messages.append({"role": "user", "content": prompt })
      with st.chat_message("user"):
          st.markdown(prompt)

      with st.chat_message("assistant"):
          stream = client.chat.completions.create(
              model="gpt-4o-mini",
              messages=[
                  {"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages
              ],
              temperature=0,
              stream=True,
          )
          response = st.write_stream(stream)
      st.session_state.messages.append({"role": "assistant", "content": response})
elif mode == "Quiz":
    st.header(f"AI Generated Quiz: {topic}")
    
    # --- QUIZ SETTINGS SIDEBAR ---
    st.sidebar.divider()
    st.sidebar.subheader("Quiz Settings")
    num_questions = st.sidebar.slider("Number of questions", 1, 10, 3)
    difficulty = st.sidebar.select_slider("Difficulty", options=["Easy", "Medium", "Hard(Out of syllabus)"])
    quiz_type = st.sidebar.selectbox("Question Type", ["Multiple Choice", "True/False"])

    quiz_key = f"quiz_questions_{topic}"
    
    # Button to generate/regenerate the quiz
    if st.button("Generate New Quiz"):
        with st.spinner(f"Generating {difficulty} {quiz_type} questions..."):
            client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

            # Logic to adjust prompt based on settings
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

    # --- DISPLAY QUIZ ---
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
