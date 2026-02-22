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
        "glossary": {
            "Computer System": "A device that receives and processes data according to instructions to produce output.",
            "Computer Architecture": "The design, structure, organization, and interconnection of a computer system.",
            "Digital System": "A system that processes data using binary (0 and 1).",
            "Bit": "The smallest unit of data, represented as 0 or 1.",
            "Byte": "A group of 8 bits.",
            "Kilobyte (kB)": "1000 bytes.",
            "Megabyte (MB)": "1000 kilobytes.",
            "Gigabyte (GB)": "1000 megabytes.",
            "Terabyte (TB)": "1000 gigabytes.",
            "Petabyte (PB)": "1000 terabytes.",
            "Kibibyte (KiB)": "1024 bytes.",
            "Mebibyte (MiB)": "1024 kibibytes.",
            "Gibibyte (GiB)": "1024 mebibytes.",
            "Tebibyte (TiB)": "1024 gibibytes.",
            "Pebibyte (PiB)": "1024 tebibytes.",
            "CPU": "Central Processing Unit that processes data and executes instructions.",
            "Clock Speed": "The speed at which a processor executes instructions, measured in MHz or GHz.",
            "Megahertz (MHz)": "One million cycles per second.",
            "Gigahertz (GHz)": "One billion cycles per second.",
            "Multi-core Processor": "A CPU with multiple processing cores that can execute tasks simultaneously.",
            "GPU": "Graphics Processing Unit that handles graphics rendering and AI tasks efficiently.",
            "RAM": "Volatile memory that temporarily stores data and instructions currently in use.",
            "ROM": "Non-volatile memory that stores startup instructions.",
            "Volatile Memory": "Memory that loses its contents when power is switched off.",
            "Non-volatile Memory": "Memory that retains data even when power is switched off.",
            "Secondary Storage": "Long-term storage for data and programs.",
            "Magnetic Storage": "Storage using magnetic fields, high capacity, low cost, but sensitive to impact.",
            "Optical Storage": "Laser-based storage that is portable but vulnerable to scratches.",
            "Solid-State Storage": "Fast and durable storage with no moving parts.",
            "Data Bus": "Transfers actual data between components.",
            "Address Bus": "Transfers memory addresses.",
            "Input Device": "Hardware used to enter data into a computer.",
            "Output Device": "Hardware used to display or produce processed results.",
            "USB": "Universal Serial Bus used to connect external devices.",
            "HDMI": "High-Definition Multimedia Interface used to transmit audio and video signals.",
            "PCIe": "Peripheral Component Interconnect Express used for internal hardware expansion."
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
        "glossary": {
            "Data Representation": "The method of storing, processing, and transmitting information in computers using binary digits (0 and 1).",
            "Bit": "The smallest unit of data, represented as either 0 or 1.",
            "Byte": "A group of 8 bits.",
            "Binary": "A base-2 number system using only the digits 0 and 1.",
            "Denary": "A base-10 number system using digits 0 to 9, commonly used by humans.",
            "Hexadecimal": "A base-16 number system using digits 0–9 and letters A–F, used as a compact form of binary.",
            "Place Value": "The value assigned to a digit based on its position in a number system.",
            "Most Significant Bit (MSB)": "The leftmost bit in a binary number, often used as the sign bit in signed binary numbers.",
            "Least Significant Bit (LSB)": "The rightmost bit in a binary number.",
            "Binary to Denary Conversion": "A method of converting binary to denary by multiplying each bit by its place value and summing the results.",
            "Denary to Binary Conversion": "A method of converting denary to binary using repeated division by 2 or place value subtraction.",
            "Binary to Hexadecimal Conversion": "A method of converting binary to hexadecimal by grouping bits into sets of four.",
            "Hexadecimal to Binary Conversion": "A method of converting each hexadecimal digit into its 4-bit binary equivalent.",
            "Two's Complement": "A method of representing negative numbers in binary.",
            "Sign Bit": "The most significant bit that indicates whether a number is positive (0) or negative (1).",
            "Integer Overflow": "A condition where a calculation exceeds the maximum value that can be stored using a fixed number of bits.",
            "Character Encoding": "A system that maps characters to numeric values so they can be stored in binary.",
            "ASCII": "A character encoding standard using 7 or 8 bits to represent characters.",
            "Extended ASCII": "An 8-bit version of ASCII supporting 256 characters.",
            "Unicode": "A universal character encoding system supporting global languages using 8 to 32 bits per character.",
            "Leading Zeros": "Extra zeros added to the front of a binary number to maintain consistent length without changing its value.",
            "Fixed-Length Binary": "Binary numbers that use a fixed number of bits for storage and processing."
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
        "Boolean Logic": "A system of logic based on two values, True and False, used by computers to perform decision-making operations.",
        "Boolean Value": "A data value that can be either True or False.",
        "Truth Table": "A table showing the output of a logic operation for every possible combination of inputs.",
        "Logic Gate": "An electronic circuit that performs a Boolean operation on one or more inputs to produce a single output.",
        "AND Gate": "A logic gate that outputs 1 only when both inputs are 1.",
        "OR Gate": "A logic gate that outputs 1 when at least one input is 1.",
        "NOT Gate": "A logic gate that inverts its input, producing the opposite output.",
        "NAND Gate": "A logic gate that outputs 0 only when both inputs are 1.",
        "NOR Gate": "A logic gate that outputs 0 when at least one input is 1.",
        "XOR Gate": "A logic gate that outputs 1 when the two inputs are different.",
        "Boolean Expression": "A mathematical expression formed using Boolean variables and logic operators.",
        "Boolean Operator": "A symbol used to perform logical operations such as AND, OR, and NOT.",
        "Logic Circuit": "A system formed by combining multiple logic gates to perform complex logical operations.",
        "Input": "A value fed into a logic gate or circuit.",
        "Output": "The result produced by a logic gate or circuit after processing the inputs.",
        "Sum of Products": "A method of forming a Boolean expression by combining AND terms using OR operations.",
        "Order of Operations": "The sequence used to evaluate Boolean expressions: parentheses first, then NOT, followed by AND, then OR.",
        "De Morgan’s Theorem": "A rule used to simplify Boolean expressions: NOT(A AND B) = (NOT A) OR (NOT B), and NOT(A OR B) = (NOT A) AND (NOT B).",
        "Double Negation": "A Boolean rule stating that NOT(NOT A) equals A.",
        "Commutative Law": "A Boolean law stating that the order of variables does not change the result (A AND B = B AND A, A OR B = B OR A).",
        "Distributive Law": "A Boolean law allowing expressions to be expanded or factorised, such as A AND (B OR C) = (A AND B) OR (A AND C).",
        "Absorption Law": "A Boolean rule stating that A AND (A OR B) = A, and A OR (A AND B) = A.",
        "System Problem": "A real-world situation modelled using Boolean logic and logic gates to produce an automated decision or output."
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
            "Algorithm": "A step-by-step set of instructions used to solve a problem.",
            "Program": "An algorithm written in a programming language that a computer can execute.",
            "Source Code": "Human-readable program instructions written in a programming language.",
            "Machine Code": "Low-level binary instructions that can be directly executed by the CPU.",
            "Input": "Data provided to a program for processing.",
            "Output": "Results produced by a program after processing input.",
            "Literal": "A fixed value written directly in source code, such as numbers or text.",
            "Variable": "A named storage location used to store data that can change during program execution.",
            "Identifier": "The name given to a variable, function, or object.",
            "Initialization": "Assigning a value to a variable for the first time.",
            "Memory Address": "The physical location in memory where data is stored.",
            "None": "A special value representing no data or absence of a value.",
            "del": "A command used to delete a variable and free its memory.",
            "Function": "A reusable block of code that performs a specific task.",
            "Method": "A function that belongs to an object and is called using dot notation.",
            "Argument": "A value passed into a function.",
            "Return Value": "The output produced by a function.",
            "Operator": "A symbol that performs a mathematical or logical operation.",
            "Boolean (bool)": "A data type that stores True or False values.",
            "Integer (int)": "A whole number data type.",
            "Float": "A data type used to store decimal numbers.",
            "String (str)": "A sequence of characters representing text.",
            "List": "An ordered and mutable collection of items.",
            "Dictionary (dict)": "An unordered collection of key-value pairs.",
            "Arithmetic Operators": "Operators used for mathematical calculations such as +, -, *, /, //, %, and **.",
            "Augmented Assignment": "Operators that combine calculation and assignment such as +=, -=, *=, and /=",
            "Type Casting": "Converting data from one type to another, such as int() or float().",
            "Module": "A file containing reusable code, functions, and variables.",
            "String Indexing": "Accessing individual characters in a string using position numbers.",
            "String Slicing": "Extracting a portion of a string using index ranges.",
            "Negative Indexing": "Accessing characters from the end of a string using negative positions.",
            "Flowchart": "A diagram that visually represents an algorithm using standard symbols.",
            "Terminator Symbol": "Flowchart symbol representing the start or end of a program.",
            "Process Symbol": "Flowchart symbol representing an operation or calculation.",
            "Decision Symbol": "Flowchart symbol representing a condition with branching outcomes.",
            "Sequence": "Control structure where instructions execute in order.",
            "Selection": "Control structure that chooses between paths using if, elif, and else.",
            "Iteration": "Control structure that repeats a block of code using loops.",
            "While Loop": "A loop that repeats while a condition is true.",
            "For Loop": "A loop that iterates over a sequence of values.",
            "Break": "A statement that exits a loop immediately.",
            "Continue": "A statement that skips the current loop iteration and continues with the next one.",
            "User-Defined Function (UDF)": "A custom function created by the programmer.",
            "Local Scope": "Variables accessible only within a function.",
            "Global Scope": "Variables accessible throughout the program.",
            "with Statement": "A construct used to manage resources safely, especially file handling.",
            "File Handling": "The process of reading from and writing to files in a program."
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
            "Validation": "The process of checking that input data is sensible, reasonable, and within required limits before processing.",
            "Verification": "The process of checking that data entered matches the original source data.",
            "Invalid Input": "Data that does not meet required conditions such as format, range, or presence.",
            "Interactive Input": "Data entered directly by the user while the program is running.",
            "Non-interactive Input": "Data read from files or external sources rather than direct user input.",
            "while True Loop": "A loop that repeats indefinitely until a break condition is met, often used for repeated input validation.",
            "sys.exit()": "A function used to terminate a program immediately when invalid input is detected.",
            "Length Check": "Validation check that ensures the number of characters or items is within a specified limit.",
            "Range Check": "Validation check that ensures a numerical value lies within an acceptable minimum and maximum range.",
            "Presence Check": "Validation check that ensures required data is not left blank or empty.",
            "Format Check": "Validation check that ensures data follows a specific pattern or structure (e.g., HH:MM for time).",
            "Existence Check": "Validation check that ensures required data exists in a list, file, or database, or does not exist when uniqueness is required.",
            "Check Digit": "An additional digit added to a number that helps detect errors during manual data entry.",
            "Weighted Sum": "A calculation method where digits are multiplied by fixed weights and summed, often used in check digit systems.",
            "Modulus Operation": "A mathematical operation that returns the remainder after division, often used in check digit calculations.",
            "UPC-A": "A barcode system that uses check digits to detect manual data entry errors.",
            "TypeError": "A runtime error that occurs when an operation is applied to an inappropriate data type.",
            "Error Handling": "The process of managing and responding to program errors to prevent crashes and unexpected behaviour."
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
            "Bug": "A defect that causes a program to behave in an unintended way.",
            "Debugging": "The process of identifying, locating, and removing bugs from a program.",
            "Syntax Error": "An error caused by violating the rules of a programming language, such as incorrect indentation or missing punctuation.",
            "Logic Error": "An error where the program runs but produces incorrect output due to faulty logic.",
            "Run-time Error": "An error that occurs while a program is running, often caused by invalid operations such as division by zero.",
            "Testing": "The process of comparing actual program output with expected output to find errors.",
            "Test Case": "A set of input values and the expected output used to test whether a program works correctly.",
            "Normal Condition": "A test case using typical, valid input values.",
            "Boundary Condition": "A test case using extreme valid values at the limits of acceptable input.",
            "Error Condition": "A test case using invalid input to check if the program handles errors properly.",
            "Trace Table": "A table used to manually track variable values step-by-step during program execution.",
            "Print Debugging": "Using print() statements to display intermediate values for tracking program flow.",
            "Backtracking": "Tracing program execution backwards from an observed error to locate its cause.",
            "Incremental Testing": "Testing small changes in a program step-by-step to isolate bugs.",
            "Isolation Testing": "Testing small parts of a program separately to identify the source of errors."
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
            "Algorithm": "A step-by-step set of instructions used to solve a problem.",
            "Solution": "An algorithm that always produces correct output for valid input.",
            "Computational Thinking": "A problem-solving approach where solutions are expressed as algorithms.",
            "Decomposition": "Breaking a complex problem into smaller, more manageable parts.",
            "Generalisation": "Identifying common patterns to create a generic solution.",
            "Modular Approach": "Dividing a problem into independent components or modules.",
            "Incremental Approach": "Solving a small version of a problem first and gradually extending the solution.",
            "DRY Principle": "Don't Repeat Yourself – reducing duplicated code by using reusable solutions.",
            "Linear Search": "Searching through items one by one until the target item is found.",
            "Extraction": "Selecting and collecting data items that meet specific conditions.",
            "Minimum Value": "The smallest value in a dataset.",
            "Maximum Value": "The largest value in a dataset.",
            "Iteration": "Repeating a sequence of instructions using loops.",
            "Reusable Function": "A function designed to be used multiple times to avoid repeated code."
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
            "Program Development Model": "A structured process used to design, develop, test, and deploy software systems.",
            "Waterfall Model": "A linear development model where each stage must be completed before moving to the next.",
            "Requirements Gathering": "The process of collecting and defining what a program must do.",
            "System Design": "The stage where algorithms, flowcharts, and solutions are planned before coding.",
            "Implementation": "The process of writing and coding the program.",
            "Testing": "The process of running test cases to find and fix errors in a program.",
            "Deployment": "The process of installing and releasing the completed software to users.",
            "User Acceptance Testing (UAT)": "Testing performed by users to verify the system meets their requirements.",
            "Alpha Testing": "Testing conducted at the developer’s site.",
            "Beta Testing": "Testing conducted in the real user environment.",
            "Iterative Development": "A development approach that allows stages to be revisited and refined repeatedly.",
            "Agile Development": "A development approach that uses short cycles and continuous user feedback.",
            "User Stories": "Short descriptions of system features written from the user’s perspective.",
            "Sprint": "A short development cycle in agile development.",
            "Test-Driven Development (TDD)": "A development approach where test cases are written before writing program code.",
            "Version Control": "A system that tracks changes made to program code over time (e.g., Git).",
            "Refactoring": "Improving the structure of code without changing its functionality."
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
            "Spreadsheet": "An application used to organize, calculate, and analyze data using cells arranged in rows and columns.",
            "Cell": "The intersection of a row and column in a spreadsheet (e.g., A1).",
            "Range": "A group of adjacent cells in a spreadsheet.",
            "Formula": "An expression used to perform calculations in a spreadsheet, starting with '='.",
            "Relative Cell Reference": "A reference that changes automatically when copied to another cell.",
            "Absolute Cell Reference": "A fixed reference that does not change when copied, using the $ symbol.",
            "Mixed Cell Reference": "A reference where either the row or column is fixed.",
            "Function": "A predefined formula that performs specific calculations.",
            "Logical Function": "A function that performs logical comparisons, such as AND(), OR(), and IF().",
            "IF Function": "A function that performs different actions depending on whether a condition is true or false.",
            "Mathematical Function": "A function that performs numeric calculations such as SUM(), AVERAGE(), and ROUND().",
            "Statistical Function": "A function that analyzes data sets, such as COUNT(), MAX(), and MIN().",
            "Text Function": "A function that manipulates text, such as LEFT(), RIGHT(), and MID().",
            "Lookup Function": "A function that searches for data within a table, such as VLOOKUP() and HLOOKUP().",
            "MATCH Function": "A function that finds the position of a value in a range.",
            "INDEX Function": "A function that returns the value at a specific position in a range.",
            "Conditional Formatting": "A feature that automatically formats cells based on their values.",
            "What-If Analysis": "A technique used to test different values to see how they affect results.",
            "Goal Seek": "A tool that finds the input value needed to achieve a specific output."
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
            "Computer Network": "A system of two or more devices connected by a transmission medium to exchange data.",
            "Transmission Medium": "The physical or wireless path used to transfer data between devices.",
            "LAN": "Local Area Network that connects devices in a small area such as a home, school, or office.",
            "MAN": "Metropolitan Area Network that spans a city or large campus.",
            "WAN": "Wide Area Network that spans large geographical distances, such as the Internet.",
            "Wired Network": "A network where devices are connected using physical cables such as Ethernet or fibre.",
            "Wireless Network": "A network where devices connect using radio or electromagnetic waves, such as Wi-Fi.",
            "Client-Server Network": "A network architecture where a central server manages resources and services.",
            "Peer-to-Peer Network": "A network architecture where all devices have equal roles and share resources directly.",
            "Star Topology": "A network layout where all devices connect to a central unit.",
            "Mesh Topology": "A network layout where devices are interconnected, providing multiple data paths.",
            "Protocol": "A set of rules governing communication between network devices.",
            "TCP/IP": "Core communication protocol suite used on the Internet.",
            "Packet": "A small unit of data transmitted across a network.",
            "Parity Bit": "An extra bit added to data to detect single-bit transmission errors.",
            "Checksum": "A calculated value used to verify data integrity during transmission.",
            "Echo Check": "An error detection method where data is sent back to the sender for verification.",
            "Automatic Repeat Request (ARQ)": "A system that automatically resends data if transmission errors are detected.",
            "Modem": "A device that converts digital data for transmission over long-distance media.",
            "NIC": "Network Interface Controller that connects a device to a network.",
            "Switch": "A device that connects multiple devices within a LAN and forwards data using MAC addresses.",
            "WAP": "Wireless Access Point that allows wireless devices to connect to a network.",
            "Router": "A device that forwards data packets between different networks using IP addresses.",
            "MAC Address": "A permanent 48-bit physical address used to identify devices in a network.",
            "IP Address": "A logical address used to identify devices on a network.",
            "IPv4": "A 32-bit addressing system written in four denary numbers separated by dots.",
            "IPv6": "A 128-bit addressing system using hexadecimal numbers separated by colons."
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
        "glossary": {
            "Security": "The protection of data and systems to ensure confidentiality, integrity, and availability.",
            "Privacy": "The protection and control of personal data and how it is collected, used, and shared.",
            "Confidentiality": "Ensuring that data is accessed only by authorized individuals.",
            "Integrity": "Ensuring that data is accurate and not altered without authorization.",
            "Availability": "Ensuring that data and systems are accessible when needed.",
            "Adware": "Malicious software that installs unwanted advertisements without user consent.",
            "Spyware": "Malicious software that secretly collects and transmits user information.",
            "Cookies": "Small files stored by browsers to track user preferences and activity.",
            "Phishing": "A social engineering attack that tricks users into revealing sensitive information using fake emails or websites.",
            "Pharming": "An attack that redirects users from legitimate websites to fake websites even when the correct URL is entered.",
            "Anti-malware": "Software that detects, prevents, and removes malicious programs.",
            "Firewall": "A security system that monitors and controls incoming and outgoing network traffic.",
            "Encryption": "The process of converting data into unreadable form to prevent unauthorized access.",
            "PDPA": "Singapore Personal Data Protection Act that governs the collection, use, and storage of personal data.",
            "Strong Password": "A password containing a mix of letters, numbers, and symbols to reduce unauthorized access.",
            "Multi-Factor Authentication": "A security method requiring two or more verification factors to access a system.",
            "Backup": "A copy of important data stored separately to prevent loss.",
            "Social Engineering": "Techniques that manipulate human behaviour to gain unauthorized access to information."
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
        "glossary": {
            "Intellectual Property (IP)": "Creations of the human mind that have value and exist digitally, such as software, designs, text, images, and music.",
            "Originality": "The requirement that a work must be independently created and not copied from existing works.",
            "Fixation": "The requirement that a work must be recorded in a tangible medium, such as a digital file.",
            "Ownership": "The legal recognition of a human creator as the author of intellectual property.",
            "Copyright": "The legal right that gives creators control over how their work is used, copied, and distributed.",
            "License": "An official description of what users are allowed or not allowed to do with software or digital content.",
            "Proprietary Software": "Commercial software where the source code is kept secret and modification or redistribution is illegal.",
            "Freeware": "Proprietary software that can be used free of charge but cannot be modified or redistributed.",
            "Shareware": "Software distributed for free trial but requires payment after an evaluation period.",
            "FOSS": "Free and Open Source Software that allows users to copy, modify, study, and share both the software and its source code.",
            "Public Domain": "Software or content that is not protected by copyright and can be freely used, modified, and distributed.",
            "Creative Commons": "Licensing system that allows creators to specify how their work can be shared and reused.",
            "Software Piracy": "Illegal copying, distribution, or use of copyrighted software.",
            "Crack": "A tool used to bypass software licensing or security checks illegally.",
            "Copyright Infringement": "Using copyrighted material without permission from the copyright owner.",
            "Plagiarism": "Presenting another person's work or ideas as one’s own without acknowledgment.",
            "End User License Agreement (EULA)": "A legal agreement between the software provider and the user outlining permitted usage."
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
        "glossary": {
            "Digitalisation": "The conversion of analogue information into digital form for easier processing and transmission.",
            "Compression": "Reducing file size for faster data transmission.",
            "Globalisation": "The ability to communicate and collaborate across borders using computing technologies.",
            "Mobile Computing": "The use of portable devices such as smartphones and laptops for computing on the move.",
            "Collaboration Tools": "Online platforms that allow people to work together remotely.",
            "Adaptive Learning": "Learning systems that adjust content based on a learner’s ability and progress.",
            "Navigation Systems": "Digital systems that provide route guidance using GPS and real-time traffic data.",
            "Autonomous Vehicles": "Vehicles capable of operating with minimal or no human intervention using sensors and AI.",
            "Inventory Management": "Using computing systems to track goods and stock levels in real time.",
            "E-commerce": "The buying and selling of goods and services online.",
            "Misinformation": "False or misleading information spread regardless of intent.",
            "Deepfake": "AI-generated media that realistically imitates real people, often used for deception.",
            "Filter Bubble": "A state where users are shown content matching their beliefs, limiting exposure to opposing views.",
            "Algorithm": "A set of rules used by platforms to determine what content users see.",
            "Engagement Rate": "Measurement of user interaction such as likes, shares, and comments.",
            "POFMA": "Protection from Online Falsehoods and Manipulation Act, a Singapore law to counter harmful fake news.",
            "Correction Direction": "Legal instruction requiring false information to be corrected publicly.",
            "Online Manipulation": "The deliberate spreading of misleading information to influence opinions or behavior."
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
        "glossary": {
            "Artificial Intelligence (AI)": "Technology that enables computers to perform tasks that normally require human intelligence.",
            "Autonomy": "The ability of AI systems to operate independently without constant human input.",
            "Adaptivity": "The ability of AI systems to improve performance as they receive more data.",
            "Narrow AI": "AI designed to perform specific tasks.",
            "Artificial General Intelligence (AGI)": "Future AI capable of performing any intellectual task a human can.",
            "Machine Learning (ML)": "A branch of AI that enables systems to learn patterns from data without explicit programming.",
            "Model": "A trained mathematical representation used by ML systems to make predictions.",
            "Inference": "The process of applying a trained model to new data.",
            "Overfitting": "When a model performs well on training data but poorly on unseen data.",
            "Bias": "Systematic error in AI outcomes due to unbalanced or incomplete training data.",
            "Deepfake": "AI-generated fake images, videos, or audio that appear realistic.",
            "Blockchain": "A decentralized digital ledger where records cannot be altered once added.",
            "Hash": "A cryptographic value linking blocks together in a blockchain.",
            "Decentralization": "No central authority controls the system.",
            "Immutability": "Data cannot be changed once recorded.",
            "Virtual Reality (VR)": "A fully immersive computer-generated environment.",
            "Augmented Reality (AR)": "Technology that overlays digital objects onto the real world.",
            "Head-Mounted Device (HMD)": "Wearable display device used in VR and AR systems.",
            "Quantum Computing": "Computing based on quantum mechanics principles.",
            "Qubit": "Quantum bit that can exist as 0 and 1 simultaneously.",
            "Superposition": "The ability of a qubit to exist in multiple states at once.",
            "Entanglement": "Quantum phenomenon where linked qubits influence each other instantly.",
            "Cryptography Threat": "Risk posed by quantum computing to existing encryption methods."
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
            df = pd.DataFrame(glossary.items(), columns=["Term", "Definition"])
            st.dataframe(df, use_container_width=True, hide_index=True)
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
