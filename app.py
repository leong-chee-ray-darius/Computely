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
        "summary": "The study of how computer systems are structured, how hardware components interact, and how data is processed and transferred inside a computer.",
        "detailed_notes": {
            "Overview": {
                "Computer System": "An electronic device that accepts input, processes data according to stored instructions, stores data, and produces output."
                }
            },
        "Units of Data": {
                "Bit": "Smallest unit of data represented as 0 or 1.",
                "Byte": "8 bits.",
                "Word": "Group of bits processed together by CPU (e.g., 32-bit or 64-bit).",
                "Storage Measurement": {
                    "SI": ["kB", "MB", "GB", "TB", "PB"],
                    "Binary": ["KiB", "MiB", "GiB", "TiB", "PiB"]
                }
            },
        "Hardware Components": {
                "CPU": {
                    "Description": "Processes instructions and performs calculations.",
                    "Components": ["ALU", "Control Unit", "Registers", "Cache"],
                    "Clock Speed": "Measured in GHz, determines number of cycles per second.",
                    "Cores": "Multiple cores allow parallel execution."
                },
                "GPU": "Handles graphics rendering and parallel computations such as AI training.",
                "Main Memory": {
                    "RAM": "Volatile memory storing programs and data currently in use.",
                    "ROM": "Non-volatile memory storing firmware and boot instructions."
                },
                "Secondary Storage": {
                    "HDD": "Magnetic disks, cheap, slow, mechanical parts.",
                    "SSD": "Solid-state, fast, durable, no moving parts.",
                    "Optical": "CD, DVD, Blu-ray, portable but slow."
                },
                "Buses": {
                    "Data Bus": "Transfers actual data.",
                    "Address Bus": "Transfers memory locations.",
                    "Control Bus": "Transfers control signals."
                }
            },
        "Interfaces": {
                "USB": "Universal connection for peripherals.",
                "HDMI": "High-definition video and audio transmission.",
                "PCIe": "High-speed internal expansion interface.",
                "Ethernet": "Wired network communication."
            }
        },
    "glossary": {
            "CPU": "Central Processing Unit responsible for executing instructions.",
            "ALU": "Performs arithmetic and logical operations.",
            "Register": "Extremely fast storage inside CPU.",
            "RAM": "Volatile main memory.",
            "ROM": "Permanent memory storing boot data."
        },
        "keywords": ["CPU", "ALU", "Registers", "RAM", "ROM", "Fetch Decode Execute", "Buses", "Cache"]
    },
"Data Representation": {
        "summary": "All computer data is stored and processed using binary numbers and encoding systems.",
        "detailed_notes": {
            "Number Systems": {
                "Denary": "Base-10 system used by humans.",
                "Binary": "Base-2 system used internally by computers.",
                "Hexadecimal": "Base-16 compact representation of binary."
            },
            "Conversions": {
                "Binary to Denary": "Multiply each bit by its place value and sum.",
                "Denary to Binary": "Repeated division by 2.",
                "Binary to Hex": "Group bits into 4s."
            },
            "Negative Numbers": {
                "Method": "Two's Complement",
                "Range": "-2^(n-1) to 2^(n-1) - 1",
                "Process": ["Invert bits", "Add 1"]
            },
            "Overflow": "Occurs when a result exceeds the available number of bits.",
            "Text Encoding": {
                "ASCII": "7-bit character encoding.",
                "Unicode": "Global encoding supporting many languages."
            },
            "Image Representation": {
                "Pixels": "Smallest dot in an image.",
                "Resolution": "Total number of pixels.",
                "Colour Depth": "Bits per pixel determining number of colours."
            },
            "Sound Representation": {
                "Sampling": "Taking sound measurements at regular intervals.",
                "Sample Rate": "Number of samples per second.",
                "Bit Depth": "Accuracy of each sample."
            }
        },
        "glossary": {
            "Binary": "Base-2 numbering system.",
            "Hexadecimal": "Base-16 numbering system.",
            "Two's Complement": "Method for representing negative binary numbers.",
            "Overflow": "When binary result exceeds bit limit."
        },
        "keywords": ["Binary", "Denary", "Hexadecimal", "Two's Complement", "ASCII", "Unicode", "Resolution", "Sampling"]
    },
"Boolean Logic": {
        "summary": "Logical operations used inside computers to make decisions and control data flow.",
        "detailed_notes": {
            "Logic Levels": ["1 / True / On", "0 / False / Off"],
            "Logic Gates": {
                "AND": "Outputs 1 only if both inputs are 1.",
                "OR": "Outputs 1 if any input is 1.",
                "NOT": "Inverts the input.",
                "NAND": "NOT AND.",
                "NOR": "NOT OR.",
                "XOR": "Outputs 1 only if inputs differ."
            },
            "Truth Tables": "Lists all possible input combinations and outputs.",
            "Boolean Laws": {
                "Identity": ["A + 0 = A", "A · 1 = A"],
                "Null": ["A + 1 = 1", "A · 0 = 0"],
                "De Morgan": ["¬(A·B)=¬A+¬B", "¬(A+B)=¬A·¬B"]
            },
            "Logic Circuits": "Combination of logic gates forming hardware decision systems."
        },
        "glossary": {
            "Truth Table": "Table showing outputs for all possible inputs.",
            "Logic Gate": "Electronic decision-making circuit."
        },
        "keywords": ["AND", "OR", "NOT", "XOR", "Truth Table", "Boolean Algebra"]
    },
"Programming Concepts": {
        "summary": "Core programming principles used to design, write, and test programs.",
        "detailed_notes": {
            "Algorithms": "Step-by-step solution to a problem.",
            "Variables": "Named memory storage.",
            "Data Types": ["Integer", "Float", "Boolean", "String", "List", "Dictionary"],
            "Operators": {
                "Arithmetic": ["+", "-", "*", "/", "%", "**"],
                "Comparison": ["==", "!=", ">", "<", ">=", "<="],
                "Logical": ["and", "or", "not"]
            },
            "Control Structures": {
                "Sequence": "Instructions run in order.",
                "Selection": "if, elif, else.",
                "Iteration": ["for loop", "while loop"]
            },
            "Functions": "Reusable blocks of code performing specific tasks.",
            "Testing": ["Normal", "Boundary", "Erroneous"]
        },
        "glossary": {
            "Algorithm": "Set of instructions.",
            "Iteration": "Repeating a block of code."
        },
        "keywords": ["Algorithm", "Variables", "Loops", "Functions", "Operators"]
    },
    # 5
    "Validation and Testing": {
        "summary": "Methods used to ensure correctness of input data and to detect, prevent, and fix program errors.",
        "detailed_notes": {
            "Validation": {
                "Purpose": "Ensures data is sensible and reasonable before processing.",
                "Checks": [
                    "Presence Check",
                    "Length Check",
                    "Range Check",
                    "Format Check",
                    "Existence Check",
                    "Check Digit"
                ]
            },
            "Verification": {
                "Purpose": "Ensures data entered matches original data.",
                "Methods": ["Double Entry", "Visual Check"]
            },
            "Error Types": {
                "Syntax": "Violation of language rules.",
                "Logic": "Incorrect program behaviour.",
                "Runtime": "Occurs during execution (e.g. divide by zero)."
            },
            "Testing": {
                "Normal": "Valid values within range.",
                "Boundary": "Values at limits.",
                "Erroneous": "Invalid values."
            },
            "Debugging": "Process of locating and correcting errors."
        },
        "glossary": {
            "Validation": "Checking data reasonableness.",
            "Verification": "Checking data accuracy.",
            "Debugging": "Fixing program errors."
        },
        "keywords": ["Validation", "Verification", "Syntax Error", "Logic Error", "Runtime Error", "Testing"]
    },

    # 6
    "Development Models": {
        "summary": "Structured approaches used to plan, build, test, and maintain software systems.",
        "detailed_notes": {
            "Waterfall": {
                "Stages": ["Requirements", "Design", "Implementation", "Testing", "Deployment", "Maintenance"],
                "Features": "Sequential, rigid, documentation-heavy."
            },
            "Iterative": {
                "Features": "Repeated refinement cycles.",
                "Advantage": "Early detection of problems."
            },
            "Agile": {
                "Features": ["Sprints", "User feedback", "Incremental development"],
                "Advantage": "Flexible and fast delivery."
            },
            "TDD": {
                "Process": ["Write tests", "Write code", "Refactor"],
                "Advantage": "Higher code reliability."
            }
        },
        "glossary": {
            "Sprint": "Short development cycle.",
            "Prototype": "Early test version."
        },
        "keywords": ["Waterfall", "Agile", "Iterative", "TDD", "Sprint"]
    },

    # 7
    "Spreadsheets": {
        "summary": "Spreadsheet tools used for calculation, modelling, and data analysis.",
        "detailed_notes": {
            "Basics": ["Cells", "Ranges", "Formulas", "Functions"],
            "Cell References": ["Relative", "Absolute", "Mixed"],
            "Functions": {
                "Logical": ["IF", "AND", "OR", "NOT"],
                "Math": ["SUM", "AVERAGE", "MAX", "MIN", "COUNT"],
                "Lookup": ["VLOOKUP", "HLOOKUP", "INDEX", "MATCH"]
            },
            "What-If Analysis": ["Goal Seek", "Scenario Manager"]
        },
        "glossary": {
            "Formula": "Expression that calculates a value.",
            "Absolute Reference": "Cell reference that does not change."
        },
        "keywords": ["Spreadsheet", "Formulas", "Functions", "VLOOKUP", "Goal Seek"]
    },
    "Computer Networks": {
        "summary": "Systems of interconnected devices that communicate to exchange data.",
        "detailed_notes": {
            "Network Types": ["LAN", "MAN", "WAN"],
            "Topologies": ["Star", "Bus", "Ring", "Mesh"],
            "Hardware": {
                "Router": "Routes data between networks.",
                "Switch": "Connects devices within LAN.",
                "NIC": "Provides network connectivity.",
                "WAP": "Wireless connection point."
            },
            "Protocols": {
                "TCP/IP": "Core internet communication protocol.",
                "HTTP/HTTPS": "Web data transfer.",
                "FTP": "File transfer."
            },
            "Addressing": {
                "MAC": "Permanent physical address.",
                "IPv4": "32-bit address.",
                "IPv6": "128-bit address."
            }
        },
        "glossary": {
            "Router": "Directs data packets.",
            "Protocol": "Communication rules."
        },
        "keywords": ["LAN", "WAN", "Router", "Switch", "TCP/IP", "IP Address"]
    },

    "Security and Privacy": {
        "summary": "Techniques to protect data, systems, and users from digital threats.",
        "detailed_notes": {
            "Threats": {
                "Malware": ["Virus", "Worm", "Trojan", "Ransomware", "Spyware"],
                "Social Engineering": ["Phishing", "Pharming", "Shoulder Surfing"]
            },
            "Protection Methods": {
                "Encryption": "Scrambles data into unreadable form.",
                "Firewall": "Filters network traffic.",
                "Authentication": ["Passwords", "Biometrics", "MFA"]
            },
            "Data Protection": {
                "PDPA": "Singapore Personal Data Protection Act."
            }
        },
        "glossary": {
            "Encryption": "Data scrambling process.",
            "Firewall": "Network security barrier."
        },
        "keywords": ["Malware", "Encryption", "Firewall", "MFA", "Phishing", "PDPA"]
    },
    "Intellectual Property": {
        "summary": "Legal protection of digital content and creative works.",
        "detailed_notes": {
            "Copyright": "Protects original digital work.",
            "Licenses": ["Proprietary", "FOSS", "Freeware", "Shareware"],
            "Software Piracy": "Illegal copying and distribution.",
            "Plagiarism": "Presenting others' work as your own."
        },
        "glossary": {
            "FOSS": "Free and Open Source Software.",
            "Plagiarism": "Ethical violation."
        },
        "keywords": ["Copyright", "FOSS", "Piracy", "License"]
    },

    # 11
    "Ethics and Social Impact": {
        "summary": "Impact of computing on individuals, society, and the environment.",
        "detailed_notes": {
            "Ethical Issues": ["Privacy", "Surveillance", "Digital Divide"],
            "Social Impact": ["Remote Work", "E-learning", "Social Media"],
            "Environmental Impact": ["E-waste", "Energy Consumption", "Green Computing"]
        },
        "glossary": {
            "Digital Divide": "Gap in access to technology.",
            "E-waste": "Discarded electronic devices."
        },
        "keywords": ["Ethics", "Social Impact", "Digital Divide", "E-waste"]
    },

    # 12
    "Data Management": {
        "summary": "Organising, storing, retrieving, and maintaining data efficiently.",
        "detailed_notes": {
            "Databases": {
                "Tables": "Rows and columns.",
                "Primary Key": "Unique identifier.",
                "Foreign Key": "Links tables."
            },
            "SQL": ["SELECT", "INSERT", "UPDATE", "DELETE"],
            "Data Integrity": ["Validation", "Referential Integrity", "Constraints"]
        },
        "glossary": {
            "Primary Key": "Unique table identifier.",
            "Foreign Key": "Links database tables."
        },
        "keywords": ["Database", "SQL", "Primary Key", "Foreign Key"]
    },

    # 13
    "Internet Technologies": {
        "summary": "Technologies enabling communication and data exchange over the Internet.",
        "detailed_notes": {
            "Web Technologies": ["HTML", "CSS", "JavaScript"],
            "Protocols": ["HTTP", "HTTPS", "FTP", "SMTP"],
            "Cloud Computing": ["IaaS", "PaaS", "SaaS"]
        },
        "glossary": {
            "HTTP": "HyperText Transfer Protocol.",
            "Cloud Computing": "On-demand computing services."
        },
        "keywords": ["HTML", "CSS", "HTTP", "Cloud Computing"]
    },

    "Emerging Technologies": {
        "summary": "Advanced computing innovations shaping future systems and applications.",
        "detailed_notes": {
            "Artificial Intelligence": {
                "Definition": "Systems that simulate human intelligence.",
                "Applications": ["Chatbots", "Image Recognition", "Speech Processing"]
            },
            "Machine Learning": {
                "Definition": "AI technique that learns patterns from data.",
                "Types": ["Supervised", "Unsupervised", "Reinforcement"]
            },
            "Blockchain": {
                "Definition": "Decentralized immutable digital ledger.",
                "Features": ["Distributed", "Secure", "Transparent"]
            },
            "Quantum Computing": {
                "Qubit": "Quantum bit using superposition.",
                "Entanglement": "Linked quantum states.",
                "Speed": "Solves certain problems exponentially faster."
            },
            "VR & AR": {
                "VR": "Fully immersive digital environments.",
                "AR": "Overlay of digital objects on real world."
            }
        },
        "glossary": {
            "Qubit": "Quantum data unit.",
            "Superposition": "Multiple states simultaneously.",
            "Entanglement": "Linked quantum states."
        },
        "keywords": ["AI", "Machine Learning", "Blockchain", "Quantum", "VR", "AR"]
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
    if isinstance(data, dict):
        for key, value in data.items():
            clean_key = key.replace("_", " ").title()

            if level == 0:
                st.markdown("---")
                st.markdown(f"### 📌 {clean_key}")
            elif level == 1:
                st.markdown(f"#### 🔹 {clean_key}")
            else:
                st.markdown(f"**▪ {clean_key}:**")

            display_nested_notes(value, level + 1)

    elif isinstance(data, list):
        # Horizontal layout for short lists
        if len(data) <= 6 and all(isinstance(i, str) for i in data):
            st.markdown(" • ".join(data))
        else:
            for item in data:
                st.markdown(f"- {item}")

    else:
        st.markdown(f"{data}")
# --- MAIN INTERFACE ---
mode = st.session_state.current_mode

if mode == "Review":
    st.markdown(f"# 📘 {topic}")
    st.caption("GCE O-Level Computing • Structured Study Notes")
    st.success(f"📖 **Chapter Summary:** {STATIONERY_DATA[topic]['summary']}")
    
    # Mastery Progress
    score = st.session_state.quiz_scores.get(topic, 0)
    st.write(f"**Topic Mastery:** {score}%")
    st.progress(score / 100)
    
    tab_notes, tab_glossary, tab_resources = st.tabs([
    "📝 Learn",
    "📚 Key Terms",
    "📂 Resources"
    ])

    with tab_notes:
        display_nested_notes(STATIONERY_DATA[topic].get("detailed_notes", {}))

    with tab_glossary:
        st.subheader("📚 Interactive Glossary")
        glossary = STATIONERY_DATA[topic].get("glossary", {})
    if glossary:
        for term, definition in glossary.items():
            with st.expander(f"🔹 {term}"):
                st.write(definition)
    else:
        st.warning("No glossary available.")

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
    st.title("🤖 AI Computing Tutor")

    # --- Get filtered textbook context ---
    tb_content = get_filtered_context(
        st.session_state.selected_topic,
        raw_data
    )

    system_message_content = f"""
You are a robotic, highly precise GCE Computing assistant.

PRIMARY KNOWLEDGE SOURCE:
{tb_content}

STRUCTURED NOTES DATABASE:
{json.dumps(STATIONERY_DATA[st.session_state.selected_topic], indent=2)}

RULES:
1. Always prioritise the textbook context.
2. Use the structured notes if textbook context is insufficient.
3. Maintain a technical, neutral tone.
4. Keep answers concise and accurate.
5. Use bullet points for processes and lists.
6. Only answer computing-related questions.
"""

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": system_message_content}
        ]

    # --- Chat history display ---
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # --- User input ---
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
