from openai import OpenAI
import streamlit as st
import pandas as pd
import io
import time
import json

st.set_page_config(page_title="Computing Companion", layout="wide")

# 1. Define Constants and Data First
JSON_PATH = "/content/gdrive/My Drive/Computing/textbook_data.json"
TEXTBOOK_DRIVE_LINK = "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing"

STATIONERY_DATA = {
    "Computer Architecture": {
        [cite_start]"summary": "The design and organization of a computer system's components and their connections[cite: 2].",
        "detailed_notes": {
            "Units of Data": {
                "Bit & Byte": "A bit is the smallest unit (0 or 1); 8 bits make a byte.",
                "Measurement": [
                    "SI Prefixes (Power 1000): kB, MB, GB, TB, PB.",
                    "Binary Prefixes (Power 1024): KiB, MiB, GiB, TiB, PiB."
                ]
            },
            "Hardware Components": {
                [cite_start]"CPU": "Processes data and executes instructions, measured in MHz or GHz[cite: 6].",
                [cite_start]"RAM": "Volatile memory where each byte has a unique address[cite: 8].",
                [cite_start]"Storage": "Non-volatile storage includes Magnetic (high capacity), Optical (laser-based), and Solid State (fast/durable)[cite: 10, 11].",
                "Buses": "Data Bus (bi-directional) and Address Bus (uni-directional)."
            },
            [cite_start]"Interfaces": "Includes USB (external), HDMI (AV output), and PCIe (internal expansion using lanes)[cite: 14, 15]."
        },
        "glossary": {
            [cite_start]"CPU": "Central Processing Unit; executes instructions[cite: 6].",
            [cite_start]"Volatile": "Memory that loses data when power is off, like RAM[cite: 8].",
            "Address Bus": "Transports memory addresses in one direction only.",
            [cite_start]"PCIe": "Internal motherboard expansion interface using lanes x1 to x16[cite: 15]."
        },
        "keywords": ["CPU", "RAM", "Data Bus", "Address Bus", "PCIe", "Solid State"]
    },
    "Data Representation": {
        [cite_start]"summary": "Representing information using electronic switches (bits) that are either ON (1) or OFF (0)[cite: 16].",
        "detailed_notes": {
            "Number Systems": {
                [cite_start]"Binary": "Base-2 (0 and 1)[cite: 19].",
                "Hexadecimal": "Base-16 (0-9, A-F). [cite_start]One hex digit maps to 4 binary bits[cite: 23, 24]."
            },
            "Negative Numbers": {
                [cite_start]"Two's Complement": "Standard method; flip all bits and add 1[cite: 26, 27].",
                "Sign Bit": "The MSB (Most Significant Bit) is 0 for positive and 1 for negative.",
                [cite_start]"Overflow": "Error when a result exceeds bit-length limits[cite: 28]."
            },
            "Text": [
                [cite_start]"ASCII: 7-bit (128 chars) or Extended 8-bit (256 chars)[cite: 30].",
                [cite_start]"Unicode: 8–32 bits, supports global languages[cite: 31]."
            ]
        },
        "glossary": {
            [cite_start]"Two's Complement": "A system for representing negative numbers in binary[cite: 26].",
            [cite_start]"MSB": "Most Significant Bit; the sign bit in Two's Complement (1 = negative)[cite: 26].",
            [cite_start]"Overflow": "Occurs when a calculation exceeds the bit-length limit[cite: 28]."
        },
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode"]
    },
    "Computer Networks": {
        [cite_start]"summary": "Two or more devices connected to exchange data[cite: 132].",
        "detailed_notes": {
            [cite_start]"Scope": "LAN (local/home), MAN (city-scale), and WAN (Internet)[cite: 137, 138, 139].",
            "Hardware": [
                [cite_start]"Modem: Converts digital data for long-distance transmission[cite: 148].",
                [cite_start]"Switch: Connects devices in a LAN using MAC addresses[cite: 150].",
                [cite_start]"Router: Forwards packets between networks using IP addresses[cite: 151]."
            ],
            [cite_start]"Error Detection": "Parity bits (single-bit errors), Checksums (mathematical), and Echo checks[cite: 144, 145, 146]."
        },
        "glossary": {
            [cite_start]"Modem": "Hardware that converts digital data for long-distance transmission[cite: 148].",
            [cite_start]"Switch": "LAN device that forwards data using permanent 48-bit MAC addresses[cite: 150].",
            [cite_start]"IP Address": "Hierarchical address (IPv4 32-bit or IPv6 128-bit) for network routing[cite: 152, 153]."
        },
        "keywords": ["LAN", "WAN", "Modem", "Switch", "Router", "MAC Address", "IP Address"]
    }
}

# 2. Define Helper Functions
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

# 3. Load Data and Initialize Session State
raw_data = load_textbook_data()

if "selected_topic" not in st.session_state:
    st.session_state["selected_topic"] = "Computer Architecture"

if "current_mode" not in st.session_state:
    st.session_state.current_mode = "Review"

if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {topic: 0 for topic in STATIONERY_DATA.keys()}

# 4. Sidebar Logic
st.sidebar.title("🔍 Computing Companion")

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

# 5. Fetch Content for AI Bot/Review (After topic is defined)
tb_content = get_filtered_context(topic, raw_data)
# --- UTILITY FUNCTIONS ---
def display_nested_notes(data, level=0):
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
mode = st.session_state.current_mode

if mode == "Review":
    st.title("🚀 Study Portal")
    st.header(f"Notes: {topic}")
    st.info(STATIONERY_DATA[topic]["summary"])
    
    # Mastery Progress
    score = st.session_state.quiz_scores.get(topic, 0)
    st.write(f"**Topic Mastery:** {score}%")
    st.progress(score / 100)
    
    tab_notes, tab_glossary, tab_resources = st.tabs(["📝 Detailed Notes", "🔍 Key Terms", "📂 Resources"])

    with tab_notes:
        display_nested_notes(STATIONERY_DATA[topic].get("detailed_notes", {}))

    with tab_glossary:
        st.subheader("Interactive Glossary")
        st.write("Click a term to see the textbook definition.")
        glossary = STATIONERY_DATA[topic].get("glossary", {})
        if glossary:
            cols = st.columns(3)
            for i, (term, definition) in enumerate(glossary.items()):
                with cols[i % 3]:
                    with st.popover(term, use_container_width=True):
                        st.write(definition)
        else:
            st.warning("No glossary available for this chapter.")

    with tab_resources:
        col_ref, col_quiz = st.columns(2)
        with col_ref:
            st.subheader("Reference")
            st.link_button("📂 Open Full PDF", "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing")
        
        with col_quiz:
            st.subheader("Assessment")
            # This button will now work correctly without an exception
            if st.button("🏁 Start Quiz Now", use_container_width=True):
                st.session_state.current_mode = "Quiz"
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
