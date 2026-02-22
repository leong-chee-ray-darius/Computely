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
        "summary": "Study of how computers are designed, built, organised, and how their components work together to process data.",
        "detailed_notes": {

            "Introduction": {
                "Computer System": "A device that receives and processes data according to set instructions to produce processed data as a result.",
                "Computer Architecture": "Describes how a computer is designed, built, organized, and how its various parts are connected to function.",
                "Historical Context": "Early mechanical computers used cranks, gears, pulleys, and levers to perform computations without electricity."
            },

            "Units of Data": {
                "Digital System": "Computers perform calculations using binary data.",
                "Bit": "Smallest unit of data (0 or 1).",
                "Byte": "8 bits.",
                "Storage Measurement": {
                    "SI (Power of 1000)": ["kB", "MB", "GB", "TB", "PB"],
                    "Binary (Power of 1024)": ["KiB", "MiB", "GiB", "TiB", "PiB"]
                }
            },

            "Key Components": {

                "CPU": {
                    "Function": "Processes data and executes instructions.",
                    "Speed Units": ["MHz", "GHz"],
                    "Multi-core": "Dual-core and quad-core processors can execute multiple instructions simultaneously.",
                    "Specialized Units": "GPU handles graphics and AI tasks more efficiently than CPU."
                },

                "Main Memory": {
                    "RAM": {
                        "Function": "Temporarily stores data and instructions for CPU use.",
                        "Volatile": True,
                        "Addressing": "Each byte has a unique address."
                    },
                    "ROM": {
                        "Type": "Non-volatile",
                        "Purpose": "Stores startup instructions."
                    }
                },

                "Secondary Storage": {
                    "Magnetic": "High capacity, low cost per GB, vulnerable to magnets and impact.",
                    "Optical": "Laser-based, portable, vulnerable to scratches.",
                    "Solid State": "Fastest and most durable, no moving parts, higher cost per GB."
                },

                "Buses": {
                    "Data Bus": "Bi-directional, transports actual data.",
                    "Address Bus": "Uni-directional, transports memory addresses.",
                    "Operation": "Both buses are used simultaneously when writing to memory."
                },

                "Interfaces": {
                    "Input": "Data received for processing (e.g., keyboard, camera).",
                    "Output": "Processed results (e.g., monitor, printer).",
                    "USB": "External device connection (480 Mbit/s to 80 Gbit/s).",
                    "HDMI": "High-definition audio/video output.",
                    "PCIe": "Internal motherboard expansion interface using lanes (x1 to x16)."
                }
            }
        },

        "keywords": [
            "Computer System", "Bit", "Byte", "CPU", "RAM", "ROM",
            "Secondary Storage", "Data Bus", "Address Bus", "USB", "HDMI", "PCIe"
        ]
    },

    "Data Representation": {
        "summary": "Representation of all information using binary digits (bits).",
        "detailed_notes": {

            "Introduction": {
                "Definition": "All information is represented using bits (0 and 1).",
                "Reason": "Computer memory consists of electronic switches that can only be ON (1) or OFF (0)."
            },

            "Number Systems": {

                "Denary": {
                    "Base": 10,
                    "Digits": "0–9",
                    "Place Values": "10^N",
                    "Leading Zeros": "Do not change value but maintain consistent digit length."
                },

                "Binary": {
                    "Base": 2,
                    "Digits": "0 and 1",
                    "Place Values": "2^N",
                    "Notation": ["1101₂", "0b1101"],
                    "Conversions": {
                        "Binary to Denary": "Multiply each digit by its place value and sum.",
                        "Denary to Binary (Division)": "Divide repeatedly by 2 and read remainders bottom to top.",
                        "Denary to Binary (Place Values)": "Select largest place value ≤ number and subtract repeatedly."
                    },
                    "Largest Number": "2^N - 1"
                },

                "Hexadecimal": {
                    "Base": 16,
                    "Digits": "0–9 and A–F",
                    "Place Values": "16^N",
                    "Notation": ["subscript 16", "0x prefix"],
                    "Advantage": "More compact than binary.",
                    "Conversions": {
                        "Hex to Binary": "Each hex digit maps to 4 binary bits.",
                        "Binary to Hex": "Split binary into groups of 4 from right."
                    }
                }
            },

            "Negative Numbers": {
                "System": "Two's Complement",
                "Sign Bit": "MSB (0 = positive, 1 = negative)",
                "Range": "-2^(N-1) to 2^(N-1) - 1",
                "Steps": [
                    "Convert to binary",
                    "Pad to fixed length",
                    "Invert bits",
                    "Add 1"
                ],
                "Overflow": "Occurs when result exceeds bit-length limits causing wrap-around."
            },

            "Text Representation": {
                "Character Encoding": "Maps characters to numeric codes.",
                "ASCII": {
                    "Original": "7 bits, 128 characters",
                    "Extended": "8 bits, 256 characters",
                    "Control Characters": "Codes 0–31 for non-printing functions"
                },
                "Unicode": "Uses 8–32 bits and supports over a million characters."
            }
        },

        "keywords": [
            "Binary", "Denary", "Hexadecimal", "Two's Complement",
            "ASCII", "Unicode", "Overflow"
        ]
    },
    "Boolean Logic and Logic Gates": {
    "summary": "Boolean logic is used by computers to make decisions and perform operations using binary values.",
    "detailed_notes": {
        "Boolean Logic Basics": {
            "Boolean Values": ["True", "False"],
            "Representations": ["1 / 0", "On / Off", "High / Low", "Yes / No"],
            "Importance": "Processors use Boolean logic since all data is stored as bits."
        },
        "Truth Tables": {
            "Definition": "A table showing the output for every possible input combination.",
            "Number of Rows": "2^n where n is the number of inputs.",
            "Input Order": "Binary counting order (e.g., 000 to 111 for 3 inputs)."
        },
        "Logic Gates": {
            "AND": {
                "Expression": "Q = A · B",
                "Output Rule": "Output is 1 only when both inputs are 1."
            },
            "OR": {
                "Expression": "Q = A + B",
                "Output Rule": "Output is 1 when at least one input is 1."
            },
            "NOT": {
                "Expression": "Q = ¬A",
                "Output Rule": "Inverts the input."
            },
            "NAND": {
                "Expression": "Q = ¬(A · B)",
                "Output Rule": "Output is 0 only when both inputs are 1."
            },
            "NOR": {
                "Expression": "Q = ¬(A + B)",
                "Output Rule": "Output is 0 when at least one input is 1."
            },
            "XOR": {
                "Expression": "Q = A ⊕ B",
                "Output Rule": "Output is 1 when exactly one input is 1."
            }
        },
        "Logic Circuits": {
            "Definition": "Logic circuits are created by connecting multiple logic gates.",
            "Order of Operations": ["Parentheses", "NOT", "AND", "OR"],
            "Sum of Products": "Create AND terms for rows where output is 1, then OR them together."
        },
        "Boolean Laws": {
            "Double Negation": "¬(¬A) = A",
            "De Morgan": ["¬(A · B) = ¬A + ¬B", "¬(A + B) = ¬A · ¬B"],
            "Commutative": ["A · B = B · A"],
            "Distributive": ["A · (B + C) = (A · B) + (A · C)"],
            "Absorption": ["A · (A + B) = A", "A + (A · B) = A"]
        },
        "Applications": [
            {
                "Example": "Motion-sensing lights",
                "Expression": "Q = Dark · Motion",
                "Description": "Light turns on only if it is dark AND motion is detected."
            },
            {
                "Example": "Two-way switch",
                "Expression": "Q = A · B + ¬A · ¬B",
                "Description": "Light turns on when both switches are in the same state."
            }
        ]
    },
    "glossary": {
        "Truth Table": "Table showing outputs for all input combinations.",
        "Logic Gate": "Electronic circuit performing logical operations.",
        "Boolean Logic": "Logic using binary values to make decisions."
    },
    "keywords": ["Boolean Logic", "Truth Table", "AND", "OR", "NOT", "NAND", "NOR", "XOR"]
},
    "Algorithms and Programming": {
        "summary": "Algorithms and programming involve designing step-by-step solutions and implementing them in computer programs.",
        "detailed_notes": {
            "Algorithms": {
                "Definition": "Step-by-step instructions to solve a problem.",
                "Programs": "Algorithms written as source code.",
                "Machine Code": "Source code must be translated into machine code for execution."
            },
            "Problem Definition": {
                "Inputs": "All required data affecting output, with defined type and range.",
                "Outputs": "Results produced by the program."
            },
            "Variables and Literals": {
                "Literals": "Fixed values written directly in code.",
                "Variables": "Named identifiers storing changeable values.",
                "Identifier Rules": [
                    "Letters, digits (not first), underscores",
                    "Case-sensitive",
                    "Cannot use reserved keywords"
                ],
                "Initialization": "Assigning a value for the first time.",
                "Deletion": "Removing variable using del keyword.",
                "None": "Represents missing value."
            },
            "Functions and Methods": {
                "Functions": "Reusable blocks of instructions.",
                "Arguments": "Values passed into functions.",
                "Return Values": "Results returned by functions.",
                "Methods": "Functions linked to objects using dot notation."
            },
            "Data Types": {
                "Boolean": ["True", "False"],
                "Integer": "Whole numbers.",
                "Float": "Decimal numbers.",
                "String": "Text.",
                "List": "Ordered mutable sequence.",
                "Dictionary": "Key-value pairs."
            },
            "Mathematical Operations": {
                "Operators": ["+", "-", "*", "/", "//", "%", "**"],
                "Augmented Assignment": ["+=", "-=", "*=", "/="],
                "Type Casting": "Converting data types (e.g., int(), float())."
            },
            "Modules": {
                "Purpose": "Provide reusable functions and variables.",
                "Examples": ["math", "turtle"]
            },
            "Strings": {
                "Immutability": "Strings cannot be changed.",
                "Indexing": "Access characters using []",
                "Slicing": "Access subsets of text.",
                "Formatting": ["f-strings", "str.format()"]
            },
            "Lists and Dictionaries": {
                "Lists": {
                    "Features": ["Mutable", "Ordered"],
                    "Purpose": "Store multiple values."
                },
                "Dictionaries": {
                    "Keys": "Unique and immutable.",
                    "Purpose": "Store key-value pairs."
                }
            },
            "Control Flow": {
                "Sequence": "Instructions run in order.",
                "Selection": "if / elif / else branching.",
                "Iteration": ["while loop", "for-in loop"],
                "Loop Control": ["break", "continue"]
            },
            "User-Defined Functions": {
                "Definition": "Custom reusable functions.",
                "Scope": {
                    "Local": "Accessible only within function.",
                    "Global": "Accessible everywhere using global keyword."
                },
                "Advantages": ["Reduce repetition", "Modular design", "Easier testing"]
            },
            "File Handling": {
                "with Statement": "Ensures files are properly closed even when errors occur.",
                "Usage": "Used with open() for file management."
            }
        },
        "glossary": {
            "Algorithm": "Step-by-step solution.",
            "Variable": "Named memory storage.",
            "Function": "Reusable code block.",
            "Iteration": "Repeating a block of code."
        },
        "keywords": ["Algorithm", "Variables", "Functions", "Loops", "Control Flow", "Data Types"]
    },
    "Validation and Error Handling": {
        "summary": "Techniques used to ensure program correctness and handle invalid input safely.",
        "detailed_notes": {
            "Why Validation is Needed": {
                "Purpose": "Programs must validate inputs to prevent crashes or unexpected behavior.",
                "Example": "sum() fails with TypeError when adding integers and strings."
            },
            "Recovering from Invalid Input": {
                "Interactive Input": "Use while True loop to repeatedly prompt user until valid input is received.",
                "Non-Interactive Input": "Use sys.exit() to terminate program if file data is invalid."
            },
            "Common Validation Checks": {
                "Length Check": "Ensure number of characters/items is within required limits using len().",
                "Range Check": "Ensure numeric input falls within required limits using comparison operators.",
                "Presence Check": "Ensure required input is not empty (\"\" or None).",
                "Format Check": {
                    "Description": "Ensure input matches required pattern (e.g., HH:MM).",
                    "Tools": ["str.isdigit()", "index checking"]
                },
                "Existence Check": {
                    "Must Exist": "Username must already be in database.",
                    "Must Not Exist": "New username must be unique."
                },
                "Check Digit": {
                    "Description": "Extra digit added to detect manual entry errors.",
                    "Mechanism": "Mathematically related to other digits.",
                    "Example": "UPC-A uses weighted sum and modulus 10.",
                    "Limitation": "Cannot verify ownership of valid number."
                }
            }
        },
        "glossary": {
            "Validation": "Checking data reasonableness.",
            "Check Digit": "Digit used to detect data entry errors."
        },
        "keywords": [
            "Validation", "Length Check", "Range Check", "Presence Check",
            "Format Check", "Existence Check", "Check Digit"
        ]
    },

    "Bugs, Testing, and Debugging": {
        "summary": "Understanding program errors and methods used to detect and correct them.",
        "detailed_notes": {
            "Introduction": {
                "Bug": "A defect causing unintended program behavior.",
                "Debugging": "Process of identifying and removing defects.",
                "Historical Fact": "In 1947, a moth in the Mark II computer caused malfunction, popularizing the term 'bug'."
            },
            "Types of Errors": {
                "Syntax Error": {
                    "Description": "Violation of programming language rules.",
                    "Causes": [
                        "Spelling mistakes", "Incorrect indentation",
                        "Invalid variable names", "Missing punctuation"
                    ],
                    "Detection": "Usually caught before program runs."
                },
                "Logic Error": {
                    "Description": "Program runs but produces incorrect results.",
                    "Causes": [
                        "Incorrect sequencing",
                        "Wrong loop conditions",
                        "Incomplete formulas"
                    ],
                    "Detection": "Found through testing and mismatched expected output."
                },
                "Runtime Error": {
                    "Description": "Occurs while program is executing.",
                    "Causes": [
                        "Division by zero",
                        "Invalid list index",
                        "Improper input conversion"
                    ],
                    "Note": "Often caused by earlier logic errors."
                }
            },
            "Designing Test Cases": {
                "Definition": "Comparing actual output with expected output.",
                "Components": "Inputs and expected results.",
                "Conditions": [
                    "Normal conditions",
                    "Boundary conditions",
                    "Error conditions"
                ],
                "Security Note": "Improper error handling can cause security flaws."
            },
            "Debugging Techniques": [
                "Using print() statements to track variables.",
                "Trace tables for dry runs.",
                "Backtracking from observed error.",
                "Testing incrementally after small changes.",
                "Testing small parts by isolating components."
            ]
        },
        "glossary": {
            "Bug": "Program defect.",
            "Debugging": "Finding and fixing errors."
        },
        "keywords": [
            "Bug", "Debugging", "Syntax Error",
            "Logic Error", "Runtime Error", "Test Cases"
        ]
    },

    "Algorithm Design": {
        "summary": "Methods and thinking skills used to design efficient algorithms.",
        "detailed_notes": {
            "Introduction": {
                "Algorithm": "Step-by-step instructions to solve a problem.",
                "Solution": "An algorithm that always produces correct output for valid input.",
                "Computational Thinking": {
                    "Definition": "Formulating problems so solutions can be represented as algorithms.",
                    "Core Skills": ["Decomposition", "Generalisation"]
                }
            },
            "Decomposition": {
                "Definition": "Breaking complex problems into smaller, manageable parts.",
                "Approaches": {
                    "Modular": "Divide problem into self-contained components.",
                    "Incremental": "Solve a small version first and extend gradually using loops."
                }
            },
            "Generalisation": {
                "Definition": "Identifying common features to create a generic algorithm.",
                "Methods": [
                    "Identify patterns from specific solutions.",
                    "Extract reusable functions."
                ],
                "DRY Principle": "Don't Repeat Yourself – minimise repeated code.",
                "Manual Solving": "Solve small instances to identify generic steps."
            },
            "Common Problems and Solutions": {
                "Finding Min/Max": "Assume first item is min/max and update while iterating through list.",
                "Searching": "Linear (sequential) search; return None if not found.",
                "Extraction": "Append items meeting criteria into new list."
            }
        },
        "glossary": {
            "Algorithm": "Step-by-step problem solution.",
            "Decomposition": "Breaking problems into parts.",
            "Generalisation": "Creating reusable solutions."
        },
        "keywords": [
            "Algorithm", "Computational Thinking",
            "Decomposition", "Generalisation", "DRY"
        ]
    },
    "Program Development Models": {
        "summary": "Structured approaches used to design, build, test, and deploy software systems.",
        "detailed_notes": {
            "Waterfall Model": {
                "Description": "Each stage must be completed before moving to the next.",
                "Stages": {
                    "Gather Requirements": [
                        "Interview intended audience",
                        "Specify inputs and outputs",
                        "Write normal, boundary, and error test cases"
                    ],
                    "Design Solutions": [
                        "Manually solve simplified examples",
                        "Decompose into modular parts",
                        "Use flowcharts",
                        "Estimate time and manpower"
                    ],
                    "Write Code": [
                        "Translate algorithm into programming language",
                        "Aim for efficiency",
                        "Generative AI tools may assist but can produce incorrect or unethical code"
                    ],
                    "Test and Refine Code": {
                        "Tasks": [
                            "Run test cases",
                            "Fix syntax and logic errors",
                            "Address mismatched requirements"
                        ],
                        "User Acceptance Testing": {
                            "Alpha": "Testing at developer site",
                            "Beta": "Testing in user environment"
                        },
                        "Version Control": "Systems like Git track and manage changes"
                    },
                    "Deploy Code": [
                        "Install software",
                        "Train users",
                        "Gather feedback for improvements"
                    ]
                }
            },
            "Iterative Development": "Allows revisiting earlier stages as requirements change.",
            "Agile Development": {
                "Description": "Project broken into smaller increments with continuous feedback.",
                "User Stories": "Requirements written from user perspective.",
                "Sprints": "Short development cycles implementing subsets of requirements."
            },
            "Test Driven Development": {
                "Cycle": [
                    "Write test cases",
                    "Write minimum code to pass tests",
                    "Refactor and tidy code"
                ]
            }
        },
        "glossary": {
            "Sprint": "Short development cycle.",
            "Version Control": "Tracks and manages changes to code."
        },
        "keywords": ["Waterfall", "Iterative", "Agile", "TDD", "Sprint", "Version Control"]
    },

    "Spreadsheets": {
        "summary": "Spreadsheet tools used for calculation, modelling, and data analysis.",
        "detailed_notes": {
            "Basics": {
                "Cell": "Intersection of a column and row (e.g. A1).",
                "Range": "Block of cells (e.g. A1:C3).",
                "Formulas": "Start with = followed by expression.",
                "Automatic Recalculation": "Formulas update when referenced cells change."
            },
            "Cell References": {
                "Relative": "Changes when copied.",
                "Absolute": "Locked using $ (e.g. $A$1).",
                "Mixed": "Locks row or column only."
            },
            "Logical Operators and Functions": {
                "Comparison Operators": ["<", ">", "=", "<>"],
                "Logical Functions": ["AND()", "OR()", "NOT()", "IF()", "Nested IF"]
            },
            "Mathematical and Statistical Functions": {
                "Arithmetic Operators": ["+", "-", "*", "/", "^", "%"],
                "Rounding": ["ROUND()", "CEILING.MATH()", "FLOOR.MATH()"],
                "Calculations": ["SUM()", "SUMIF()", "AVERAGE()", "AVERAGEIF()", "MOD()", "SQRT()"],
                "Counting": ["COUNT()", "COUNTA()", "COUNTBLANK()", "COUNTIF()"],
                "Ranking": ["MAX()", "MIN()", "LARGE()", "SMALL()", "RANK.EQ()"]
            },
            "Text Functions": {
                "Concatenation": ["&", "CONCAT()"],
                "Extraction": ["LEFT()", "RIGHT()", "MID()"],
                "Information": ["LEN()", "FIND()", "SEARCH()"]
            },
            "Lookup Functions": {
                "Basic": ["VLOOKUP()", "HLOOKUP()"],
                "Advanced": ["MATCH()", "INDEX()", "INDEX + MATCH"],
                "Matching": {
                    "Exact": "Returns #N/A if not found",
                    "Approximate": "Requires sorted data"
                }
            },
            "Date and Analysis Tools": {
                "Date Functions": ["TODAY()", "NOW()", "DAYS()"],
                "Date Storage": "Dates stored as serial numbers from Jan 0, 1900",
                "Analysis Tools": [
                    "Goal Seek",
                    "Conditional Formatting"
                ]
            }
        },
        "glossary": {
            "Formula": "Expression used to calculate values.",
            "Absolute Reference": "Cell reference that does not change when copied."
        },
        "keywords": ["Cells", "Formulas", "Functions", "VLOOKUP", "INDEX", "Goal Seek"]
    },

    "Computer Networks": {
        "summary": "Systems of interconnected devices used to exchange data and share resources.",
        "detailed_notes": {
            "Introduction": {
                "Definition": "Two or more devices connected for exchanging data.",
                "Advantages": [
                    "Shared resources",
                    "Shared Internet",
                    "Centralized software",
                    "Efficient communication"
                ],
                "Disadvantages": [
                    "High cost",
                    "Security risks",
                    "Server dependency"
                ]
            },
            "Types of Networks": {
                "Connection Type": {
                    "Wired": "Uses cables; faster, reliable, secure.",
                    "Wireless": "Uses radio waves; mobile, scalable, prone to interference."
                },
                "Geographical Scope": {
                    "LAN": "Small area, high speed.",
                    "MAN": "City scale.",
                    "WAN": "Large distance, Internet example."
                },
                "Architecture": {
                    "Client Server": "Central server manages resources.",
                    "Peer to Peer": "All devices equal."
                },
                "Topologies": {
                    "Star": "All devices connect to central unit.",
                    "Mesh": "Interconnected devices."
                }
            },
            "Protocols and Error Detection": {
                "Protocols": "Rules governing communication.",
                "Packets": "Data broken into smaller units.",
                "Error Detection": [
                    "Parity bits",
                    "Checksums",
                    "Echo checks",
                    "Automatic repeat request"
                ]
            },
            "Home Networks and Internet": {
                "Hardware": {
                    "Modem": "Converts digital data for transmission.",
                    "NIC": "Connects device to network.",
                    "Switch": "Connects devices in LAN.",
                    "WAP": "Wireless access point.",
                    "Router": "Forwards packets between networks."
                },
                "Addressing": {
                    "MAC": "Permanent 48-bit address.",
                    "IP": {
                        "IPv4": "32-bit dotted format.",
                        "IPv6": "128-bit hexadecimal format."
                    }
                }
            }
        },
        "glossary": {
            "Protocol": "Communication rules.",
            "Router": "Forwards data between networks."
        },
        "keywords": ["LAN", "WAN", "Router", "IP Address", "Protocols", "Topology"]
    },
    "Security and Privacy": {
        "summary": "Protection of data and personal information from unauthorized access, misuse, and threats.",
        "detailed_notes": {
            "Security": {
                "Definition": "Protecting the confidentiality, integrity, and availability of all data.",
                "Confidentiality": "Protection from unauthorized access.",
                "Integrity": "Protection from unauthorized modification.",
                "Availability": "Ability to access data in a timely and uninterrupted manner."
            },
            "Privacy": {
                "Definition": "Protecting the confidentiality and control of personal data such as name, IP address, and birth date.",
                "Key Difference": "Security protects all data; privacy protects personal data specifically."
            },
            "Common Threats": {
                "Human Actions": {
                    "Physical": "Damage to storage media from impact or extreme temperatures.",
                    "Non-Physical": "Incorrect data entry or accidentally sending sensitive emails."
                },
                "Malware and Deception": {
                    "Adware": "Installs without user knowledge to display unwanted ads.",
                    "Spyware": "Secretly collects personal information.",
                    "Cookies": "Tracks browsing preferences and history.",
                    "Phishing": "Deceptive emails or websites to steal sensitive data.",
                    "Pharming": "Redirects users to fake websites even with correct URLs."
                }
            },
            "Defenses": {
                "Anti-malware": "Detects, stops, and removes malware.",
                "Firewalls": "Monitors and blocks unauthorized network traffic.",
                "Encryption": "Encodes data into unreadable format without a secret key.",
                "PDPA": "Singapore law regulating collection and usage of personal data."
            },
            "Good Practices": {
                "Strong Passwords": "Mix letters, numbers, and symbols.",
                "MFA": ["Something you know", "Something you own", "Something you are"],
                "Backups": "Regularly store copies of important files."
            }
        },
        "keywords": ["Security", "Privacy", "Encryption", "Firewall", "PDPA", "Malware", "Phishing"]
    },

    "Intellectual Property": {
        "summary": "Legal protection of digital and creative works.",
        "detailed_notes": {
            "Definition": "Creations of the mind with value such as software, designs, and songs.",
            "Copyright": "Legal right to control usage and distribution.",
            "Licensing": "Defines permitted and prohibited activities.",
            "Types of Software Licenses": {
                "Proprietary": "Commercial software with restricted usage.",
                "Freeware": "Free to use but not modify.",
                "Shareware": "Trial software requiring purchase after evaluation.",
                "FOSS": "Free and Open Source Software allowing modification and distribution.",
                "Public Domain": "No copyright restrictions.",
                "Creative Commons": "Flexible copyright licenses."
            },
            "Software Piracy": {
                "Definition": "Illegal copying or usage of software.",
                "Risks": ["Malware", "Viruses", "Identity Theft", "System Failure"]
            },
            "Plagiarism": "Passing off someone else's work as your own."
        },
        "keywords": ["Copyright", "Licenses", "Piracy", "Plagiarism", "FOSS"]
    },

    "Impact of Computing": {
        "summary": "Effects of computing on society and industries.",
        "detailed_notes": {
            "Communications": [
                "Digitalisation",
                "Real-time multimedia communication",
                "Global connectivity",
                "Mobile computing",
                "Privacy risks"
            ],
            "Education": [
                "Online collaboration",
                "Access to information",
                "Personalised learning",
                "Automated assessment",
                "Digital literacy"
            ],
            "Transportation": [
                "GPS navigation",
                "Autonomous vehicles",
                "Smart public transport"
            ],
            "Retail": [
                "Inventory management",
                "Cashless payments",
                "Self-checkout",
                "E-commerce"
            ],
            "Online Falsehoods": {
                "Algorithms": "Promote highly engaging content.",
                "Filter Bubbles": "Increase misinformation exposure.",
                "POFMA": {
                    "Purpose": "Combat fake news in Singapore.",
                    "Actions": ["Correction orders", "Content removal", "Legal penalties"]
                }
            }
        },
        "keywords": ["Digitalisation", "E-learning", "E-commerce", "POFMA", "Falsehoods"]
    },

    "Emerging Technologies": {
        "summary": "Advanced computing technologies shaping future systems.",
        "detailed_notes": {
            "Artificial Intelligence": {
                "Characteristics": ["Autonomy", "Adaptivity"],
                "Applications": [
                    "Face recognition",
                    "Voice recognition",
                    "Image classification",
                    "Spam filtering",
                    "Generative AI"
                ],
                "AI Levels": ["Narrow AI", "AGI"]
            },
            "Machine Learning": {
                "Definition": "Detects patterns and makes decisions using data.",
                "Concepts": [
                    "Model training",
                    "Inference",
                    "Probabilistic output"
                ]
            },
            "Nearest Neighbour": {
                "Purpose": "Simple classification algorithm.",
                "Process": [
                    "Measure features",
                    "Calculate distance",
                    "Find nearest point",
                    "Assign label"
                ]
            },
            "Risks of AI": [
                "Overfitting",
                "Bias",
                "Privacy issues",
                "Copyright ambiguity",
                "Misinformation",
                "Safety concerns"
            ],
            "Blockchain": {
                "Definition": "Decentralized immutable ledger.",
                "Properties": ["Transparency", "Security", "Immutability"],
                "Applications": ["Cryptocurrency", "Health records", "Voting"]
            },
            "VR and AR": {
                "VR": "Fully immersive environments.",
                "AR": "Digital overlays on real world."
            },
            "Quantum Computing": {
                "Qubit": "Exists as 0 and 1 simultaneously.",
                "Entanglement": "Linked quantum states.",
                "Impact": "Solves specific problems exponentially faster."
            }
        },
        "keywords": ["AI", "Machine Learning", "Blockchain", "Quantum Computing", "VR", "AR"]
    }
}

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
