STATIONERY_DATA = {
    "Computer Architecture": {
    "summary": "Study of how computers are designed, built, organised, and how their components work together to process data.",
    "detailed_notes": {
        "Introduction": {
            "Computer System": "A device that receives and processes data according to a set of instructions to produce processed data as output.",
            "Computer Architecture": "Describes how a computer is designed, built, organised, and how its various parts are connected to function.",
            "Historical Context": "Early mechanical computers used cranks, gears, pulleys, and levers to perform computations without electricity."
        },
        "Units of Data": {
            "Digital System": "Computers perform calculations using binary data represented by bits.",
            "Bit": "The smallest unit of data, represented as either 0 or 1.",
            "Byte": "A unit of data made up of 8 bits.",
            "Storage Measurement": {
                "SI (Power of 1000)": ["kB", "MB", "GB", "TB", "PB"],
                "Binary (Power of 1024)": ["KiB", "MiB", "GiB", "TiB", "PiB"]
            }
        },
        "Key Components": {
            "CPU": {
                "Function": "Processes data and executes instructions.",
                "Speed Units": ["MHz", "GHz"],
                "Multi-core": "Dual-core and quad-core processors contain multiple processing cores that can execute multiple instructions simultaneously.",
                "Specialized Units": "GPU handles graphics processing and certain parallel computations more efficiently than the CPU."
            },
            "Main Memory": {
                "RAM": {
                    "Function": "Temporarily stores data and instructions for CPU use.",
                    "Volatile": True,
                    "Addressing": "Each byte stored in memory has a unique address."
                },
                "ROM": {
                    "Type": "Non-volatile",
                    "Purpose": "Stores startup instructions required to boot the computer."
                }
            },
            "Secondary Storage": {
                "Magnetic": "High capacity, low cost per GB, but vulnerable to magnetic fields and physical impact.",
                "Optical": "Laser-based storage, portable, but vulnerable to scratches.",
                "Solid State": "Fast storage with no moving parts, more durable but typically higher cost per GB."
            },
            "Buses": {
                "Data Bus": "Bi-directional bus that transports actual data between components.",
                "Address Bus": "Uni-directional bus that transports memory addresses.",
                "Operation": "Both data bus and address bus are used together when reading from or writing to memory."
            },
            "Interfaces": {
                "Input": "Data received for processing (e.g., keyboard, camera).",
                "Output": "Processed results produced by the computer (e.g., monitor, printer).",
                "USB": "Interface used to connect external devices for data transfer and power.",
                "HDMI": "Interface used to transmit high-definition audio and video signals.",
                "PCIe": "Internal motherboard expansion interface using lanes (e.g., x1 to x16)."
            }
        }
    },
    "glossary": {
        "Computer System": "A device that receives and processes data according to instructions to produce output.",
        "Computer Architecture": "The design, structure, organisation, and interconnection of a computer system.",
        "Digital System": "A system that processes data using binary digits (0 and 1).",
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
        "GPU": "Graphics Processing Unit that handles graphics rendering and certain parallel computations.",
        "RAM": "Volatile memory that temporarily stores data and instructions currently in use.",
        "ROM": "Non-volatile memory that stores startup instructions.",
        "Volatile Memory": "Memory that loses its contents when power is switched off.",
        "Non-volatile Memory": "Memory that retains data even when power is switched off.",
        "Secondary Storage": "Long-term storage for data and programs.",
        "Magnetic Storage": "Storage using magnetic material; high capacity and low cost but sensitive to magnetic fields and impact.",
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
    "summary": "Methods used to represent different types of data in binary form so that they can be processed by a computer system.",
    "detailed_notes": {
        "Number Systems": {
            "Binary": "Base 2 number system using digits 0 and 1.",
            "Denary": "Base 10 number system using digits 0–9.",
            "Hexadecimal": "Base 16 number system using digits 0–9 and letters A–F.",
            "Conversion": {
                "Binary to Denary": "Multiply each bit by 2 raised to its positional value and sum the results.",
                "Denary to Binary": "Repeatedly divide the denary number by 2 and record remainders.",
                "Binary to Hexadecimal": "Group binary digits into sets of four bits and convert each group.",
                "Hexadecimal to Binary": "Convert each hexadecimal digit into its 4-bit binary equivalent."
            }
        },
        "Binary Arithmetic": {
            "Binary Addition": "Addition using binary rules (0+0=0, 0+1=1, 1+1=10).",
            "Overflow": "Occurs when a calculation produces a result outside the range that can be represented with the available number of bits."
        },
        "Data Storage": {
            "Unsigned Integers": "Binary numbers representing only non-negative whole numbers.",
            "Signed Integers": "Binary numbers that represent both positive and negative whole numbers.",
            "Two's Complement": "Method used to represent negative integers in binary by inverting bits and adding 1.",
            "Range": "Determined by the number of bits available."
        },
        "Character Representation": {
            "ASCII": "American Standard Code for Information Interchange; uses 7 bits to represent characters.",
            "Extended ASCII": "Uses 8 bits to represent additional characters.",
            "Unicode": "Character encoding standard capable of representing a wide range of characters from multiple languages."
        },
        "Images": {
            "Pixel": "The smallest unit of a digital image.",
            "Resolution": "The number of pixels in an image (width × height).",
            "Colour Depth": "Number of bits used to represent the colour of a single pixel.",
            "Image File Size": "Resolution × Colour Depth."
        },
        "Sound": {
            "Sampling": "Taking measurements of sound at regular time intervals.",
            "Sampling Rate": "Number of samples taken per second, measured in Hz.",
            "Bit Depth": "Number of bits used to store each sample.",
            "Sound File Size": "Sampling Rate × Bit Depth × Duration."
        },
        "Compression": {
            "Lossless": "Compression that reduces file size without losing any data.",
            "Lossy": "Compression that reduces file size by permanently removing some data."
        }
    },
    "glossary": {
        "Binary": "Base 2 number system.",
        "Denary": "Base 10 number system.",
        "Hexadecimal": "Base 16 number system.",
        "Overflow": "When a calculation exceeds the available number of bits.",
        "Unsigned Integer": "A whole number represented in binary without a sign.",
        "Signed Integer": "A whole number represented in binary with a sign.",
        "Two's Complement": "Binary method used to represent negative numbers.",
        "ASCII": "7-bit character encoding standard.",
        "Unicode": "Character encoding standard supporting many languages.",
        "Pixel": "Smallest unit of a digital image.",
        "Resolution": "Total number of pixels in an image.",
        "Colour Depth": "Number of bits per pixel.",
        "Sampling Rate": "Number of sound samples taken per second.",
        "Bit Depth": "Number of bits used per sound sample.",
        "Lossless Compression": "Compression without data loss.",
        "Lossy Compression": "Compression with some data loss."
    },
    "keywords": [
        "Binary", "Denary", "Hexadecimal", "Overflow",
        "Two's Complement", "ASCII", "Unicode",
        "Pixel", "Resolution", "Colour Depth",
        "Sampling Rate", "Bit Depth",
        "Lossless", "Lossy"
    ]
},
"Logic Gates": {
    "summary": "Boolean logic is used to represent and evaluate logical operations using binary values.",
    "detailed_notes": {
        "Boolean Logic": "A system of logic based on two possible values: 1 (True) and 0 (False).",
        "Logic Gates": {
            "AND Gate": "Outputs 1 only when both inputs are 1.",
            "OR Gate": "Outputs 1 when at least one input is 1.",
            "NOT Gate": "Outputs the inverse of the input.",
            "NAND Gate": "Outputs 0 only when both inputs are 1.",
            "NOR Gate": "Outputs 1 only when both inputs are 0.",
            "XOR Gate": "Outputs 1 when the inputs are different."
        },
        "Truth Table": "A table that shows all possible combinations of inputs and their corresponding outputs.",
        "Boolean Expressions": {
            "AND": "Represented using multiplication (·) or AND.",
            "OR": "Represented using addition (+) or OR.",
            "NOT": "Represented using a bar over the variable or NOT."
        },
        "Logic Circuits": "Complex logical operations can be constructed by combining multiple logic gates.",
        "Sum of Products": "A Boolean expression formed by creating AND terms for input combinations that produce an output of 1, then combining those terms using OR."
    },
    "glossary": {
        "Boolean Logic": "Logical system using binary values 1 and 0.",
        "Logic Gate": "An electronic circuit that performs a Boolean operation on one or more inputs to produce a single output.",
        "AND Gate": "Outputs 1 only if both inputs are 1.",
        "OR Gate": "Outputs 1 if at least one input is 1.",
        "NOT Gate": "Inverts the input.",
        "NAND Gate": "NOT-AND operation.",
        "NOR Gate": "NOT-OR operation.",
        "XOR Gate": "Exclusive OR; outputs 1 when inputs differ.",
        "Truth Table": "Table listing all possible input combinations and outputs.",
        "Boolean Expression": "An algebraic representation of a logical operation.",
        "Logic Circuit": "Combination of logic gates to perform complex operations.",
        "Sum of Products": "Standard form Boolean expression using AND terms combined by OR."
    },
    "keywords": [
        "Boolean Logic", "Logic Gate", "AND", "OR", "NOT",
        "NAND", "NOR", "XOR",
        "Truth Table", "Boolean Expression",
        "Logic Circuit", "Sum of Products"
    ]
},
"Programming": {
    "summary": "The process of designing algorithms and implementing them as computer programs to solve problems.",
    "detailed_notes": {

        "Problem Solving": {
            "Problem Definition": "Clearly identifying the problem and required output.",
            "Requirements Analysis": "Determining inputs, outputs, and constraints.",
            "Algorithm Design": "Developing a step-by-step solution to the problem.",
            "Pseudocode": "A structured description of an algorithm written in plain language.",
            "Flowchart": "A diagrammatic representation of an algorithm using standard symbols."
        },

        "Programming Concepts": {
            "Variable": "A named storage location used to store data values.",
            "Constant": "A value that does not change during program execution.",
            "Data Types": {
                "Integer": "Whole numbers.",
                "Float": "Numbers with decimal points.",
                "String": "A sequence of characters.",
                "Boolean": "A data type with two possible values: True or False.",
                "List": "An ordered collection of values.",
                "Dictionary": "A collection of key-value pairs."
            },
            "Assignment": "Storing a value in a variable using the assignment operator.",
            "Input": "Receiving data from the user or another source.",
            "Output": "Displaying or returning processed data."
        },

        "Control Structures": {
            "Sequence": "Statements executed one after another in order.",
            "Selection": {
                "If Statement": "Executes a block of code when a condition is true.",
                "If-Else Statement": "Chooses between two blocks based on a condition.",
                "Nested Selection": "A selection structure inside another selection structure."
            },
            "Iteration": {
                "For Loop": "Repeats a block of code a fixed number of times.",
                "While Loop": "Repeats a block of code while a condition remains true.",
                "Nested Loop": "A loop inside another loop."
            }
        },

        "Functions": {
            "Definition": "A reusable block of code that performs a specific task.",
            "Parameters": "Values passed into a function.",
            "Return Value": "The value sent back from a function to the caller.",
            "Scope": "The region of a program where a variable can be accessed."
        },

        "Error Handling": {
            "Syntax Error": "An error caused by violating the rules of the programming language.",
            "Runtime Error": "An error that occurs during program execution.",
            "Logic Error": "An error where the program runs but produces incorrect results."
        },

        "File Handling": {
            "Read": "Retrieving data from a file.",
            "Write": "Storing data into a file.",
            "Append": "Adding data to the end of a file without removing existing content."
        }

    },

    "glossary": {
        "Algorithm": "A step-by-step procedure for solving a problem.",
        "Pseudocode": "Structured description of an algorithm using plain language.",
        "Flowchart": "Diagram showing the logical steps of an algorithm.",
        "Variable": "Named storage location for data.",
        "Constant": "Value that does not change.",
        "Integer": "Whole number.",
        "Float": "Decimal number.",
        "String": "Sequence of characters.",
        "Boolean": "True or False value.",
        "List": "Ordered collection of values.",
        "Dictionary": "Collection of key-value pairs.",
        "Sequence": "Execution in order.",
        "Selection": "Decision-making structure.",
        "Iteration": "Repetition structure.",
        "Function": "Reusable block of code.",
        "Parameter": "Input to a function.",
        "Return": "Value sent back by a function.",
        "Scope": "Region where a variable is accessible.",
        "Syntax Error": "Violation of programming language rules.",
        "Runtime Error": "Error during execution.",
        "Logic Error": "Incorrect program logic."
    },

    "keywords": [
        "Algorithm", "Pseudocode", "Flowchart",
        "Variable", "Constant", "Data Type",
        "Integer", "Float", "String", "Boolean",
        "List", "Dictionary",
        "Sequence", "Selection", "Iteration",
        "If", "For", "While",
        "Function", "Parameter", "Return",
        "Syntax Error", "Runtime Error", "Logic Error"
    ]
},
"Input Validation": {
    "summary": "The process of checking that input data is sensible, reasonable, and within acceptable limits before processing.",
    "detailed_notes": {

        "Purpose": {
            "Prevent Errors": "Ensures invalid data does not cause incorrect processing.",
            "Improve Data Integrity": "Maintains accuracy and consistency of stored data.",
            "Enhance Security": "Reduces risk caused by malicious or inappropriate input."
        },

        "Validation Checks": {
            "Presence Check": "Ensures that data has been entered and is not empty.",
            "Length Check": "Ensures the number of characters entered is within a specified range.",
            "Range Check": "Ensures numeric input falls within a defined minimum and maximum value.",
            "Format Check": "Ensures data matches a required pattern (e.g., email format).",
            "Type Check": "Ensures the data entered is of the correct data type.",
            "Existence Check": "Ensures the entered value exists within a predefined list or database.",
            "Check Digit": "An additional digit calculated from other digits to detect input errors."
        },

        "Verification vs Validation": {
            "Validation": "Automatic checking that data meets specified rules.",
            "Verification": "Ensuring data has been entered correctly, often by comparing with the original source."
        },

        "Methods of Verification": {
            "Double Entry": "Data is entered twice and compared for consistency.",
            "Visual Check": "Data is manually checked against the original source."
        }

    },

    "glossary": {
        "Validation": "Automatic checking that input data follows defined rules.",
        "Verification": "Checking that data matches the original source.",
        "Presence Check": "Ensures data is not left blank.",
        "Length Check": "Checks number of characters.",
        "Range Check": "Checks numeric limits.",
        "Format Check": "Checks required pattern.",
        "Type Check": "Checks correct data type.",
        "Existence Check": "Checks data exists in a predefined list.",
        "Check Digit": "Digit used to detect input errors.",
        "Double Entry": "Entering data twice to compare.",
        "Visual Check": "Manual comparison against source."
    },

    "keywords": [
        "Validation", "Verification",
        "Presence Check", "Length Check",
        "Range Check", "Format Check",
        "Type Check", "Existence Check",
        "Check Digit",
        "Double Entry", "Visual Check"
    ]
},
"Testing and Debugging": {
    "summary": "The process of identifying, locating, and correcting errors in a program to ensure it meets its requirements and functions correctly.",
    "detailed_notes": {

        "Purpose of Testing": {
            "Detect Errors": "Identify faults in logic, syntax, or runtime behaviour.",
            "Ensure Requirements Met": "Confirm the program produces the expected output.",
            "Improve Reliability": "Increase confidence that the program works under different conditions."
        },

        "Types of Errors": {
            "Syntax Error": "An error caused by violating the rules of the programming language.",
            "Runtime Error": "An error that occurs during program execution, often causing the program to stop.",
            "Logic Error": "An error where the program executes without crashing but produces incorrect results."
        },

        "Types of Testing": {
            "Normal Data": "Valid input data that should be processed correctly.",
            "Boundary Data": "Valid input data at the extreme limits of acceptable range.",
            "Invalid (Abnormal) Data": "Input data that should be rejected by the program."
        },

        "Test Case": {
            "Definition": "A set of input data with the expected output used to verify correct program behaviour.",
            "Components": {
                "Test Data": "Input values provided to the program.",
                "Expected Result": "The correct output that should be produced."
            }
        },

        "Debugging Techniques": {
            "Tracing": "Following the flow of program execution step-by-step to identify errors.",
            "Breakpoints": "Pausing program execution at specific points to examine variable values.",
            "Print Statements": "Displaying intermediate values to monitor program behaviour."
        }

    },

    "glossary": {
        "Testing": "Process of checking whether a program works as intended.",
        "Debugging": "Process of finding and correcting errors in a program.",
        "Syntax Error": "Violation of programming language rules.",
        "Runtime Error": "Error occurring during execution.",
        "Logic Error": "Incorrect program logic producing wrong output.",
        "Normal Data": "Valid input within acceptable range.",
        "Boundary Data": "Valid input at extreme limits.",
        "Invalid Data": "Input that should be rejected.",
        "Test Case": "Input data with expected output.",
        "Tracing": "Step-by-step execution tracking.",
        "Breakpoint": "Pause point during execution."
    },

    "keywords": [
        "Testing", "Debugging",
        "Syntax Error", "Runtime Error", "Logic Error",
        "Normal Data", "Boundary Data", "Invalid Data",
        "Test Case",
        "Tracing", "Breakpoint"
    ]
},
"Algorithm Design": {
    "summary": "The process of planning and structuring a step-by-step solution to a problem before implementing it as a program.",
    "detailed_notes": {

        "Definition": {
            "Algorithm": "A finite sequence of clear, unambiguous steps used to solve a problem or perform a task.",
            "Characteristics": {
                "Finiteness": "The algorithm must terminate after a limited number of steps.",
                "Definiteness": "Each step must be clearly and precisely defined.",
                "Input": "Zero or more inputs supplied externally.",
                "Output": "At least one result produced.",
                "Effectiveness": "Each step must be simple enough to be carried out."
            }
        },

        "Design Techniques": {
            "Decomposition": "Breaking a complex problem into smaller, manageable sub-problems.",
            "Abstraction": "Focusing on essential details while ignoring irrelevant information.",
            "Stepwise Refinement": "Developing an algorithm by starting with a high-level solution and gradually adding detail."
        },

        "Representation Methods": {
            "Pseudocode": "A structured description of an algorithm written in plain language using programming-like constructs.",
            "Flowchart": {
                "Definition": "A graphical representation of an algorithm using standard symbols.",
                "Common Symbols": {
                    "Terminator": "Indicates start or end.",
                    "Process": "Represents a processing step.",
                    "Input/Output": "Represents data input or output.",
                    "Decision": "Represents a branching point based on a condition.",
                    "Flowline": "Shows direction of control flow."
                }
            }
        },

        "Efficiency": {
            "Time Efficiency": "The amount of time an algorithm takes to complete.",
            "Space Efficiency": "The amount of memory an algorithm uses during execution."
        }

    },

    "glossary": {
        "Algorithm": "Step-by-step procedure for solving a problem.",
        "Decomposition": "Breaking a problem into smaller parts.",
        "Abstraction": "Removing unnecessary detail to focus on key aspects.",
        "Stepwise Refinement": "Gradually adding detail to an algorithm.",
        "Pseudocode": "Structured algorithm description.",
        "Flowchart": "Graphical representation of algorithm steps.",
        "Time Efficiency": "Time taken to execute.",
        "Space Efficiency": "Memory used during execution."
    },

    "keywords": [
        "Algorithm", "Decomposition", "Abstraction",
        "Stepwise Refinement",
        "Pseudocode", "Flowchart",
        "Time Efficiency", "Space Efficiency"
    ]
},
"Software Engineering": {
    "summary": "The systematic approach to designing, developing, testing, deploying, and maintaining software systems.",
    "detailed_notes": {

        "Software Development Life Cycle (SDLC)": {
            "Planning": "Identifying the problem, objectives, scope, and feasibility.",
            "Requirements Analysis": "Gathering and documenting functional and non-functional requirements.",
            "Design": "Creating system architecture and detailed design specifications.",
            "Implementation": "Writing and compiling the program code.",
            "Testing": "Verifying that the system meets requirements and functions correctly.",
            "Deployment": "Releasing the software for use.",
            "Maintenance": "Updating, improving, and fixing issues after deployment."
        },

        "Development Models": {
            "Waterfall Model": "A linear and sequential approach where each phase is completed before the next begins.",
            "Iterative Model": "Development through repeated cycles, refining the system in stages.",
            "Agile": "An adaptive approach emphasizing incremental development, collaboration, and flexibility."
        },

        "Documentation": {
            "Technical Documentation": "Information for developers detailing system design and code structure.",
            "User Documentation": "Guides and instructions for end-users."
        },

        "Version Control": {
            "Purpose": "Tracking and managing changes to source code over time.",
            "Benefits": [
                "Maintains revision history",
                "Supports collaboration",
                "Allows rollback to previous versions"
            ]
        },

        "Quality Assurance": {
            "Code Review": "Systematic examination of source code to detect errors and improve quality.",
            "Unit Testing": "Testing individual components independently.",
            "Integration Testing": "Testing combined components to ensure they work together.",
            "System Testing": "Testing the complete system as a whole."
        }

    },

    "glossary": {
        "Software Engineering": "Systematic development and maintenance of software.",
        "SDLC": "Software Development Life Cycle.",
        "Waterfall Model": "Sequential development model.",
        "Iterative Model": "Repeated cycle development model.",
        "Agile": "Incremental and flexible development approach.",
        "Technical Documentation": "Documentation for developers.",
        "User Documentation": "Documentation for users.",
        "Version Control": "System for managing code changes.",
        "Code Review": "Examination of code for quality.",
        "Unit Testing": "Testing individual components.",
        "Integration Testing": "Testing combined components.",
        "System Testing": "Testing the complete system."
    },

    "keywords": [
        "Software Engineering",
        "SDLC",
        "Waterfall",
        "Iterative",
        "Agile",
        "Documentation",
        "Version Control",
        "Unit Testing",
        "Integration Testing",
        "System Testing"
    ]
},
"Spreadsheets": {
    "summary": "Application software used to organise, calculate, analyse, and visualise data in tabular form.",
    "detailed_notes": {

        "Basic Concepts": {
            "Workbook": "A spreadsheet file containing one or more worksheets.",
            "Worksheet": "A single spreadsheet page consisting of rows and columns.",
            "Cell": "The intersection of a row and a column where data is stored.",
            "Cell Reference": "The address of a cell, identified by column letter and row number (e.g., A1).",
            "Range": "A group of selected cells."
        },

        "Data Types": {
            "Label": "Text data used for headings or descriptions.",
            "Value": "Numeric data used in calculations.",
            "Formula": "An expression used to perform calculations, beginning with '='.",
            "Function": "A predefined formula that performs a specific calculation."
        },

        "Common Functions": {
            "SUM": "Adds a range of numbers.",
            "AVERAGE": "Calculates the mean of a range of numbers.",
            "MIN": "Returns the smallest value in a range.",
            "MAX": "Returns the largest value in a range.",
            "COUNT": "Counts the number of numeric entries in a range."
        },

        "Cell Referencing": {
            "Relative Reference": "Changes when a formula is copied to another cell.",
            "Absolute Reference": "Remains constant when a formula is copied (e.g., $A$1).",
            "Mixed Reference": "Partially fixed reference (e.g., $A1 or A$1)."
        },

        "Data Analysis": {
            "Sorting": "Arranging data in ascending or descending order.",
            "Filtering": "Displaying only data that meets specified criteria.",
            "Conditional Formatting": "Automatically formatting cells based on defined rules."
        },

        "Charts": {
            "Purpose": "Graphical representation of data for easier interpretation.",
            "Common Types": {
                "Bar Chart": "Compares values across categories.",
                "Line Chart": "Shows trends over time.",
                "Pie Chart": "Shows proportions of a whole."
            }
        }

    },

    "glossary": {
        "Workbook": "Spreadsheet file containing worksheets.",
        "Worksheet": "Single spreadsheet page.",
        "Cell": "Intersection of row and column.",
        "Cell Reference": "Address of a cell.",
        "Range": "Group of cells.",
        "Formula": "Expression for calculation.",
        "Function": "Predefined formula.",
        "Relative Reference": "Reference that changes when copied.",
        "Absolute Reference": "Reference that remains fixed.",
        "Mixed Reference": "Partially fixed reference.",
        "Sorting": "Ordering data.",
        "Filtering": "Displaying selected data.",
        "Conditional Formatting": "Formatting based on rules.",
        "Chart": "Graphical data representation."
    },

    "keywords": [
        "Workbook", "Worksheet", "Cell", "Cell Reference",
        "Range", "Formula", "Function",
        "SUM", "AVERAGE", "MIN", "MAX", "COUNT",
        "Relative Reference", "Absolute Reference", "Mixed Reference",
        "Sorting", "Filtering", "Conditional Formatting",
        "Chart"
    ]
},
"Networking": {
    "summary": "The interconnection of computers and devices to enable communication and sharing of data and resources.",
    "detailed_notes": {

        "Basic Concepts": {
            "Network": "A group of connected computers and devices that can communicate and share resources.",
            "Node": "Any device connected to a network.",
            "Protocol": "A set of rules governing data communication.",
            "Bandwidth": "The maximum rate of data transfer across a network connection.",
            "Latency": "The delay before data transfer begins following an instruction."
        },

        "Types of Networks": {
            "LAN": "Local Area Network covering a small geographical area.",
            "WAN": "Wide Area Network covering a large geographical area.",
            "MAN": "Metropolitan Area Network covering a city or metropolitan region."
        },

        "Network Hardware": {
            "Router": "A device that forwards data packets between networks.",
            "Switch": "Connects devices within the same network and forwards data to the intended recipient.",
            "Modem": "Modulates and demodulates signals for internet connectivity.",
            "Access Point": "Allows wireless devices to connect to a wired network."
        },

        "Addressing": {
            "IP Address": "A logical numerical label assigned to a device on a network.",
            "IPv4": "32-bit IP addressing format.",
            "IPv6": "128-bit IP addressing format.",
            "MAC Address": "A unique physical address assigned to a network interface."
        },

        "Data Transmission": {
            "Packet": "A unit of data transmitted over a network.",
            "Client-Server": "Model where clients request services from a central server.",
            "Peer-to-Peer": "Model where each device can act as both client and server."
        },

        "Network Topologies": {
            "Star Topology": "All devices connect to a central device.",
            "Bus Topology": "All devices share a single communication line.",
            "Ring Topology": "Devices are connected in a circular structure."
        }

    },

    "glossary": {
        "Network": "Connected devices sharing data and resources.",
        "Protocol": "Rules for communication.",
        "Bandwidth": "Maximum data transfer rate.",
        "Latency": "Delay in data transmission.",
        "LAN": "Local Area Network.",
        "WAN": "Wide Area Network.",
        "MAN": "Metropolitan Area Network.",
        "Router": "Forwards packets between networks.",
        "Switch": "Connects devices within a network.",
        "IP Address": "Logical network address.",
        "MAC Address": "Physical hardware address.",
        "Packet": "Unit of transmitted data.",
        "Client-Server": "Centralised service model.",
        "Peer-to-Peer": "Decentralised network model."
    },

    "keywords": [
        "Network", "Protocol",
        "Bandwidth", "Latency",
        "LAN", "WAN", "MAN",
        "Router", "Switch", "Modem", "Access Point",
        "IP Address", "IPv4", "IPv6", "MAC Address",
        "Packet",
        "Client-Server", "Peer-to-Peer",
        "Star", "Bus", "Ring"
    ]
},
"Security and Privacy": {
    "summary": "The protection of computer systems, networks, and data from unauthorised access, misuse, damage, or disclosure while ensuring responsible handling of personal information.",
    "detailed_notes": {

        "Core Principles": {
            "Confidentiality": "Ensuring that data is accessible only to authorised users.",
            "Integrity": "Ensuring that data is accurate and not altered without authorisation.",
            "Availability": "Ensuring that systems and data are accessible when required."
        },

        "Threats": {
            "Malware": "Malicious software designed to damage or disrupt systems.",
            "Virus": "A type of malware that replicates itself by attaching to programs.",
            "Worm": "Malware that spreads automatically across networks.",
            "Trojan": "Malware disguised as legitimate software.",
            "Phishing": "Fraudulent attempt to obtain sensitive information by impersonation.",
            "Denial of Service (DoS)": "An attack that overwhelms a system to make it unavailable."
        },

        "Protection Measures": {
            "Authentication": "Verifying the identity of a user.",
            "Authorisation": "Granting access rights after authentication.",
            "Encryption": "Converting data into an unreadable form to prevent unauthorised access.",
            "Firewall": "A security system that monitors and controls incoming and outgoing network traffic.",
            "Antivirus": "Software designed to detect and remove malware.",
            "Two-Factor Authentication (2FA)": "Security process requiring two different forms of verification."
        },

        "Privacy": {
            "Personal Data": "Information that can identify an individual.",
            "Data Protection": "Practices and policies designed to safeguard personal data.",
            "Data Breach": "Unauthorised access to confidential data."
        },

        "Ethical Considerations": {
            "Responsible Use": "Using technology in a lawful and ethical manner.",
            "Digital Footprint": "The trail of data left by users when interacting online."
        }

    },

    "glossary": {
        "Confidentiality": "Restricting data access to authorised users.",
        "Integrity": "Maintaining accuracy and consistency of data.",
        "Availability": "Ensuring systems are accessible when needed.",
        "Malware": "Malicious software.",
        "Phishing": "Fraudulent data collection attempt.",
        "Authentication": "Identity verification.",
        "Authorisation": "Granting access rights.",
        "Encryption": "Converting data into secure form.",
        "Firewall": "Network traffic security system.",
        "Antivirus": "Malware detection software.",
        "Personal Data": "Identifiable individual information.",
        "Data Breach": "Unauthorised data access.",
        "Digital Footprint": "Online data trail."
    },

    "keywords": [
        "Confidentiality", "Integrity", "Availability",
        "Malware", "Virus", "Worm", "Trojan", "Phishing", "DoS",
        "Authentication", "Authorisation", "Encryption",
        "Firewall", "Antivirus", "Two-Factor Authentication",
        "Personal Data", "Data Protection", "Data Breach",
        "Digital Footprint"
    ]
},
"Intellectual Property": {
    "summary": "Legal rights that protect creations of the mind, including digital content, software, and other original works.",
    "detailed_notes": {

        "Types of Intellectual Property": {
            "Copyright": "Legal protection granted to creators of original works, giving them exclusive rights to use and distribute their work.",
            "Trademark": "A symbol, name, or logo legally registered to represent a company or product.",
            "Patent": "Legal protection granted for a new invention, giving exclusive rights to the inventor for a limited period."
        },

        "Software Licensing": {
            "Proprietary Software": "Software owned by an individual or company, with restrictions on use, modification, and distribution.",
            "Open Source Software": "Software whose source code is publicly available for use and modification under specific licence terms.",
            "Freeware": "Software distributed free of charge but usually without access to source code.",
            "Shareware": "Software distributed for trial use, often with limited features or time restrictions."
        },

        "Copyright Infringement": {
            "Definition": "Using copyrighted material without permission from the copyright holder.",
            "Software Piracy": "Unauthorised copying, distribution, or use of software.",
            "Plagiarism": "Presenting another person’s work as one’s own without proper acknowledgment."
        },

        "Ethical and Legal Responsibilities": {
            "Fair Use": "Limited use of copyrighted material without permission under specific conditions.",
            "Attribution": "Giving proper credit to the original creator.",
            "Compliance": "Following licensing agreements and copyright laws."
        }

    },

    "glossary": {
        "Intellectual Property": "Legal rights protecting creations of the mind.",
        "Copyright": "Protection for original works.",
        "Trademark": "Registered symbol or name representing a brand.",
        "Patent": "Protection for new inventions.",
        "Proprietary Software": "Software with restricted rights.",
        "Open Source Software": "Software with accessible source code under licence.",
        "Freeware": "Free-to-use software.",
        "Shareware": "Trial software with restrictions.",
        "Software Piracy": "Illegal copying or distribution of software.",
        "Plagiarism": "Using another’s work without credit."
    },

    "keywords": [
        "Intellectual Property",
        "Copyright",
        "Trademark",
        "Patent",
        "Proprietary Software",
        "Open Source Software",
        "Freeware",
        "Shareware",
        "Software Piracy",
        "Plagiarism",
        "Fair Use",
        "Attribution"
    ]
},
"Impact of Computing": {
    "summary": "The effects of computing technologies on individuals, society, and the environment, including social, economic, and ethical consequences.",
    "detailed_notes": {

        "Social Impact": {
            "Communication": "Computing enables instant communication through email, messaging, and social media.",
            "Education": "Technology supports online learning, research, and access to information.",
            "Social Interaction": "Computing changes how people interact, collaborate, and form communities."
        },

        "Economic Impact": {
            "Automation": "Computers perform tasks automatically, increasing efficiency but reducing some job roles.",
            "Employment": "New careers are created in technology-related fields.",
            "E-commerce": "Online buying and selling of goods and services."
        },

        "Ethical Impact": {
            "Privacy": "Concerns about collection and use of personal data.",
            "Security": "Need to protect systems and data from misuse.",
            "Digital Divide": "Unequal access to technology between individuals or regions."
        },

        "Environmental Impact": {
            "Energy Consumption": "Computing devices and data centres consume electricity.",
            "Electronic Waste": "Discarded electronic devices can harm the environment if not recycled properly.",
            "Sustainability": "Designing systems to reduce environmental impact."
        }

    },

    "glossary": {
        "Automation": "Use of computers to perform tasks with minimal human input.",
        "E-commerce": "Online buying and selling.",
        "Digital Divide": "Gap between those with and without access to technology.",
        "Electronic Waste": "Discarded electronic equipment."
    },

    "keywords": [
        "Social Impact",
        "Economic Impact",
        "Ethical Impact",
        "Environmental Impact",
        "Automation",
        "E-commerce",
        "Digital Divide",
        "Electronic Waste",
        "Sustainability"
    ]
},
"Emerging Technologies": {
    "summary": "New and developing technologies that have the potential to significantly impact society, industries, and daily life.",
    "detailed_notes": {

        "Artificial Intelligence": {
            "Definition": "The ability of machines to perform tasks that normally require human intelligence.",
            "Machine Learning": "A subset of artificial intelligence where systems learn patterns from data.",
            "Applications": "Used in areas such as recommendation systems, image recognition, and automation.",
            "Ethical Issues": "Concerns include bias, accountability, and transparency."
        },

        "Blockchain": {
            "Definition": "A distributed ledger technology that records transactions across multiple computers.",
            "Characteristics": {
                "Decentralisation": "No central authority controls the system.",
                "Immutability": "Recorded data cannot easily be altered.",
                "Transparency": "Transactions can be verified by participants."
            },
            "Applications": "Used in cryptocurrencies, supply chain tracking, and digital records."
        },

        "Internet of Things (IoT)": {
            "Definition": "A network of physical devices embedded with sensors and connectivity.",
            "Examples": "Smart homes, wearable devices, and smart cities.",
            "Impact": "Improves automation and data collection but raises security and privacy concerns."
        },

        "Virtual and Augmented Reality": {
            "Virtual Reality (VR)": "A fully computer-generated environment experienced through specialised equipment.",
            "Augmented Reality (AR)": "Digital content overlaid onto the real world.",
            "Uses": "Education, training, entertainment, and simulation."
        },

        "Quantum Computing": {
            "Definition": "Computing based on quantum-mechanical phenomena.",
            "Qubit": "The basic unit of quantum information.",
            "Potential": "Solves certain complex problems more efficiently than classical computers.",
            "Limitations": "Currently expensive, experimental, and sensitive to errors."
        }

    },

    "glossary": {
        "Artificial Intelligence": "Machines performing tasks requiring human intelligence.",
        "Machine Learning": "Systems learning from data.",
        "Blockchain": "Distributed transaction ledger.",
        "Internet of Things": "Network of connected physical devices.",
        "Virtual Reality": "Immersive digital environment.",
        "Augmented Reality": "Digital overlay on real world.",
        "Quantum Computing": "Computing using quantum phenomena.",
        "Qubit": "Quantum information unit."
    },

    "keywords": [
        "Artificial Intelligence",
        "Machine Learning",
        "Blockchain",
        "Internet of Things",
        "Virtual Reality",
        "Augmented Reality",
        "Quantum Computing",
        "Qubit"
    ]
}
}
