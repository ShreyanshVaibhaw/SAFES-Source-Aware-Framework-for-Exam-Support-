"""Generate 3 sample study PDFs for testing SAFES."""

from fpdf import FPDF
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "uploads"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def pdf1_operating_systems():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "Operating Systems - Study Notes", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 1: Introduction to Operating Systems", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "An Operating System (OS) is system software that manages computer hardware and software "
        "resources and provides common services for computer programs. The OS acts as an intermediary "
        "between users and the computer hardware.\n\n"
        "Key Functions of an Operating System:\n"
        "1. Process Management: The OS handles the creation, scheduling, and termination of processes. "
        "It allocates CPU time to various processes using scheduling algorithms such as First-Come-First-Served "
        "(FCFS), Shortest Job First (SJF), Round Robin (RR), and Priority Scheduling.\n\n"
        "2. Memory Management: The OS manages primary memory (RAM) by keeping track of which parts "
        "of memory are in use, allocating memory to processes when needed, and deallocating it when no "
        "longer needed. Techniques include paging, segmentation, and virtual memory.\n\n"
        "3. File System Management: The OS provides a uniform interface for storing and retrieving data "
        "on storage devices. It manages files and directories, handles permissions, and implements file "
        "systems like NTFS, ext4, and FAT32.\n\n"
        "4. I/O Device Management: The OS manages input/output devices through device drivers, buffering, "
        "caching, and spooling to ensure efficient data transfer between devices and the CPU.\n\n"
        "5. Security and Protection: The OS implements user authentication, access control lists (ACLs), "
        "encryption, and firewall capabilities to protect system resources from unauthorized access."
    ))
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 2: Process Management", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "A process is a program in execution. Each process has its own address space, program counter, "
        "registers, and stack. Processes can be in one of five states: New, Ready, Running, Waiting, "
        "or Terminated.\n\n"
        "Process Scheduling Algorithms:\n\n"
        "First-Come-First-Served (FCFS): Processes are executed in the order they arrive. Simple but can "
        "cause the convoy effect where short processes wait behind long ones.\n\n"
        "Shortest Job First (SJF): The process with the smallest burst time is selected next. This "
        "minimizes average waiting time but requires knowledge of future burst times.\n\n"
        "Round Robin (RR): Each process gets a fixed time quantum (typically 10-100 milliseconds). "
        "After the quantum expires, the process is moved to the back of the ready queue.\n\n"
        "Priority Scheduling: Each process is assigned a priority. The CPU is allocated to the process "
        "with the highest priority. Can lead to starvation, which is solved using aging.\n\n"
        "Context Switching: When the CPU switches from one process to another, the system must save "
        "the state of the old process and load the saved state of the new process. This takes 1-10 microseconds.\n\n"
        "Inter-Process Communication (IPC): Methods include shared memory, message passing, pipes, "
        "sockets, and signals. The Producer-Consumer problem is a classic IPC scenario."
    ))

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 3: Memory Management", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "Virtual Memory: Virtual memory allows execution of processes not completely in memory. "
        "It separates user logical memory from physical memory using demand paging.\n\n"
        "Paging: Physical memory is divided into fixed-size frames. Logical memory is divided into "
        "same-size pages. A page table maps logical pages to physical frames.\n\n"
        "Page Replacement Algorithms:\n"
        "- FIFO: Replace the oldest page. Simple but suffers from Belady anomaly.\n"
        "- LRU: Replace the page not used for longest time. Good but expensive.\n"
        "- Optimal: Replace page not used for longest future time. Theoretical best.\n\n"
        "Thrashing: When a process spends more time paging than executing. Occurs when working set "
        "exceeds available physical memory.\n\n"
        "Deadlock: Occurs when processes wait for each other to release resources. Four conditions: "
        "Mutual Exclusion, Hold and Wait, No Preemption, Circular Wait. Solutions include prevention, "
        "avoidance (Banker's algorithm), detection, and recovery."
    ))

    path = OUTPUT_DIR / "Operating_Systems_Notes.pdf"
    pdf.output(str(path))
    print(f"Created: {path.name} ({path.stat().st_size // 1024} KB)")


def pdf2_computer_networks():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "Computer Networks - Exam Revision", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 1: OSI Model and TCP/IP", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "The OSI model standardizes communication functions into seven layers:\n\n"
        "Layer 7 - Application: HTTP, FTP, SMTP, DNS, DHCP. User interaction layer.\n"
        "Layer 6 - Presentation: Data translation, encryption (SSL/TLS), compression.\n"
        "Layer 5 - Session: Session management, checkpointing, recovery.\n"
        "Layer 4 - Transport: TCP (reliable, ordered) and UDP (fast, connectionless).\n"
        "Layer 3 - Network: IP addressing, routing. Routers operate here.\n"
        "Layer 2 - Data Link: Framing, MAC addressing, error detection. Switches operate here.\n"
        "Layer 1 - Physical: Electrical signals, cables, data rates. Hubs operate here.\n\n"
        "The TCP/IP model has four layers: Network Access, Internet, Transport, and Application."
    ))
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 2: TCP vs UDP", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "TCP (Transmission Control Protocol):\n"
        "- Connection-oriented: Three-way handshake (SYN, SYN-ACK, ACK)\n"
        "- Reliable: Acknowledgments, sequence numbers, retransmission\n"
        "- Flow control: Sliding window protocol\n"
        "- Congestion control: Slow start, congestion avoidance, fast retransmit\n"
        "- Ordered delivery, Header: 20-60 bytes\n"
        "- Use cases: HTTP, FTP, SMTP, SSH\n\n"
        "UDP (User Datagram Protocol):\n"
        "- Connectionless: No handshake\n"
        "- Unreliable: No acknowledgments, no retransmission\n"
        "- No flow/congestion control, No ordering\n"
        "- Header: 8 bytes (source port, dest port, length, checksum)\n"
        "- Use cases: DNS, DHCP, video streaming, gaming, VoIP\n\n"
        "TCP is used when reliability matters. UDP when speed matters more than reliability."
    ))

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 3: IP Addressing and Subnetting", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "IPv4: 32-bit address in four octets (e.g., 192.168.1.1).\n"
        "Classes: A (1-126, 16M hosts), B (128-191, 65K hosts), C (192-223, 254 hosts)\n"
        "Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16\n\n"
        "Subnetting divides a network into smaller sub-networks using subnet masks.\n"
        "CIDR notation (e.g., /24) indicates network bits.\n"
        "Example: 192.168.1.0/26 creates 4 subnets with 62 usable hosts each.\n\n"
        "IPv6: 128-bit addresses in hexadecimal. 340 undecillion addresses.\n"
        "Features: Auto-configuration, built-in IPsec, simplified headers.\n\n"
        "NAT: Multiple private devices share one public IP. Types: Static, Dynamic, PAT.\n\n"
        "DNS: Hierarchical naming system translating domains to IPs. Uses root servers, "
        "TLD servers, and authoritative servers. Supports recursive and iterative queries."
    ))

    path = OUTPUT_DIR / "Computer_Networks_Revision.pdf"
    pdf.output(str(path))
    print(f"Created: {path.name} ({path.stat().st_size // 1024} KB)")


def pdf3_dbms():
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, "Database Management Systems", new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 1: Relational Database Concepts", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "A DBMS manages databases, providing mechanisms for storing, retrieving, and manipulating data.\n\n"
        "Relational Model: Data in tables (relations) with rows (tuples) and columns (attributes).\n\n"
        "Keys:\n"
        "- Primary Key: Uniquely identifies each record. Cannot be NULL.\n"
        "- Foreign Key: References primary key of another table.\n"
        "- Candidate Key: Minimal set that uniquely identifies a tuple.\n"
        "- Super Key: Set that uniquely identifies (may have extra attributes).\n"
        "- Composite Key: Primary key from multiple columns.\n\n"
        "ACID Properties:\n"
        "- Atomicity: Transaction is all-or-nothing.\n"
        "- Consistency: Database moves from one valid state to another.\n"
        "- Isolation: Concurrent transactions don't interfere.\n"
        "- Durability: Committed changes are permanent.\n\n"
        "ER Model: Entities (Student, Course), Attributes (name, age), Relationships (enrolls_in). "
        "Cardinality: one-to-one, one-to-many, many-to-many."
    ))
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 2: Normalization", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "Normalization reduces redundancy and improves data integrity.\n\n"
        "1NF: Atomic values, single type per column, unique rows, no repeating groups.\n\n"
        "2NF: In 1NF + no partial dependencies on composite primary key.\n\n"
        "3NF: In 2NF + no transitive dependencies. Non-key attributes depend only on primary key.\n"
        "Example: Student_ID -> Department -> HOD violates 3NF.\n\n"
        "BCNF: Stronger 3NF. For every X -> Y, X must be a super key.\n\n"
        "Denormalization: Intentionally adding redundancy for read performance. Used in data "
        "warehousing and OLAP systems."
    ))

    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "Chapter 3: SQL and Query Processing", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, (
        "SQL Categories:\n"
        "- DDL: CREATE, ALTER, DROP, TRUNCATE (define structure)\n"
        "- DML: SELECT, INSERT, UPDATE, DELETE (manipulate data)\n"
        "- DCL: GRANT, REVOKE (control access)\n"
        "- TCL: COMMIT, ROLLBACK, SAVEPOINT (manage transactions)\n\n"
        "JOINs: INNER (matching rows), LEFT (all left + matches), RIGHT (all right + matches), "
        "FULL OUTER (all rows from both).\n\n"
        "Indexes: B-Tree for range queries, Hash for equality. Trade-off: faster reads, slower writes.\n\n"
        "Query Processing: 1) Parsing (syntax check), 2) Optimization (cost-based plan selection), "
        "3) Execution.\n\n"
        "Concurrency Control: Locking (shared/exclusive), timestamp ordering, MVCC. "
        "Two-Phase Locking (2PL) ensures serializability."
    ))

    path = OUTPUT_DIR / "DBMS_Study_Material.pdf"
    pdf.output(str(path))
    print(f"Created: {path.name} ({path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    pdf1_operating_systems()
    pdf2_computer_networks()
    pdf3_dbms()
    print("\nAll 3 PDFs ready in data/uploads/")
