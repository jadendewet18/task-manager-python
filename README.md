# Task Manager Terminal

A robust, role-based command-line interface (CLI) application built in Python to help small teams efficiently coordinate, delegate, track, and analyze project milestones. 

The application utilizes local flat-text files (`user.txt` and `tasks.txt`) acting as an lightweight, decentralized database ecosystem.

---

## Features

### Core Task Tracking
* **Secure Access Engine:** Restricts system utility behind an initial credential login wall validated against local records.
* **Interactive Assignment Modification (`vm`):** Allows users to selectively target assigned items via dynamic menus to toggle task completion states or modify due dates and reassign ownership handlers.
* **Global Ecosystem Monitoring (`va`):** Transparently formats and prints all systemic workflow objects concurrently.
* **Safe Appending Guard:** Employs protective formatting handlers that preserve structure during registration or task creation, guaranteeing data points never crush together on a single line.

### Administrative Capabilities (Exclusive to `admin`)
* **Unique Profile Generation (`r`):** Includes verification guards preventing duplicate user credentials from colliding within the ecosystem.
* **Live System Analytics Summary (`gr` / `ds`):** Compiles and streams high-level team performance reports tracking workload share distribution balances, completion percentages, and open overdue counts.
* **System Purge Controller (`del`):** Grants the power to permanently wipe out invalid or deprecated tracking arrays via indexed targets.

---

## System Data Architecture

Data arrays are serialized using standard comma-separated variables (`CSV` format) natively across two files:

* **`user.txt`** — `Username, Password`
* **`tasks.txt`** — `Assigned User, Title, Description, Date Assigned, Due Date, Completed Status`

---

## Getting Started

### Prerequisites
* **Python 3.x** installed locally.

### Installation & Execution
1. Clone the repository to your desktop machine:
   ```bash
   git clone [https://github.com/jadendewet18/task-manager-python.git](https://github.com/jadendewet18/task-manager-python.git)
