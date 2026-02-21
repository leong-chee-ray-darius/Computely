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
        "summary": "Describes how a computer is designed, built, and organized, focusing on processing and data movement.",
        "detailed_notes": [
            "**Units of Data:** A bit is the smallest unit (0 or 1); 8 bits make a byte.",
            "**CPU:** Processes data and executes instructions; speed is measured in MHz or GHz.",
            "**RAM:** Volatile memory that temporarily stores data for the CPU; each byte has a unique address.",
            "**Secondary Storage:** Long-term non-volatile storage (Magnetic, Optical, and Solid State).",
            "**Buses:** Data Bus is bi-directional (transports data); Address Bus is uni-directional (transports memory addresses).",
            "**Interfaces:** Includes USB (external), HDMI (AV output), and PCIe (internal expansion)."
        ],
        "keywords": ["CPU", "RAM", "Bit", "Byte", "Magnetic", "Optical", "Solid State", "Data Bus", "Address Bus", "USB", "PCIe"],
        "quiz": [{"q": "What is the function of the address bus?", "a": "Transports memory addresses (uni-directional)."}]
    },
    "Data Representation": {
        "summary": "How all information is represented using electronic switches (bits).",
        "detailed_notes": [
            "**Number Systems:** Denary (Base-10), Binary (Base-2), and Hexadecimal (Base-16).",
            "**Hexadecimal:** Each hex digit maps to exactly 4 binary bits.",
            "**Negative Numbers:** Represented via Two's Complement; involves flipping bits and adding 1.",
            "**Text:** ASCII (7 or 8 bits) and Unicode (8–32 bits, supports global languages)."
        ],
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode", "MSB", "Overflow"],
        "quiz": [{"q": "How many bits are in an extended ASCII character?", "a": "8"}]
    },
    "Boolean Logic": {
        "summary": "Boolean values and logic gates used by the processor to perform operations.",
        "detailed_notes": [
            "**Truth Tables:** Shows output for every input combination; number of rows is 2^n.",
            "**Logic Gates:** AND (Q=A·B), OR (Q=A+B), NOT (Q=¬A), NAND, NOR, and XOR.",
            "**Laws:** De Morgan's Theorem (¬(A·B) = ¬A+¬B) and Double Negation (¬(¬A) = A).",
            "**Order of Ops:** Parentheses, NOT, AND, then OR."
        ],
        "keywords": ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "De Morgan", "Truth Table"],
        "quiz": [{"q": "What is the Boolean expression for an AND gate?", "a": "Q = A · B"}]
    },
    "Algorithms and Programming": {
        "summary": "Step-by-step instructions translated into source code for processor execution.",
        "detailed_notes": [
            "**Variables:** Named identifiers storing changeable values; must follow specific naming rules.",
            "**Data Types:** bool, int (unlimited size), float (precision errors), str (immutable), list (mutable), dict.",
            "**Control Flow:** Sequence, Selection (if-elif-else), and Iteration (while, for-in).",
            "**UDFs:** User-Defined Functions allow modular design and follow the DRY (Don't Repeat Yourself) principle."
        ],
        "keywords": ["Algorithm", "Variable", "Literal", "Iteration", "Selection", "Mutable", "DRY", "Scope"],
        "quiz": [{"q": "Which data type is an ordered, mutable sequence?", "a": "list"}]
    },
    "Validation and Error Handling": {
        "summary": "Techniques to ensure input data is sensible and prevent program crashes.",
        "detailed_notes": [
            "**Common Checks:** Length, Range, Presence (not empty), and Format (e.g., HH:MM).",
            "**Existence Checks:** Verifying if data is or is not in a collection (e.g., unique username).",
            "**Check Digits:** Extra digit to detect manual entry errors (e.g., UPC-A)."
        ],
        "keywords": ["Validation", "Range check", "Length check", "Presence check", "Format check", "Check digit"],
        "quiz": [{"q": "Which check ensures a numeric input is within boundaries?", "a": "Range check"}]
    },
    "Bugs and Testing": {
        "summary": "Identifying and removing defects (bugs) that cause unintended behavior.",
        "detailed_notes": [
            "**Error Types:** Syntax (grammar rules), Logic (incorrect results), and Run-time (execution crash).",
            "**Test Cases:** Should include Normal, Boundary, and Error conditions.",
            "**Techniques:** Trace tables for dry runs and incremental testing."
        ],
        "keywords": ["Bug", "Syntax Error", "Logic Error", "Trace Table", "Boundary Condition"],
        "quiz": [{"q": "Which error type is caught before the program runs?", "a": "Syntax Error"}]
    },
    "Algorithm Design": {
        "summary": "Formulating problems into algorithmic solutions using computational thinking.",
        "detailed_notes": [
            "**Decomposition:** Breaking complex problems into manageable modular or incremental parts.",
            "**Generalisation:** Identifying patterns to create generic, reusable algorithms.",
            "**Solutions:** Finding Min/Max (assume first is min/max) and Linear Search."
        ],
        "keywords": ["Decomposition", "Generalisation", "Computational Thinking", "Linear Search", "Extraction"],
        "quiz": [{"q": "What is the process of breaking a problem down called?", "a": "Decomposition"}]
    },
    "Program Development Models": {
        "summary": "Structured approaches to managing the software development lifecycle.",
        "detailed_notes": [
            "**Waterfall:** Sequential stages from requirements to deployment.",
            "**Agile:** Incremental development using 'sprints' and 'user stories' for continuous feedback.",
            "**TDD:** Test-Driven Development; writing tests before the minimum code needed to pass them.",
            "**User Testing:** Alpha (developer site) and Beta (user environment)."
        ],
        "keywords": ["Waterfall", "Agile", "Sprints", "TDD", "Alpha testing", "Beta testing", "Version Control"],
        "quiz": [{"q": "What is testing in the user environment called?", "a": "Beta testing"}]
    },
    "Spreadsheets": {
        "summary": "Using cell references, formulas, and functions for data analysis.",
        "detailed_notes": [
            "**References:** Relative (A1), Absolute ($A$1), and Mixed.",
            "**Functions:** IF (logic), VLOOKUP/HLOOKUP (search), and INDEX+MATCH (advanced lookup).",
            "**Data Types:** Numbers < Text < Logical < Error.",
            "**Tools:** Goal Seek for what-if analysis and Conditional Formatting."
        ],
        "keywords": ["Absolute reference", "VLOOKUP", "IF function", "Goal Seek", "Conditional Formatting"],
        "quiz": [{"q": "What symbol is used to lock a cell reference?", "a": "$"}]
    },
    "Computer Networks": {
        "summary": "Devices connected by transmission media for exchanging data and sharing resources.",
        "detailed_notes": [
            "**Geographical Scope:** LAN (local), MAN (city), and WAN (wide/Internet).",
            "**Error Detection:** Parity bits, Checksums, and Echo checks.",
            "**Hardware:** Modem (long-distance), Switch (MAC-based LAN forwarding), and Router (IP-based).",
            "**Addressing:** MAC (48-bit permanent) and IP (IPv4 32-bit or IPv6 128-bit)."
        ],
        "keywords": ["LAN", "WAN", "Protocol", "MAC address", "IP address", "Checksum", "Switch", "Router"],
        "quiz": [{"q": "Which device connects devices within a LAN using MAC addresses?", "a": "Switch"}]
    },
    "Security and Privacy": {
        "summary": "Protecting data confidentiality, integrity, and availability.",
        "detailed_notes": [
            "**Threats:** Malware (adware, spyware), Phishing (deceptive emails), and Pharming (URL redirection).",
            "**Defenses:** Firewalls (packet filtering), Encryption (meaningless without key), and MFA.",
            "**Legal:** PDPA (Singapore law regulating personal data consent and retention)."
        ],
        "keywords": ["Confidentiality", "Integrity", "Phishing", "Pharming", "Encryption", "Firewall", "PDPA", "MFA"],
        "quiz": [{"q": "What does PDPA stand for?", "a": "Personal Data Protection Act"}]
    },
    "Intellectual Property": {
        "summary": "Legal protections for original digital creations of the mind.",
        "detailed_notes": [
            "**Copyright:** Control over use/distribution; only humans are recognized authors in Singapore.",
            "**Software Licenses:** Proprietary (secret code), Freeware, FOSS (open source), and Public Domain.",
            "**Piracy:** Illegal copying or using cracks to bypass license detection.",
            "**Plagiarism:** Ethical offense of passing off others' work as your own."
        ],
        "keywords": ["Copyright", "License", "Proprietary", "FOSS", "Freeware", "Piracy", "Plagiarism"],
        "quiz": [{"q": "Is AI-generated content copyrightable in Singapore?", "a": "No (requires a human author)"}]
    },
    "Impact of Computing": {
        "summary": "Transformation of society across industries and the spread of online falsehoods.",
        "detailed_notes": [
            "**Industries:** Communications (globalization), Education (personalized learning), and Retail (e-commerce).",
            "**Falsehoods:** Filter bubbles created by social media algorithms increase misinformation.",
            "**POFMA:** Singapore law to combat fake news harming public interest."
        ],
        "keywords": ["Globalisation", "Digital Literacy", "Filter Bubble", "Misinformation", "POFMA"],
        "quiz": [{"q": "What Singapore law is used to issue correction directions for fake news?", "a": "POFMA"}]
    },
    "Emerging Technologies": {
        "summary": "Innovations like AI, Blockchain, and Quantum Computing that improve performance autonomously.",
        "detailed_notes": [
            "**AI:** Narrow AI (specialized) vs. AGI (human-level).",
            "**ML:** Detects patterns in data to produce models for inference.",
            "**Blockchain:** Decentralized, immutable ledger linked via cryptographic hashes.",
            "**Quantum:** Uses Qubits (superposition of 0 and 1) and Entanglement to solve problems exponentially faster."
        ],
        "keywords": ["Artificial Intelligence", "Machine Learning", "Blockchain", "Quantum Computing", "Qubit", "Superposition"],
        "quiz": [{"q": "What is the state where a qubit exists as both 0 and 1 simultaneously?", "a": "Superposition"}]
    }
}
# --- SEARCH LOGIC ---
st.sidebar.title("🔍 Search")
search_query = st.sidebar.text_input("Find a term (e.g., 'Protocol')")

if search_query:
    st.sidebar.subheader("Results:")
    found = False
    for t_name, t_data in STATIONERY_DATA.items():
        in_notes = any(search_query.lower() in note.lower() for note in t_data.get("detailed_notes", []))
        if (search_query.lower() in t_name.lower() or 
            search_query.lower() in t_data["summary"].lower() or in_notes):
            if st.sidebar.button(f"Go to {t_name}", key=f"search_{t_name}"):
                st.session_state["selected_topic"] = t_name
            found = True
    if not found:
        st.sidebar.write("No matches found.")

# --- SIDEBAR NAV ---
topic_list = list(STATIONERY_DATA.keys())
try:
    topic_index = topic_list.index(st.session_state["selected_topic"])
except ValueError:
    topic_index = 0

topic = st.sidebar.selectbox("Select a Chapter:", topic_list, index=topic_index)
st.session_state["selected_topic"] = topic

mode = st.sidebar.radio("Activity:", ["Review", "AI bot", "Quiz"])

# --- FILTERING LOGIC ---
def get_filtered_context(selected_topic):
    if not raw_data:
        return ""
    search_terms = STATIONERY_DATA[selected_topic].get("keywords", []) + [selected_topic]
    matches = []
    for page in raw_data:
        content = str(page) # Adjust based on your JSON structure
        if any(term.lower() in content.lower() for term in search_terms):
            matches.append(content)
    return "\n\n".join(matches[:10])

tb_content = get_filtered_context(topic)
if "quiz_scores" not in st.session_state:
    st.session_state.quiz_scores = {topic: 0 for topic in STATIONERY_DATA.keys()}

def display_nested_notes(data, level=0):
    """Recursively displays dictionary content as nested markdown[cite: 1, 101]."""
    if isinstance(data, dict):
        for key, value in data.items():
            clean_key = key.replace("_", " ").title()
            if level == 0:
                st.subheader(f"📍 {clean_key}")
            else:
                st.markdown(f"{'  ' * level}**{clean_key}:**")
            display_nested_notes(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            st.markdown(f"{'  ' * level}- {item}")
    else:
        st.markdown(f"{'  ' * level}{data}")

if mode == "Review":
    st.title("🚀 Computing Study Companion")
    st.header(f"Study Notes: {topic}")
    
    # Header summary
    st.info(STATIONERY_DATA[topic]["summary"])
    
    # --- DYNAMIC MASTERY PROGRESS ---
    # Mastery is linked to the session_state score for the current topic
    current_score = st.session_state.quiz_scores.get(topic, 0)
    st.write(f"**Topic Mastery:** {current_score}%")
    st.progress(current_score / 100)
    
    # Navigation Tabs
    tab_notes, tab_glossary, tab_resources = st.tabs(["📝 Detailed Notes", "🔍 Key Terms", "📂 Resources"])

    with tab_notes:
        display_nested_notes(STATIONERY_DATA[topic].get("detailed_notes", {}))

    with tab_glossary:
        st.subheader("Interactive Glossary")
        st.write("Click a term to see its definition from the textbook[cite: 1, 164].")
        
        # --- CLICKABLE KEY TERMS ---
        glossary = STATIONERY_DATA[topic].get("glossary", {})
        if glossary:
            # Display terms in a grid using columns
            cols = st.columns(3)
            for i, (term, definition) in enumerate(glossary.items()):
                with cols[i % 3]:
                    # Using popover to show definition on click
                    with st.popover(term, use_container_width=True):
                        st.write(definition)
        else:
            st.warning("No glossary terms available for this topic.")

    with tab_resources:
        col_ref, col_quiz = st.columns(2)
        with col_ref:
            st.subheader("Reference Material")
            with st.container(border=True):
                st.write("Full Textbook Access[cite: 111, 183].")
                st.link_button("📂 Open PDF in Drive", TEXTBOOK_DRIVE_LINK)
                st.caption("Use chapter titles to navigate.")
        
        with col_quiz:
            st.subheader("Mastery Quiz")
            with st.container(border=True):
                st.write("Ready to test your knowledge?")
                if st.button("📝 Start Quiz", use_container_width=True):
                    # In your real app, this would switch 'mode' to 'Quiz'
                    st.session_state.mode = "Quiz"
                    st.rerun()

    st.divider()
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
