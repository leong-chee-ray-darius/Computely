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
        "summary": "Study of how computers are designed, built, organized, and how their components interact to process data.",
        "detailed_notes": {
            "Overview": {
                "Computer System": "A device that receives, processes, and outputs data according to instructions.",
                "Historical Context": "Early computers used mechanical parts such as gears, pulleys, and levers before electronics."
            },
            "Units of Data": {
                "Digital System": "Computers use binary (0 and 1).",
                "Bit": "Smallest unit of data (0 or 1).",
                "Byte": "8 bits.",
                "Measurement": [
                    "SI Prefixes (1000): kB, MB, GB, TB, PB",
                    "Binary Prefixes (1024): KiB, MiB, GiB, TiB, PiB"
                ]
            },
            "Hardware Components": {
                "CPU": "Processes data and executes instructions. Speed measured in MHz or GHz. Multi-core CPUs can execute multiple instructions simultaneously.",
                "GPU": "Specialized processor for graphics and AI tasks.",
                "Main Memory": "RAM is volatile and stores running programs. ROM is non-volatile and stores startup instructions.",
                "Storage": {
                    "Magnetic": "High capacity, low cost, vulnerable to shock and magnets.",
                    "Optical": "Laser-based, portable, scratch-sensitive.",
                    "Solid State": "Fast, durable, no moving parts, higher cost."
                },
                "Buses": {
                    "Data Bus": "Bi-directional, transfers data.",
                    "Address Bus": "Uni-directional, transfers memory addresses."
                }
            },
            "Interfaces": {
                "USB": "External device connection (480 Mbit/s – 80 Gbit/s).",
                "HDMI": "High-definition audio/video output.",
                "PCIe": "Internal expansion using lanes x1 to x16."
            }
        },
        "glossary": {
            "CPU": "Central Processing Unit that executes instructions.",
            "Volatile": "Memory that loses data when power is lost.",
            "ROM": "Non-volatile memory storing startup instructions.",
            "Data Bus": "Transfers data between components.",
            "Address Bus": "Transfers memory addresses."
        },
        "keywords": ["CPU", "RAM", "ROM", "GPU", "Data Bus", "Address Bus", "PCIe", "Solid State"]
    },

    "Data Representation": {
        "summary": "All data in computers is represented using binary numbers (0 and 1).",
        "detailed_notes": {
            "Number Systems": {
                "Denary": "Base-10 using digits 0–9.",
                "Binary": "Base-2 using digits 0 and 1.",
                "Hexadecimal": "Base-16 using digits 0–9 and A–F."
            },
            "Conversions": {
                "Binary ↔ Denary": "Use place values or repeated division.",
                "Binary ↔ Hex": "Group binary into 4-bit sections.",
                "Largest Number": "2^N - 1"
            },
            "Negative Numbers": {
                "System": "Two's Complement",
                "Sign Bit": "MSB determines sign (0 positive, 1 negative).",
                "Range": "-2^(N-1) to 2^(N-1) - 1",
                "Steps": [
                    "Convert to binary",
                    "Add leading zeros",
                    "Invert bits",
                    "Add 1"
                ]
            },
            "Text Encoding": {
                "ASCII": "7-bit (128 chars), Extended 8-bit (256 chars).",
                "Unicode": "8–32 bits, supports global languages."
            }
        },
        "glossary": {
            "Binary": "Base-2 number system.",
            "Hexadecimal": "Base-16 number system.",
            "Two's Complement": "Binary system for negative numbers.",
            "MSB": "Most Significant Bit.",
            "Overflow": "Result exceeds allowed bit size."
        },
        "keywords": ["Binary", "Denary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode"]
    },

    "Boolean Logic": {
        "summary": "Uses logical values and gates to perform decision-making operations in computers.",
        "detailed_notes": {
            "Boolean Values": ["True/False", "1/0", "On/Off"],
            "Truth Tables": "Shows output for all input combinations. Rows = 2^n.",
            "Logic Gates": {
                "AND": "Output 1 only if both inputs are 1.",
                "OR": "Output 1 if any input is 1.",
                "NOT": "Inverts input.",
                "NAND": "NOT AND.",
                "NOR": "NOT OR.",
                "XOR": "Output 1 only when inputs differ."
            },
            "Boolean Laws": {
                "Double Negation": "¬(¬A) = A",
                "De Morgan": ["¬(A · B) = ¬A + ¬B", "¬(A + B) = ¬A · ¬B"],
                "Absorption": ["A · (A + B) = A", "A + (A · B) = A"]
            },
            "Logic Circuits": "Built by connecting logic gates to perform tasks."
        },
        "glossary": {
            "Truth Table": "Table showing outputs for all input combinations.",
            "Logic Gate": "Electronic circuit performing logical operations.",
            "XOR": "Exclusive OR gate."
        },
        "keywords": ["Truth Table", "Logic Gates", "XOR", "NAND", "Boolean Algebra"]
    },

    "Programming Concepts": {
        "summary": "Algorithms and programming techniques used to create computer programs.",
        "detailed_notes": {
            "Algorithms": "Step-by-step solution to a problem.",
            "Variables": "Named storage locations referencing memory.",
            "Data Types": ["bool", "int", "float", "str", "list", "dict"],
            "Operators": ["+", "-", "*", "/", "//", "%", "**"],
            "Control Flow": {
                "Sequence": "Statements run in order.",
                "Selection": "if / elif / else branching.",
                "Iteration": ["while loop", "for loop"]
            },
            "Functions": "Reusable blocks of code.",
            "Scope": {
                "Local": "Inside function.",
                "Global": "Outside function."
            }
        },
        "glossary": {
            "Algorithm": "Step-by-step instructions.",
            "Variable": "Stores changeable values.",
            "Function": "Reusable code block.",
            "Scope": "Where variables can be accessed."
        },
        "keywords": ["Algorithm", "Variables", "Loops", "Functions", "Data Types", "Scope"]
    },

    "Validation and Testing": {
        "summary": "Methods to ensure correct data input and program correctness.",
        "detailed_notes": {
            "Validation Checks": ["Length", "Range", "Presence", "Format", "Existence", "Check Digit"],
            "Error Types": {
                "Syntax": "Language rule violations.",
                "Logic": "Incorrect output.",
                "Run-time": "Errors during execution."
            },
            "Testing": "Compare actual output with expected output using normal, boundary, and error cases.",
            "Debugging": "Identifying and removing bugs."
        },
        "glossary": {
            "Validation": "Ensuring correct input.",
            "Debugging": "Removing errors.",
            "Test Case": "Input + expected output."
        },
        "keywords": ["Validation", "Debugging", "Syntax Error", "Logic Error", "Test Case"]
    },

    "Development Models": {
        "summary": "Structured approaches to software development.",
        "detailed_notes": {
            "Waterfall": "Sequential stages: requirements → design → coding → testing → deployment.",
            "Iterative": "Repeated cycles of development.",
            "Agile": "Short sprints with continuous feedback.",
            "TDD": "Write tests before writing code."
        },
        "glossary": {
            "Sprint": "Short development cycle.",
            "Beta Testing": "User environment testing."
        },
        "keywords": ["Waterfall", "Agile", "Iterative", "TDD", "Sprint"]
    },

    "Spreadsheets": {
        "summary": "Tools for data storage, analysis, and calculations using formulas and functions.",
        "detailed_notes": {
            "Basics": "Cells (A1), ranges (A1:C3), formulas start with =.",
            "References": ["Relative", "Absolute", "Mixed"],
            "Functions": {
                "Logical": ["IF", "AND", "OR", "NOT"],
                "Math": ["SUM", "AVERAGE", "COUNT", "MAX", "MIN"],
                "Lookup": ["VLOOKUP", "HLOOKUP", "INDEX", "MATCH"],
                "Text": ["LEFT", "RIGHT", "MID", "LEN"]
            }
        },
        "glossary": {
            "Formula": "Equation that calculates a value.",
            "Absolute Reference": "Cell reference that does not change.",
            "VLOOKUP": "Vertical lookup function."
        },
        "keywords": ["Formula", "VLOOKUP", "Functions", "Cell Reference", "Goal Seek"]
    },

    "Computer Networks": {
        "summary": "Interconnected devices exchanging data through communication channels.",
        "detailed_notes": {
            "Types": ["LAN", "MAN", "WAN"],
            "Topologies": ["Star", "Mesh"],
            "Hardware": ["Router", "Switch", "Modem", "NIC", "WAP"],
            "Addressing": {
                "MAC": "48-bit permanent address.",
                "IP": ["IPv4 (32-bit)", "IPv6 (128-bit)"]
            },
            "Protocols": "Rules governing data transmission (TCP/IP)."
        },
        "glossary": {
            "Router": "Forwards data between networks.",
            "Switch": "Connects devices within LAN.",
            "Protocol": "Communication rules."
        },
        "keywords": ["LAN", "Router", "Switch", "IP Address", "MAC Address", "TCP/IP"]
    },

    "Security and Privacy": {
        "summary": "Protection of data confidentiality, integrity, and availability.",
        "detailed_notes": {
            "Threats": ["Malware", "Phishing", "Pharming", "Spyware", "Adware"],
            "Defenses": ["Anti-malware", "Firewalls", "Encryption", "MFA", "PDPA"],
            "Good Practices": ["Strong passwords", "Backups", "MFA", "Scam awareness"]
        },
        "glossary": {
            "Encryption": "Encoding data for security.",
            "Phishing": "Fake messages to steal information.",
            "MFA": "Multi-Factor Authentication."
        },
        "keywords": ["Security", "Encryption", "Firewall", "Phishing", "MFA", "PDPA"]
    },

    "Intellectual Property": {
        "summary": "Legal rights protecting digital creations.",
        "detailed_notes": {
            "Copyright": "Controls usage and distribution.",
            "Licenses": ["Proprietary", "Freeware", "Shareware", "FOSS", "Public Domain"],
            "Piracy": "Illegal copying or distribution of software.",
            "Plagiarism": "Claiming others' work as your own."
        },
        "glossary": {
            "FOSS": "Free and Open-Source Software.",
            "Plagiarism": "Ethical offense."
        },
        "keywords": ["Copyright", "FOSS", "Piracy", "License", "Plagiarism"]
    },

    "Emerging Technologies": {
        "summary": "Advanced computing technologies shaping the future.",
        "detailed_notes": {
            "Artificial Intelligence": "Systems capable of autonomous learning and decision making.",
            "Machine Learning": "AI method that learns patterns from data.",
            "Blockchain": "Decentralized, immutable digital ledger.",
            "Quantum Computing": "Computing using qubits, superposition, and entanglement.",
            "VR & AR": "Immersive and augmented digital environments."
        },
        "glossary": {
            "Qubit": "Quantum bit that exists as 0 and 1 simultaneously.",
            "Superposition": "Ability to exist in multiple states.",
            "Entanglement": "Linked quantum states."
        },
        "keywords": ["AI", "Machine Learning", "Blockchain", "Quantum Computing", "Qubit", "VR", "AR"]
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
