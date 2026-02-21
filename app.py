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
        [cite_start]"summary": "Describes how a computer is designed, built, organized, and how its various parts are connected to function. [cite: 2]",
        "detailed_notes": {
            "Units of Data": {
                [cite_start]"Digital System": "Computers perform calculations using binary data (0 or 1). [cite: 3]",
                "Measurement": [
                    [cite_start]"SI Prefixes (Power 1000): kB, MB, GB, TB, PB. [cite: 4]",
                    [cite_start]"Binary Prefixes (Power 1024): KiB, MiB, GiB, TiB, PiB. [cite: 4]"
                ]
            },
            "Hardware Components": {
                [cite_start]"CPU": "Processes data and executes instructions; speed is measured in MHz or GHz. [cite: 6]",
                [cite_start]"Main Memory": "RAM is volatile (loses data without power) and each byte has a unique address. [cite: 8] [cite_start]ROM is non-volatile and stores startup instructions. [cite: 8]",
                [cite_start]"Storage": "Magnetic (high capacity, low cost), Optical (laser-based), and Solid State (fast, durable, no moving parts). [cite: 10, 11]",
                "Buses": "Data Bus is bi-directional; [cite_start]Address Bus is uni-directional. [cite: 12]"
            },
            [cite_start]"Interfaces": "Includes USB (external), HDMI (AV output), and PCIe (internal expansion using lanes x1 to x16). [cite: 14, 15]"
        },
        "glossary": {
            [cite_start]"Computer Architecture": "The organization and connection of computer parts. [cite: 2]",
            [cite_start]"Volatile": "Memory that loses data when power is off, like RAM. [cite: 8]",
            [cite_start]"Address Bus": "Transports memory addresses in one direction only. [cite: 12]"
        },
        "keywords": ["CPU", "RAM", "Data Bus", "Address Bus", "PCIe", "Solid State"]
    },
    "Data Representation": {
        [cite_start]"summary": "All information is represented using electronic switches that are either ON (1) or OFF (0). [cite: 16]",
        "detailed_notes": {
            "Number Systems": {
                [cite_start]"Binary": "Base-2 (0 and 1). [cite: 19]",
                "Hexadecimal": "Base-16 (0-9, A-F). [cite_start]One hex digit maps to 4 binary bits. [cite: 23, 24]"
            },
            "Negative Numbers": {
                [cite_start]"Two's Complement": "Standard method; flip all bits and add 1. [cite: 26, 27]",
                [cite_start]"Sign Bit": "The MSB (Most Significant Bit) is 0 for positive and 1 for negative. [cite: 26]"
            },
            "Text Encoding": [
                [cite_start]"ASCII: 7-bit (128 chars) or Extended 8-bit (256 chars). [cite: 29, 30]",
                [cite_start]"Unicode: 8–32 bits, supports over a million global characters. [cite: 31]"
            ]
        },
        "glossary": {
            [cite_start]"Two's Complement": "A system for representing negative numbers in binary. [cite: 26]",
            [cite_start]"Overflow": "Error when a calculation result exceeds bit-length limits. [cite: 28]",
            [cite_start]"MSB": "Most Significant Bit; the sign bit in Two's Complement. [cite: 26]"
        },
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode"]
    },
    "Boolean Logic": {
        [cite_start]"summary": "Processor operations based on Boolean values (True/False) processed as bits. [cite: 33]",
        "detailed_notes": {
            [cite_start]"Truth Tables": "Shows output for every input combination; row count is 2^n. [cite: 33]",
            "Logic Gates": {
                [cite_start]"Basic": "AND (Q=A·B), OR (Q=A+B), NOT (Q=¬A). [cite: 35-38]",
                [cite_start]"Advanced": "NAND, NOR, and XOR (Q=A⊕B). [cite: 39-41]"
            },
            [cite_start]"Laws": "Includes Double Negation, De Morgan's Theorem, and Absorption ($A \cdot (A + B) = A$). [cite: 44-46]"
        },
        "glossary": {
            [cite_start]"Truth Table": "A table showing all possible logic gate inputs and outputs. [cite: 33]",
            [cite_start]"XOR": "Exclusive OR; output is 1 only when exactly one input is 1. [cite: 41]"
        },
        "keywords": ["Truth Table", "NAND", "XOR", "De Morgan's Theorem", "Logic Circuits"]
    },
    "Programming Concepts": {
        [cite_start]"summary": "Algorithms (step-by-step instructions) converted into source code for execution. [cite: 52]",
        "detailed_notes": {
            [cite_start]"Variables": "Named identifiers referencing memory addresses (id() function). [cite: 55, 56]",
            [cite_start]"Data Types": "bool, int, float, str, list (mutable/ordered), and dict (key-value pairs). [cite: 59, 60]",
            "Control Flow": {
                [cite_start]"Sequence": "Fixed order. [cite: 68]",
                [cite_start]"Selection": "if-elif-else branching. [cite: 68]",
                [cite_start]"Iteration": "while and for loops. [cite: 68]"
            }
        },
        "glossary": {
            [cite_start]"Algorithm": "Step-by-step instructions to solve a problem. [cite: 52]",
            [cite_start]"Scope": "The accessibility of variables (local vs global). [cite: 70]"
        },
        "keywords": ["Variables", "List", "Dictionary", "Loops", "Functions", "Scope"]
    },
    "Validation and Testing": {
        [cite_start]"summary": "Techniques to ensure data integrity and identify program bugs. [cite: 74, 86]",
        "detailed_notes": {
            [cite_start]"Validation Checks": "Includes Length, Range, Presence, Format, and Existence checks. [cite: 77-81]",
            "Program Errors": [
                [cite_start]"Syntax: Violation of language rules (spelling, punctuation). [cite: 87, 88]",
                [cite_start]"Logic: Incorrect results (wrong formulas or sequencing). [cite: 90, 91]",
                [cite_start]"Run-time: Errors during execution (division by zero). [cite: 92]"
            ],
            [cite_start]"Testing": "Comparing actual vs expected output under normal, boundary, and error conditions. [cite: 94, 95]"
        },
        "glossary": {
            [cite_start]"Check Digit": "Extra digit added to detect manual entry errors. [cite: 83]",
            [cite_start]"Debugging": "Process of identifying and removing program defects. [cite: 86]"
        },
        "keywords": ["Validation", "Syntax Error", "Logic Error", "Debugging", "Test Case"]
    },
    "Development Models": {
        [cite_start]"summary": "Structured approaches to software creation and management. [cite: 109]",
        "detailed_notes": {
            [cite_start]"Waterfall Model": "Sequential stages from gathering requirements to deployment. [cite: 109-118]",
            "Modern Models": [
                [cite_start]"Iterative: Revisiting stages as requirements change. [cite: 119]",
                [cite_start]"Agile: Small increments with continuous feedback and sprints. [cite: 120]",
                [cite_start]"TDD: Write tests first, then code to pass them. [cite: 121]"
            ]
        },
        "glossary": {
            [cite_start]"Beta Testing": "Testing in the user environment. [cite: 115]",
            [cite_start]"Sprint": "Short development cycle in Agile. [cite: 120]"
        },
        "keywords": ["Waterfall", "Agile", "Iterative", "TDD", "Sprints", "Requirements"]
    },
    "Spreadsheets": {
        [cite_start]"summary": "Tools for data analysis using formulas and logical functions. [cite: 122]",
        "detailed_notes": {
            [cite_start]"Basics": "Cells (A1) and Ranges (A1:C3); formulas start with =. [cite: 122]",
            [cite_start]"References": "Relative (A1), Absolute ($A$1), and Mixed (A$1 or $A1). [cite: 123]",
            "Functions": [
                [cite_start]"Lookup: VLOOKUP, HLOOKUP, and INDEX+MATCH. [cite: 128, 130]",
                [cite_start]"Logical: IF, AND, OR, NOT. [cite: 124, 125]",
                [cite_start]"Math: SUMIF, AVERAGEIF, COUNTIF. [cite: 126]"
            ]
        },
        "glossary": {
            [cite_start]"Absolute Reference": "A cell reference that stays locked when copied. [cite: 123]",
            [cite_start]"VLOOKUP": "Function used to search for data in columns. [cite: 128]"
        },
        "keywords": ["Formulas", "VLOOKUP", "Absolute Reference", "IF Function", "Goal Seek"]
    },
    "Computer Networks": {
        [cite_start]"summary": "Devices connected via transmission media to exchange data. [cite: 132]",
        "detailed_notes": {
            [cite_start]"Types": "LAN (local), MAN (city), and WAN (Internet). [cite: 136-139]",
            "Hardware": [
                [cite_start]"Modem: Converts digital data for long-distance media. [cite: 147]",
                [cite_start]"Switch: Connects LAN devices using MAC addresses. [cite: 149]",
                [cite_start]"Router: Forwards packets between networks using IP addresses. [cite: 151]"
            ],
            [cite_start]"Addressing": "MAC (48-bit, permanent) and IP (IPv4 32-bit or IPv6 128-bit). [cite: 151-153]"
        },
        "glossary": {
            [cite_start]"Protocol": "Rules governing communication (e.g., TCP/IP). [cite: 143]",
            [cite_start]"Parity Bit": "Error detection method adding a bit to make 1-bits even or odd. [cite: 144]"
        },
        "keywords": ["LAN", "Router", "Switch", "IP Address", "MAC Address", "TCP/IP"]
    },
    "Security and Privacy": {
        [cite_start]"summary": "Protecting data confidentiality, integrity, and availability. [cite: 154]",
        "detailed_notes": {
            [cite_start]"Threats": "Malware (adware, spyware), phishing, and pharming. [cite: 157, 158]",
            [cite_start]"Defenses": "Anti-malware, firewalls, encryption, and MFA (Something you know, own, or are). [cite: 159-161]",
            [cite_start]"Legal": "Singapore's PDPA requires consent and limited data retention. [cite: 159]"
        },
        "glossary": {
            [cite_start]"Phishing": "Deceptive emails used to trick users into revealing data. [cite: 158]",
            [cite_start]"MFA": "Multi-Factor Authentication using multiple verification types. [cite: 160]"
        },
        "keywords": ["Encryption", "Firewall", "Phishing", "MFA", "PDPA", "Malware"]
    },
    "Intellectual Property": {
        [cite_start]"summary": "Legal protections for original digital creations. [cite: 164]",
        "detailed_notes": {
            "Copyright": "Control over use/distribution; [cite_start]AI-generated content is not copyrightable in Singapore. [cite: 165-167]",
            "Software Licenses": [
                [cite_start]"Proprietary: Source code secret; no copying. [cite: 168]",
                [cite_start]"FOSS: Users can copy, modify, and share source code. [cite: 171]",
                [cite_start]"Freeware vs Shareware: Free forever vs evaluation demos. [cite: 169, 170]"
            ]
        },
        "glossary": {
            [cite_start]"Plagiarism": "Ethical offense of passing off others' work as your own. [cite: 175]",
            [cite_start]"FOSS": "Free and Open-Source Software. [cite: 171]"
        },
        "keywords": ["Copyright", "FOSS", "Software Piracy", "License", "Plagiarism"]
    },
    "Emerging Technologies": {
        [cite_start]"summary": "Advanced technologies including AI, Blockchain, and Quantum Computing. [cite: 194]",
        "detailed_notes": {
            "AI & ML": "Autonomy and adaptivity; [cite_start]ML derives rules from data patterns. [cite: 194, 198]",
            [cite_start]"Blockchain": "Decentralized, immutable ledger linked via hashes. [cite: 204]",
            [cite_start]"Quantum": "Uses Qubits (superposition) and Entanglement to solve problems faster. [cite: 207-209]"
        },
        "glossary": {
            [cite_start]"Qubit": "A quantum bit that can exist as 0 and 1 simultaneously. [cite: 207]",
            [cite_start]"Superposition": "The ability of a qubit to be in multiple states at once. [cite: 207]"
        },
        "keywords": ["Artificial Intelligence", "Blockchain", "Quantum Computing", "Qubit", "Machine Learning"]
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
