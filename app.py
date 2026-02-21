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
        "summary": "Covers the CPU, RAM, secondary storage, and data/address buses.",
        "detailed_notes": [
            "**CPU Components:** Contains the ALU for calculations and the CU for instruction management.",
            "**Buses:** Address Bus (unidirectional) and Data Bus (bidirectional).",
            "**FDE Cycle:** Fetch-Decode-Execute cycle is the basic operation.",
            "**Memory:** RAM is volatile; ROM is non-volatile."
        ],
        "keywords": ["processor", "CPU", "RAM", "memory", "storage", "bus", "USB", "HDMI"],
        "quiz": [{"q": "What is the function of the address bus?", "a": "Transports memory locations from the processor to memory."}]
    },
    "Data Representation": {
        "summary": "Number systems (Binary, Denary, Hexadecimal) and text representation.",
        "detailed_notes": [
            "**Binary:** Base-2 system (0 and 1).",
            "**Hexadecimal:** Base-16 system used for MAC addresses.",
            "**Units:** 8 bits = 1 Byte; 1000 Bytes = 1 Kilobyte.",
            "**Characters:** ASCII and Unicode."
        ],
        "keywords": ["binary", "denary", "hexadecimal", "ASCII", "bit", "byte", "negative numbers"],
        "quiz": [{"q": "How many bits are in a byte?", "a": "8"}]
    },
    "Logic Gates": {
        "summary": "Boolean logic, truth tables, and logic circuits.",
        "detailed_notes": ["**AND:** 1 if both 1.", "**OR:** 1 if either 1.", "**NOT:** Inverts input.", "**XOR:** 1 if inputs differ."],
        "keywords": ["AND", "OR", "NOT", "XOR", "truth table", "Boolean", "logic circuit"]
    },
    "Programming": {
        "summary": "Python basics, data types, control flow, and functions.",
        "detailed_notes": ["**Types:** Int, Float, String, Boolean.", "**Loops:** For and While.", "**Logic:** If/Elif/Else."],
        "keywords": ["python", "variable", "list", "loop", "function"]
    },
    "Input Validation": {
        "summary": "Techniques to ensure data entered by users is sensible and secure.",
        "detailed_notes": ["**Checks:** Range, Type, Presence, and Format checks."],
        "keywords": ["validation", "range check", "type check"]
    },
    "Testing and Debugging": {
        "summary": "Identifying bugs, error types, and designing test cases.",
        "detailed_notes": ["**Errors:** Syntax (grammar), Logic (wrong result), Runtime (crash)."],
        "keywords": ["bug", "syntax error", "logic error", "debugging"]
    },
    "Algorithm Design": {
        "summary": "Decomposition, generalisation, and solving common problems.",
        "detailed_notes": ["**Decomposition:** Breaking problems down.", "**Abstraction:** Hiding complexity."],
        "keywords": ["decomposition", "abstraction", "algorithm", "pseudocode"]
    },
    "Software Engineering": {
        "summary": "Development stages and alternative methodologies.",
        "detailed_notes": ["**SDLC:** Analysis, Design, Implementation, Testing, Maintenance."],
        "keywords": ["SDLC", "waterfall", "agile", "testing"]
    },
    "Spreadsheets": {
        "summary": "Using cell references, formulas, and complex functions.",
        "detailed_notes": ["**References:** Absolute ($A$1) vs Relative (A1).", "**VLOOKUP:** Search table arrays."],
        "keywords": ["formula", "vlookup", "spreadsheet"]
    },
    "Networking": {
        "summary": "Types of networks, protocols, and the Internet.",
        "detailed_notes": ["**LAN/WAN:** Local vs Wide area.", "**Protocols:** TCP/IP, HTTP, DNS."],
        "keywords": ["LAN", "WAN", "protocol", "packet switching"]
    },
    "Security and Privacy": {
        "summary": "Threats (malware, phishing) and defenses (encryption, firewalls).",
        "detailed_notes": ["**Malware:** Viruses, Trojans.", "**Defense:** Encryption and Firewalls."],
        "keywords": ["malware", "phishing", "encryption", "firewall"]
    },
    "Intellectual Property": {
        "summary": "Copyright, software licenses, and piracy.",
        "detailed_notes": ["**Copyright:** Legal ownership.", "**Licenses:** Open Source vs Proprietary."],
        "keywords": ["copyright", "license", "piracy"]
    },
    "Impact of Computing": {
        "summary": "How computing affects industries and the spread of falsehoods.",
        "detailed_notes": ["**Automation:** Machines replacing labor.", "**Divide:** Digital access gap."],
        "keywords": ["automation", "falsehoods", "ethics"]
    },
    "Emerging Technologies": {
        "summary": "Artificial Intelligence, machine learning, and new innovations.",
        "detailed_notes": ["**AI:** Machine intelligence.", "**ML:** Learning from patterns."],
        "keywords": ["AI", "machine learning", "blockchain"]
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
# Connect selectbox to session state
topic_list = list(STATIONERY_DATA.keys())
try:
    topic_index = topic_list.index(st.session_state["selected_topic"])
except ValueError:
    topic_index = 0

topic = st.sidebar.selectbox("Select a Chapter:", topic_list, index=topic_index)
st.session_state["selected_topic"] = topic

mode = st.sidebar.radio("Activity:", ["Review", "AI bot", "Dynamic Quiz"])

# --- FILTERING LOGIC ---
def get_filtered_context(selected_topic):
    if not raw_data:
        return ""
    # Use both keywords and the topic name for better matching
    search_terms = STATIONERY_DATA[selected_topic].get("keywords", []) + [selected_topic]
    matches = []
    for page in raw_data:
        content = page.get('content', '')
        if any(term.lower() in content.lower() for term in search_terms):
            matches.append(content)
    return "\n\n".join(matches[:10])

tb_content = get_filtered_context(topic)

# --- REVIEW MODE (FIXED) ---
if mode == "Review":
    st.title("Computing Study Companion")
    st.header(f"📖 Study Notes: {topic}")
    
    # Use a container for the summary
    st.info(STATIONERY_DATA[topic]["summary"])
    
    # Split layout for notes and quick actions
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
    
    # Context section
    with st.expander("🔍 View AI-Extracted Context from Textbook"):
        if tb_content:
            st.markdown(tb_content)
        else:
            st.warning(f"No specific textbook context found for '{topic}' in your JSON file.")
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
