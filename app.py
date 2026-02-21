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
        [cite_start]"summary": "Describes how a computer is designed, built, and organized, focusing on processing and data movement[cite: 1, 2].",
        "detailed_notes": [
            "**Units of Data:** A bit is the smallest unit (0 or 1); [cite_start]8 bits make a byte[cite: 4].",
            [cite_start]"**CPU:** Processes data and executes instructions; speed is measured in MHz or GHz[cite: 6, 7].",
            [cite_start]"**RAM:** Volatile memory that temporarily stores data for the CPU; each byte has a unique address[cite: 8, 9].",
            [cite_start]"**Secondary Storage:** Long-term non-volatile storage (Magnetic, Optical, and Solid State)[cite: 10, 11].",
            "**Buses:** Data Bus is bi-directional (transports data); [cite_start]Address Bus is uni-directional (transports memory addresses)[cite: 12, 13].",
            [cite_start]"**Interfaces:** Includes USB (external), HDMI (AV output), and PCIe (internal expansion)[cite: 15]."
        ],
        "keywords": ["CPU", "RAM", "Bit", "Byte", "Magnetic", "Optical", "Solid State", "Data Bus", "Address Bus", "USB", "PCIe"],
        "quiz": [{"q": "What is the function of the address bus?", "a": "Transports memory addresses (uni-directional)."}]
    },
    "Data Representation": {
        [cite_start]"summary": "How all information is represented using electronic switches (bits)[cite: 16, 17].",
        "detailed_notes": [
            [cite_start]"**Number Systems:** Denary (Base-10), Binary (Base-2), and Hexadecimal (Base-16)[cite: 18, 19, 23].",
            [cite_start]"**Hexadecimal:** Each hex digit maps to exactly 4 binary bits[cite: 24].",
            [cite_start]"**Negative Numbers:** Represented via Two's Complement; involves flipping bits and adding 1[cite: 26, 27].",
            [cite_start]"**Text:** ASCII (7 or 8 bits) and Unicode (8–32 bits, supports global languages)[cite: 30, 31, 32]."
        ],
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode", "MSB", "Overflow"],
        "quiz": [{"q": "How many bits are in an extended ASCII character?", "a": "8"}]
    },
    "Boolean Logic": {
        [cite_start]"summary": "Boolean values and logic gates used by the processor to perform operations[cite: 33].",
        "detailed_notes": [
            [cite_start]"**Truth Tables:** Shows output for every input combination; number of rows is 2^n[cite: 34].",
            [cite_start]"**Logic Gates:** AND (Q=A·B), OR (Q=A+B), NOT (Q=¬A), NAND, NOR, and XOR[cite: 36, 37, 38, 42].",
            [cite_start]"**Laws:** De Morgan's Theorem (¬(A·B) = ¬A+¬B) and Double Negation (¬(¬A) = A)[cite: 45].",
            [cite_start]"**Order of Ops:** Parentheses, NOT, AND, then OR[cite: 43]."
        ],
        "keywords": ["AND", "OR", "NOT", "NAND", "NOR", "XOR", "De Morgan", "Truth Table"],
        "quiz": [{"q": "What is the Boolean expression for an AND gate?", "a": "Q = A · B"}]
    },
    "Algorithms and Programming": {
        [cite_start]"summary": "Step-by-step instructions translated into source code for processor execution[cite: 52, 53].",
        "detailed_notes": [
            [cite_start]"**Variables:** Named identifiers storing changeable values; must follow specific naming rules[cite: 55].",
            [cite_start]"**Data Types:** bool, int (unlimited size), float (precision errors), str (immutable), list (mutable), dict[cite: 60, 61, 63, 65].",
            [cite_start]"**Control Flow:** Sequence, Selection (if-elif-else), and Iteration (while, for-in)[cite: 68].",
            [cite_start]"**UDFs:** User-Defined Functions allow modular design and follow the DRY (Don't Repeat Yourself) principle[cite: 70, 71]."
        ],
        "keywords": ["Algorithm", "Variable", "Literal", "Iteration", "Selection", "Mutable", "DRY", "Scope"],
        "quiz": [{"q": "Which data type is an ordered, mutable sequence?", "a": "list"}]
    },
    "Validation and Error Handling": {
        [cite_start]"summary": "Techniques to ensure input data is sensible and prevent program crashes[cite: 74].",
        "detailed_notes": [
            [cite_start]"**Common Checks:** Length, Range, Presence (not empty), and Format (e.g., HH:MM)[cite: 77, 78, 79, 80].",
            [cite_start]"**Existence Checks:** Verifying if data is or is not in a collection (e.g., unique username)[cite: 81, 82].",
            [cite_start]"**Check Digits:** Extra digit to detect manual entry errors (e.g., UPC-A)[cite: 84]."
        ],
        "keywords": ["Validation", "Range check", "Length check", "Presence check", "Format check", "Check digit"],
        "quiz": [{"q": "What check ensures a numeric input is within boundaries?", "a": "Range check"}]
    },
    "Bugs and Testing": {
        [cite_start]"summary": "Identifying and removing defects (bugs) that cause unintended behavior[cite: 86].",
        "detailed_notes": [
            [cite_start]"**Error Types:** Syntax (grammar rules), Logic (incorrect results), and Run-time (execution crash)[cite: 88, 90, 93].",
            [cite_start]"**Test Cases:** Should include Normal, Boundary, and Error conditions[cite: 95].",
            [cite_start]"**Techniques:** Trace tables for dry runs and incremental testing[cite: 97, 98]."
        ],
        "keywords": ["Bug", "Syntax Error", "Logic Error", "Trace Table", "Boundary Condition"],
        "quiz": [{"q": "Which error type is caught before the program runs?", "a": "Syntax Error"}]
    },
    "Algorithm Design": {
        [cite_start]"summary": "Formulating problems into algorithmic solutions using computational thinking[cite: 99, 100].",
        "detailed_notes": [
            [cite_start]"**Decomposition:** Breaking complex problems into manageable modular or incremental parts[cite: 101, 102].",
            [cite_start]"**Generalisation:** Identifying patterns to create generic, reusable algorithms[cite: 103, 104].",
            [cite_start]"**Solutions:** Finding Min/Max (assume first is min/max) and Linear Search[cite: 106, 107]."
        ],
        "keywords": ["Decomposition", "Generalisation", "Computational Thinking", "Linear Search", "Extraction"],
        "quiz": [{"q": "What is the process of breaking a problem down called?", "a": "Decomposition"}]
    },
    "Program Development Models": {
        [cite_start]"summary": "Structured approaches to managing the software development lifecycle[cite: 109].",
        "detailed_notes": [
            [cite_start]"**Waterfall:** Sequential stages from requirements to deployment[cite: 110, 118].",
            [cite_start]"**Agile:** Incremental development using 'sprints' and 'user stories' for continuous feedback[cite: 120].",
            [cite_start]"**TDD:** Test-Driven Development; writing tests before the minimum code needed to pass them[cite: 121].",
            [cite_start]"**User Testing:** Alpha (developer site) and Beta (user environment)[cite: 116]."
        ],
        "keywords": ["Waterfall", "Agile", "Sprints", "TDD", "Alpha testing", "Beta testing", "Version Control"],
        "quiz": [{"q": "What is testing in the user environment called?", "a": "Beta testing"}]
    },
    "Spreadsheets": {
        [cite_start]"summary": "Using cell references, formulas, and functions for data analysis[cite: 122].",
        "detailed_notes": [
            [cite_start]"**References:** Relative (A1), Absolute ($A$1), and Mixed[cite: 123].",
            [cite_start]"**Functions:** IF (logic), VLOOKUP/HLOOKUP (search), and INDEX+MATCH (advanced lookup)[cite: 125, 128, 130].",
            [cite_start]"**Data Types:** Numbers < Text < Logical < Error[cite: 125].",
            [cite_start]"**Tools:** Goal Seek for what-if analysis and Conditional Formatting[cite: 131]."
        ],
        "keywords": ["Absolute reference", "VLOOKUP", "IF function", "Goal Seek", "Conditional Formatting"],
        "quiz": [{"q": "What symbol is used to lock a cell reference?", "a": "$"}]
    },
    "Computer Networks": {
        [cite_start]"summary": "Devices connected by transmission media for exchanging data and sharing resources[cite: 132, 133].",
        "detailed_notes": [
            [cite_start]"**Geographical Scope:** LAN (local), MAN (city), and WAN (wide/Internet)[cite: 137, 138, 139].",
            [cite_start]"**Error Detection:** Parity bits, Checksums, and Echo checks[cite: 145, 146, 147].",
            [cite_start]"**Hardware:** Modem (long-distance), Switch (MAC-based LAN forwarding), and Router (IP-based)[cite: 148, 150, 151].",
            [cite_start]"**Addressing:** MAC (48-bit permanent) and IP (IPv4 32-bit or IPv6 128-bit)[cite: 152, 153]."
        ],
        "keywords": ["LAN", "WAN", "Protocol", "MAC address", "IP address", "Checksum", "Switch", "Router"],
        "quiz": [{"q": "Which device connects devices within a LAN using MAC addresses?", "a": "Switch"}]
    },
    "Security and Privacy": {
        [cite_start]"summary": "Protecting data confidentiality, integrity, and availability[cite: 154].",
        "detailed_notes": [
            [cite_start]"**Threats:** Malware (adware, spyware), Phishing (deceptive emails), and Pharming (URL redirection)[cite: 158].",
            [cite_start]"**Defenses:** Firewalls (packet filtering), Encryption (meaningless without key), and MFA[cite: 159, 161].",
            [cite_start]"**Legal:** PDPA (Singapore law regulating personal data consent and retention)[cite: 160]."
        ],
        "keywords": ["Confidentiality", "Integrity", "Phishing", "Pharming", "Encryption", "Firewall", "PDPA", "MFA"],
        "quiz": [{"q": "What does PDPA stand for?", "a": "Personal Data Protection Act"}]
    },
    "Intellectual Property": {
        [cite_start]"summary": "Legal protections for original digital creations of the mind[cite: 164].",
        "detailed_notes": [
            [cite_start]"**Copyright:** Control over use/distribution; only humans are recognized authors in Singapore[cite: 165, 166].",
            [cite_start]"**Software Licenses:** Proprietary (secret code), Freeware, FOSS (open source), and Public Domain[cite: 169, 172, 173].",
            [cite_start]"**Piracy:** Illegal copying or using cracks to bypass license detection[cite: 175].",
            [cite_start]"**Plagiarism:** Ethical offense of passing off others' work as your own[cite: 176]."
        ],
        "keywords": ["Copyright", "License", "Proprietary", "FOSS", "Freeware", "Piracy", "Plagiarism"],
        "quiz": [{"q": "Is AI-generated content copyrightable in Singapore?", "a": "No (requires a human author)"}]
    },
    "Impact of Computing": {
        [cite_start]"summary": "Transformation of society across industries and the spread of online falsehoods[cite: 178].",
        "detailed_notes": [
            [cite_start]"**Industries:** Communications (globalization), Education (personalized learning), and Retail (e-commerce)[cite: 181, 183, 189].",
            [cite_start]"**Falsehoods:** Filter bubbles created by social media algorithms increase misinformation[cite: 191].",
            [cite_start]"**POFMA:** Singapore law to combat fake news harming public interest[cite: 192, 193]."
        ],
        "keywords": ["Globalisation", "Digital Literacy", "Filter Bubble", "Misinformation", "POFMA"],
        "quiz": [{"q": "What Singapore law is used to issue correction directions for fake news?", "a": "POFMA"}]
    },
    "Emerging Technologies": {
        [cite_start]"summary": "Innovations like AI, Blockchain, and Quantum Computing that improve performance autonomously[cite: 194, 195].",
        "detailed_notes": [
            [cite_start]"**AI:** Narrow AI (specialized) vs. AGI (human-level)[cite: 197].",
            [cite_start]"**ML:** Detects patterns in data to produce models for inference[cite: 198, 199].",
            [cite_start]"**Blockchain:** Decentralized, immutable ledger linked via cryptographic hashes[cite: 204, 205].",
            [cite_start]"**Quantum:** Uses Qubits (superposition of 0 and 1) and Entanglement to solve problems exponentially faster[cite: 208, 209]."
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
# --- REVIEW MODE (FIXED) ---
if mode == "Review":
    st.title("Computing Study Companion")
    st.header(f"📖 Study Notes: {topic}")
    st.info(STATIONERY_DATA[topic]["summary"])
    
    col_notes, col_action = st.columns([2, 1])
    
    with col_notes:
        st.subheader("Key Concepts")
        notes_list = STATIONERY_DATA[topic].get("detailed_notes", [])
        if notes_list:
            for note in notes_list:
                st.markdown(f"- {note}")
        else:
            st.write("No detailed notes available yet.")

    with col_action:
        st.subheader("Reference Material")
        with st.container(border=True):
            st.write("Full Textbook Access")
            st.link_button("📂 Open PDF in Drive", TEXTBOOK_DRIVE_LINK)
            st.caption("Tip: Use the chapter titles to navigate the PDF.")

    st.divider()
    with st.expander("🔍 View AI-Extracted Context from Textbook"):
        if tb_content:
            st.markdown(tb_content)
        else:
            st.warning(f"No specific textbook context found for '{topic}'.")
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
