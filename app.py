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
        "summary": "Describes how a computer is designed, built, organized, and how its various parts are connected to function.",
        "detailed_notes": {
            "Units of Data": {
                "Digital System": "Computers perform calculations using binary data (0 or 1).",
                "Measurement": [
                    "SI Prefixes (Power 1000): kB, MB, GB, TB, PB.",
                    "Binary Prefixes (Power 1024): KiB, MiB, GiB, TiB, PiB."
                ]
            },
            "Hardware Components": {
                "CPU": "Processes data and executes instructions; speed is measured in MHz or GHz.",
                "Main Memory": "RAM is volatile (loses data without power) and each byte has a unique address. ROM is non-volatile and stores startup instructions.",
                "Storage": "Magnetic (high capacity, low cost), Optical (laser-based), and Solid State (fast, durable, no moving parts).",
                "Buses": "Data Bus is bi-directional; Address Bus is uni-directional."
            },
            "Interfaces": "Includes USB (external), HDMI (AV output), and PCIe (internal expansion using lanes x1 to x16)."
        },
        "glossary": {
            "Computer Architecture": "The organization and connection of computer parts.",
            "Volatile": "Memory that loses data when power is off, like RAM.",
            "Address Bus": "Transports memory addresses in one direction only."
        },
        "keywords": ["CPU", "RAM", "Data Bus", "Address Bus", "PCIe", "Solid State"]
    },

    "Data Representation": {
        "summary": "All information is represented using electronic switches that are either ON (1) or OFF (0).",
        "detailed_notes": {
            "Number Systems": {
                "Binary": "Base-2 (0 and 1).",
                "Hexadecimal": "Base-16 (0-9, A-F). One hex digit maps to 4 binary bits."
            },
            "Negative Numbers": {
                "Two's Complement": "Standard method; flip all bits and add 1.",
                "Sign Bit": "The MSB (Most Significant Bit) is 0 for positive and 1 for negative."
            },
            "Text Encoding": [
                "ASCII: 7-bit (128 chars) or Extended 8-bit (256 chars).",
                "Unicode: 8–32 bits, supports over a million global characters."
            ]
        },
        "glossary": {
            "Two's Complement": "A system for representing negative numbers in binary.",
            "Overflow": "Error when a calculation result exceeds bit-length limits.",
            "MSB": "Most Significant Bit; the sign bit in Two's Complement."
        },
        "keywords": ["Binary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode"]
    },

    "Boolean Logic": {
        "summary": "Processor operations based on Boolean values (True/False) processed as bits.",
        "detailed_notes": {
            "Truth Tables": "Shows output for every input combination; row count is 2^n.",
            "Logic Gates": {
                "Basic": "AND (Q=A·B), OR (Q=A+B), NOT (Q=¬A).",
                "Advanced": "NAND, NOR, and XOR (Q=A⊕B)."
            },
            "Laws": "Includes Double Negation, De Morgan's Theorem, and Absorption (A · (A + B) = A)."
        },
        "glossary": {
            "Truth Table": "A table showing all possible logic gate inputs and outputs.",
            "XOR": "Exclusive OR; output is 1 only when exactly one input is 1."
        },
        "keywords": ["Truth Table", "NAND", "XOR", "De Morgan's Theorem", "Logic Circuits"]
    },

    "Programming Concepts": {
        "summary": "Algorithms (step-by-step instructions) converted into source code for execution.",
        "detailed_notes": {
            "Variables": "Named identifiers referencing memory addresses.",
            "Data Types": "bool, int, float, str, list (mutable/ordered), and dict (key-value pairs).",
            "Control Flow": {
                "Sequence": "Fixed order.",
                "Selection": "if-elif-else branching.",
                "Iteration": "while and for loops."
            }
        },
        "glossary": {
            "Algorithm": "Step-by-step instructions to solve a problem.",
            "Scope": "The accessibility of variables (local vs global)."
        },
        "keywords": ["Variables", "List", "Dictionary", "Loops", "Functions", "Scope"]
    },

    "Validation and Testing": {
        "summary": "Techniques to ensure data integrity and identify program bugs.",
        "detailed_notes": {
            "Validation Checks": "Includes Length, Range, Presence, Format, and Existence checks.",
            "Program Errors": [
                "Syntax: Violation of language rules (spelling, punctuation).",
                "Logic: Incorrect results (wrong formulas or sequencing).",
                "Run-time: Errors during execution (division by zero)."
            ],
            "Testing": "Comparing actual vs expected output under normal, boundary, and error conditions."
        },
        "glossary": {
            "Check Digit": "Extra digit added to detect manual entry errors.",
            "Debugging": "Process of identifying and removing program defects."
        },
        "keywords": ["Validation", "Syntax Error", "Logic Error", "Debugging", "Test Case"]
    },

    "Development Models": {
        "summary": "Structured approaches to software creation and management.",
        "detailed_notes": {
            "Waterfall Model": "Sequential stages from gathering requirements to deployment.",
            "Modern Models": [
                "Iterative: Revisiting stages as requirements change.",
                "Agile: Small increments with continuous feedback and sprints.",
                "TDD: Write tests first, then code to pass them."
            ]
        },
        "glossary": {
            "Beta Testing": "Testing in the user environment.",
            "Sprint": "Short development cycle in Agile."
        },
        "keywords": ["Waterfall", "Agile", "Iterative", "TDD", "Sprints", "Requirements"]
    },

    "Spreadsheets": {
        "summary": "Tools for data analysis using formulas and logical functions.",
        "detailed_notes": {
            "Basics": "Cells (A1) and Ranges (A1:C3); formulas start with =.",
            "References": "Relative (A1), Absolute ($A$1), and Mixed (A$1 or $A1).",
            "Functions": [
                "Lookup: VLOOKUP, HLOOKUP, and INDEX+MATCH.",
                "Logical: IF, AND, OR, NOT.",
                "Math: SUMIF, AVERAGEIF, COUNTIF."
            ]
        },
        "glossary": {
            "Absolute Reference": "A cell reference that stays locked when copied.",
            "VLOOKUP": "Function used to search for data in columns."
        },
        "keywords": ["Formulas", "VLOOKUP", "Absolute Reference", "IF Function", "Goal Seek"]
    },

    "Computer Networks": {
        "summary": "Devices connected via transmission media to exchange data.",
        "detailed_notes": {
            "Types": "LAN (local), MAN (city), and WAN (Internet).",
            "Hardware": [
                "Modem: Converts digital data for long-distance media.",
                "Switch: Connects LAN devices using MAC addresses.",
                "Router: Forwards packets between networks using IP addresses."
            ],
            "Addressing": "MAC (48-bit, permanent) and IP (IPv4 32-bit or IPv6 128-bit)."
        },
        "glossary": {
            "Protocol": "Rules governing communication (e.g., TCP/IP).",
            "Parity Bit": "Error detection method adding a bit to make 1-bits even or odd."
        },
        "keywords": ["LAN", "Router", "Switch", "IP Address", "MAC Address", "TCP/IP"]
    },

    "Security and Privacy": {
        "summary": "Protecting data confidentiality, integrity, and availability.",
        "detailed_notes": {
            "Threats": "Malware (adware, spyware), phishing, and pharming.",
            "Defenses": "Anti-malware, firewalls, encryption, and MFA (Something you know, own, or are).",
            "Legal": "Singapore's PDPA requires consent and limited data retention."
        },
        "glossary": {
            "Phishing": "Deceptive emails used to trick users into revealing data.",
            "MFA": "Multi-Factor Authentication using multiple verification types."
        },
        "keywords": ["Encryption", "Firewall", "Phishing", "MFA", "PDPA", "Malware"]
    },

    "Intellectual Property": {
        "summary": "Legal protections for original digital creations.",
        "detailed_notes": {
            "Copyright": "Control over use/distribution; AI-generated content is not copyrightable in Singapore.",
            "Software Licenses": [
                "Proprietary: Source code secret; no copying.",
                "FOSS: Users can copy, modify, and share source code.",
                "Freeware vs Shareware: Free forever vs evaluation demos."
            ]
        },
        "glossary": {
            "Plagiarism": "Ethical offense of passing off others' work as your own.",
            "FOSS": "Free and Open-Source Software."
        },
        "keywords": ["Copyright", "FOSS", "Software Piracy", "License", "Plagiarism"]
    },

    "Emerging Technologies": {
        "summary": "Advanced technologies including AI, Blockchain, and Quantum Computing.",
        "detailed_notes": {
            "AI & ML": "Autonomy and adaptivity; ML derives rules from data patterns.",
            "Blockchain": "Decentralized, immutable ledger linked via hashes.",
            "Quantum": "Uses Qubits (superposition) and Entanglement to solve problems faster."
        },
        "glossary": {
            "Qubit": "A quantum bit that can exist as 0 and 1 simultaneously.",
            "Superposition": "The ability of a qubit to be in multiple states at once."
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
# 5. Fetch Content for AI Bot/Review (Ater topic is defined)
def display_nested_notes(data, level=0):
    """Recursively displays dictionary content as nested markdown."""
    if isinstance(data, dict):
        for key, value in data.items():
            # Format the key into a nice title (e.g., 'si_prefixes' -> 'Si Prefixes')
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
