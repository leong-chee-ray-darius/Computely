from openai import OpenAI
import streamlit as st
import pandas as pd
import io
import time
import json
st.set_page_config(page_title="Computing Companion", layout="wide")
JSON_PATH = "/content/gdrive/My Drive/Computing/textbook_data.json"
def load_textbook_data():
    try:
        with open(JSON_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

raw_data = load_textbook_data()

STATIONERY_DATA = {
    "Computer Architecture": {
        "summary": "Covers the CPU, RAM, secondary storage, and data/address buses.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**CPU Components:** Contains the ALU (Arithmetic Logic Unit) for calculations and the CU (Control Unit) for instruction management.",
            "**Buses:** The **Address Bus** (unidirectional) holds the memory location; the **Data Bus** (bidirectional) carries the actual data.",
            "**FDE Cycle:** The Fetch-Decode-Execute cycle is the basic operational process of a computer.",
            "**Memory:** RAM is volatile (temporary) while ROM is non-volatile (permanent)."
        ],
        "keywords": ["processor", "CPU", "RAM", "memory", "storage", "bus", "USB", "HDMI"],
        "quiz": [{"q": "What is the function of the address bus?", "a": "Transports memory locations from the processor to memory."}]
    },
    "Data Representation": {
        "summary": "Number systems (Binary, Denary, Hexadecimal) and text representation.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Binary:** Base-2 system. Computers use it because transistors have two states (on/off).",
            "**Hexadecimal:** Base-16 system. Used for HTML color codes and MAC addresses because it's easier for humans to read than binary.",
            "**Units:** 8 bits = 1 Byte; 1000 Bytes = 1 Kilobyte (KB).",
            "**Character Sets:** ASCII (7/8-bit) and Unicode (16-bit) allow computers to represent text."
        ],
        "keywords": ["binary", "denary", "hexadecimal", "ASCII", "bit", "byte", "negative numbers"],
        "quiz": [{"q": "How many bits are in a byte?", "a": "8"}]
    },
    "Logic Gates": {
        "summary": "Boolean logic, truth tables, and logic circuits.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**AND Gate:** Output is 1 only if both inputs are 1.",
            "**OR Gate:** Output is 1 if at least one input is 1.",
            "**NOT Gate:** Reverses the input (Inverter).",
            "**XOR Gate:** Output is 1 if inputs are different.",
            "**Truth Tables:** Used to track the output of a logic circuit for every possible input combination."
        ],
        "keywords": ["AND", "OR", "NOT", "XOR", "truth table", "Boolean", "logic circuit"],
        "quiz": [{"q": "Which gate outputs 1 only if both inputs are 1?", "a": "AND"}]
    },
    "Programming": {
        "summary": "Python basics, data types, control flow, and functions.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Variables:** Named locations in memory used to store data.",
            "**Data Types:** Integer (whole number), Float (decimal), String (text), Boolean (True/False).",
            "**Iteration:** Using 'for' loops (count-controlled) or 'while' loops (condition-controlled).",
            "**Selection:** 'if', 'elif', and 'else' statements to branch code execution."
        ],
        "keywords": ["python", "variable", "list", "dictionary", "loop", "function", "if statement"],
        "quiz": [{"q": "Which Python statement is used to handle files safely?", "a": "with statement"}]
    },
    "Input Validation": {
        "summary": "Techniques to ensure data entered by users is sensible and secure.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Range Check:** Ensures data is between two values (e.g., age 1-100).",
            "**Type Check:** Ensures the correct data type is entered (e.g., no letters in a phone number).",
            "**Presence Check:** Ensures a field has not been left blank.",
            "**Format Check:** Ensures data follows a pattern (e.g., Postcodes or Email addresses)."
        ],
        "keywords": ["validation", "invalid input", "check", "range check", "type check"],
        "quiz": [{"q": "Why is input validation needed?", "a": "To prevent program errors from invalid data."}]
    },
    "Testing and Debugging": {
        "summary": "Identifying bugs, error types, and designing test cases.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Syntax Error:** A mistake in the grammar of the code (e.g., missing a bracket).",
            "**Logic Error:** The code runs but does not do what was intended.",
            "**Runtime Error:** Occurs while the program is running (e.g., dividing by zero).",
            "**Test Data:** Normal (expected), Boundary (limits), and Erroneous (invalid) data."
        ],
        "keywords": ["bug", "syntax error", "logic error", "test case", "trace table", "debugging"],
        "quiz": [{"q": "What is a logic error?", "a": "The program runs but produces the wrong result."}]
    },
    "Algorithm Design": {
        "summary": "Decomposition, generalisation, and solving common problems.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Decomposition:** Breaking a large problem into smaller, manageable sub-problems.",
            "**Abstraction:** Removing unnecessary details to focus on important parts.",
            "**Algorithmic Thinking:** Creating a step-by-step set of instructions to solve a problem.",
            "**Tools:** Flowcharts (visual) and Pseudocode (text-based logic)."
        ],
        "keywords": ["decomposition", "generalisation", "algorithm", "flowchart", "pseudocode"],
        "quiz": [{"q": "What is decomposition?", "a": "Breaking a complex problem into smaller parts."}]
    },
    "Software Engineering": {
        "summary": "Development stages and alternative methodologies.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**SDLC:** Software Development Life Cycle (Analysis, Design, Implementation, Testing, Maintenance).",
            "**Waterfall:** Linear, sequential phases. Hard to change once started.",
            "**Iterative/Agile:** Developing in small parts and refining based on feedback.",
            "**Alpha Testing:** Internal testing by the developers.",
            "**Beta Testing:** Testing by a small group of real users before full release."
        ],
        "keywords": ["requirement gathering", "design", "development", "alpha testing", "beta testing"],
        "quiz": [{"q": "What is beta testing?", "a": "Testing done externally in the user's environment."}]
    },
    "Spreadsheets": {
        "summary": "Using cell references, formulas, and complex functions.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Relative Reference:** Changes when a formula is copied (e.g., A1).",
            "**Absolute Reference:** Stays fixed when copied (e.g., $A$1).",
            "**VLOOKUP:** Searches for a value in the first column of a table array.",
            "**IF Function:** Returns one value if a condition is true and another if false."
        ],
        "keywords": ["formula", "relative reference", "absolute reference", "VLOOKUP", "IF", "COUNTIF"],
        "quiz": [{"q": "What does an absolute reference look like?", "a": "e.g., $A$1"}]
    },
    "Networking": {
        "summary": "Types of networks, protocols, and the Internet.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**LAN vs WAN:** LAN covers a small area (home); WAN covers a large area (the Internet).",
            "**IP Address:** A unique string of numbers that identifies a device on a network.",
            "**Protocols:** HTTP (Web), SMTP (Email), FTP (Files), TCP/IP (Standard communication).",
            "**Packet Switching:** Data is broken into packets, sent via different routes, and reassembled."
        ],
        "keywords": ["LAN", "WAN", "protocol", "TCP/IP", "HTTP", "DNS", "packet switching"],
        "quiz": [{"q": "What is a protocol?", "a": "A set of rules for data communication."}]
    },
    "Security and Privacy": {
        "summary": "Threats (malware, phishing) and defenses (encryption, firewalls).",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Malware:** Viruses, worms, and trojans designed to damage or gain access.",
            "**Phishing:** Deceptive emails used to steal personal info (passwords/credit cards).",
            "**Encryption:** Scrambling data so it cannot be read without a key.",
            "**Firewall:** Monitors incoming/outgoing traffic to block unauthorized access."
        ],
        "keywords": ["privacy", "security", "malware", "phishing", "encryption", "firewall", "biometrics"],
        "quiz": [{"q": "What is phishing?", "a": "Attempting to acquire sensitive info by masquerading as a trustworthy entity."}]
    },
    "Intellectual Property": {
        "summary": "Copyright, software licenses, and piracy.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Copyright:** Legal right that protects original works (code, art, text).",
            "**Proprietary Software:** Closed source; you buy a license but don't own the code.",
            "**Open Source:** Source code is free to view, modify, and distribute.",
            "**Piracy:** Illegal copying or distribution of software."
        ],
        "keywords": ["copyright", "license", "piracy", "infringement", "open source", "proprietary"],
        "quiz": [{"q": "What is software piracy?", "a": "The unauthorized copying or distribution of software."}]
    },
    "Impact of Computing": {
        "summary": "How computing affects industries and the spread of falsehoods.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**Automation:** Replacing human labor with machines (leads to job displacement but higher efficiency).",
            "**Digital Divide:** The gap between those with access to technology and those without.",
            "**Falsehoods:** How 'echo chambers' and algorithms can spread fake news rapidly.",
            "**E-Waste:** The environmental impact of disposing of old hardware."
        ],
        "keywords": ["automation", "falsehoods", "ethics", "social media", "industry impact"],
        "quiz": [{"q": "How can falsehoods spread online?", "a": "Through social media algorithms and bot accounts."}]
    },
    "Emerging Technologies": {
        "summary": "Artificial Intelligence, machine learning, and new innovations.",
        "drive_link": "https://drive.google.com/file/d/1p4icGvOPN61lQhowHjzh1aZErT0fBx1j/view?usp=sharing",
        "detailed_notes": [
            "**AI:** Systems designed to perform tasks that usually require human intelligence.",
            "**Machine Learning:** A subset of AI where systems learn from data to make predictions.",
            "**Bias:** If training data is flawed, the AI output will be biased.",
            "**Cloud Computing:** Accessing servers and storage over the internet rather than locally."
        ],
        "keywords": ["AI", "machine learning", "training data", "bias", "cloud computing", "blockchain"],
        "quiz": [{"q": "What is training data?", "a": "Data used to 'teach' an AI model how to make predictions."}]
    }
}
# --- SEARCH LOGIC ---
st.sidebar.title("Search")
search_query = st.sidebar.text_input("Find a term (e.g., 'Protocol')")

if search_query:
    st.sidebar.subheader("Results:")
    found = False
    for t_name, t_data in STATIONERY_DATA.items():
        # Check if query is in Name, Summary, or Keywords
        in_notes = any(search_query.lower() in note.lower() for note in t_data.get("detailed_notes", []))
        if (search_query.lower() in t_name.lower() or 
            search_query.lower() in t_data["summary"].lower() or 
            in_notes):
            
            if st.sidebar.button(f"Go to {t_name}", key=f"search_{t_name}"):
                # This updates the selectbox by finding the index of the topic
                topic_list = list(STATIONERY_DATA.keys())
                st.session_state["selected_topic"] = t_name
            found = True
    if not found:
        st.sidebar.write("No matches found.")

st.title("Computing Study Companion")
topic = st.sidebar.selectbox("Select a Chapter:", list(STATIONERY_DATA.keys()))
mode = st.sidebar.radio("Activity:", ["Review", "AI bot", "Dynamic Quiz"])
def get_filtered_context(selected_topic):
    keywords = STATIONERY_DATA[selected_topic].get("keywords", [])
    matches = []
    for page in raw_data:
        if any(key.lower() in page['content'].lower() for key in keywords):
            matches.append(page['content'])
    return "\n\n".join(matches[:10])
tb_content = get_filtered_context(topic)

# --- MODES ---

if mode == "Review":
    st.header(f"📖 Study Notes: {topic}")
    st.info(STATIONERY_DATA[topic]["summary"])
    st.subheader("Key Concepts")
    for note in STATIONERY_DATA[topic].get("detailed_notes", ["No detailed notes available yet."]):
        st.write(f"- {note}")
    st.divider()
    st.subheader("Reference Material")
    col1, col2 = st.columns([1, 3])
    with col1:
        pdf_url = STATIONERY_DATA[topic].get("pdf_url", "#")
        st.link_button("📂 Open Textbook Page", pdf_url)
    with col2:
        st.caption("This will open the textbook PDF in a new tab at the relevant chapter.")
    with st.expander("View AI-Extracted Context from Textbook"):
        if tb_content:
            st.write(tb_content)
        else:
            st.warning("No specific context found in the uploaded JSON for this topic.")
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
elif mode == "Dynamic Quiz":
    st.header(f"⚡ AI-Generated Quiz: {topic}")
    
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
