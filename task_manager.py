"""Task Manager Capstone Project.

This program handles small business task tracking, credential verification,
and detailed reporting with distinct administrative controls.
"""

import datetime
import os


# ==============================================================================
# 1. HELPER / DEFENSIVE PROGRAMMING FUNCTIONS
# ==============================================================================

def load_users():
    """Reads user.txt and returns a dictionary of usernames and passwords.

    Returns:
        dict: A dictionary where keys are usernames and values are passwords.
    """
    user_details = {}
    
    # Check if the file exists before attempting to open it.
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as file:
            file.write("admin, adm1n\n")
        return {"admin": "adm1n"}

    with open("user.txt", "r") as file:
        for line in file:
            if line.strip():
                # Split line by comma and space to extract credentials.
                username, password = line.strip().split(", ")
                user_details[username] = password
                
    return user_details


def load_tasks():
    """Reads tasks.txt and returns a list of individual task lists.

    Returns:
        list: A nested list structure containing split task data.
    """
    tasks = []
    
    if not os.path.exists("tasks.txt"):
        return tasks

    with open("tasks.txt", "r") as file:
        for line in file:
            if line.strip():
                task_data = line.strip().split(", ")
                # Ensure the data matches the expected 6 fields.
                if len(task_data) == 6:
                    tasks.append(task_data)
                    
    return tasks


def save_tasks(tasks_list):
    """Overwrites tasks.txt with the updated nested list of tasks.

    This systematically ensures every single task gets its own separate line
    by ending each written record with a clean newline character.

    Args:
        tasks_list (list): Nested list structure containing all tasks.
    """
    with open("tasks.txt", "w") as file:
        for task in tasks_list:
            # Join the task components back into a comma-separated line.
            file.write(", ".join(task) + "\n")


def get_valid_task_number(user_tasks, total_tasks):
    """Recursively validates the task index chosen by the user.

    Args:
        user_tasks (dict): Map of displayed menu numbers to main database index.
        total_tasks (int): Total number of items displayed to the user.

    Returns:
        int: The verified key value selected, or -1 to return to the menu.
    """
    user_input = input("\nEnter task number to edit/complete (or -1 to exit): ").strip()
    
    if user_input == "-1":
        return -1
        
    try:
        task_num = int(user_input)
        if task_num in user_tasks:
            return task_num
        
        print(f"Error: Number out of range. Choose between 1 and {total_tasks}.")
        return get_valid_task_number(user_tasks, total_tasks)
        
    except ValueError:
        print("Error: Invalid entry. Please input a numerical value.")
        return get_valid_task_number(user_tasks, total_tasks)


# ==============================================================================
# 2. CORE SYSTEM FUNCTIONALITIES
# ==============================================================================

def reg_user():
    """Registers a new user into user.txt.

    Enforces unique username validation and confirmation checking.
    """
    print("\n--- Register a New User ---")
    user_details = load_users()
    
    while True:
        new_username = input("Enter new username: ").strip()
        
        # Prevent duplicate usernames as requested in Part 3.
        if new_username in user_details:
            print("Error: Username already exists. Try a different name.\n")
            continue
        if ", " in new_username or not new_username:
            print("Error: Username cannot contain commas or be empty.\n")
            continue
        break

    new_password = input("Enter new password: ")
    confirm_password = input("Confirm new password: ")

    # Check if the new password matches the confirmation password.
    if new_password == confirm_password:
        # Check if the file already ends with a newline to prevent string smashing.
        ensure_newline_before_append("user.txt")
        
        with open("user.txt", "a") as file:
            file.write(f"{new_username}, {new_password}\n")
        print(f"Success: User '{new_username}' added to database.\n")
    else:
        print("Error: Passwords did not match. Registration cancelled.\n")


def ensure_newline_before_append(filename):
    """Helper tool to check if a file ends with a newline character.

    If it does not, it adds one dynamically so appending writes onto a
    brand-new line instead of smashing records together.
    """
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, "rb+") as file:
            file.seek(-1, os.SEEK_END)
            last_char = file.read(1)
            if last_char != b'\n':
                file.write(b'\n')


def add_task():
    """Prompts for task attributes and saves them to tasks.txt.

    Ensures data does not collide on an existing line without a trailing newline.
    """
    print("\n--- Add a New Task ---")
    user_details = load_users()
    
    while True:
        task_user = input("Enter username assigned to task: ").strip()
        if task_user not in user_details:
            print("Warning: User does not exist in system database.")
            confirm = input("Assign anyway? (yes/no): ").lower()
            if confirm != 'yes':
                continue
        break

    title = input("Enter task title: ").replace(",", "")
    description = input("Enter task description: ").replace(",", "")
    due_date = input("Enter due date (e.g., 24 Oct 2026): ").replace(",", "")
    
    # Get the current date and format it correctly.
    current_date = datetime.date.today().strftime("%d %b %Y")
    task_completed = "No"

    # Fix logic: Systematically verify and handle existing lines before appending.
    ensure_newline_before_append("tasks.txt")

    with open("tasks.txt", "a") as file:
        file.write(f"{task_user}, {title}, {description}, {current_date}, {due_date}, {task_completed}\n")
    print("Success: Task assigned and written to storage.\n")


def view_all():
    """Reads and cleanly prints every recorded task from storage."""
    print("\n=== VIEW ALL GLOBAL TASKS ===")
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks are currently tracked in system database.\n")
        return

    for t in tasks:
        print("-" * 50)
        print(f"Task Title:       {t[1]}")
        print(f"Assigned To:      {t[0]}")
        print(f"Date Assigned:    {t[3]}")
        print(f"Due Date:         {t[4]}")
        print(f"Completed?        {t[5]}")
        print(f"Description:      {t[2]}")
    print("-" * 50 + "\n")


def view_mine(current_user):
    """Displays specific user tasks and allows modification or status edits."""
    print(f"\n=== MY ASSIGNED TASKS ({current_user}) ===")
    tasks = load_tasks()
    
    if not tasks:
        print("No tasks logged in data ecosystem.\n")
        return

    # Keep track of indices uniquely assigned to this specific user.
    user_tasks = {}
    display_index = 1

    for global_index, t in enumerate(tasks):
        if t[0] == current_user:
            user_tasks[display_index] = global_index
            print("-" * 50)
            print(f"ID Number: [{display_index}]")
            print(f"Task Title:       {t[1]}")
            print(f"Date Assigned:    {t[3]}")
            print(f"Due Date:         {t[4]}")
            print(f"Completed?        {t[5]}")
            print(f"Description:      {t[2]}")
            display_index += 1

    if not user_tasks:
        print("You have zero tasks assigned to your name.\n")
        return
    print("-" * 50)

    # Call the recursive task selection input engine.
    selected_id = get_valid_task_number(user_tasks, len(user_tasks))
    if selected_id == -1:
        return

    global_target = user_tasks[selected_id]
    target_task = tasks[global_target]

    print("\nOptions:\n1 - Mark task as complete\n2 - Edit task parameters")
    action = input("Select action (1/2): ").strip()

    if action == "1":
        target_task[5] = "Yes"
        save_tasks(tasks)
        print("Success: Task status updated to Completed.\n")
        
    elif action == "2":
        # Block edits if the selected task is already marked completed.
        if target_task[5] == "Yes":
            print("Error: You cannot modify a finalized task.\n")
            return
            
        print("\nEditing Options:\n1 - Reassign owner\n2 - Alter due date")
        edit_choice = input("Select field to mutate (1/2): ").strip()
        
        if edit_choice == "1":
            new_owner = input("Enter new owner username: ").strip()
            target_task[0] = new_owner
            save_tasks(tasks)
            print("Success: Ownership modified.\n")
        elif edit_choice == "2":
            new_date = input("Enter new due date: ").strip()
            target_task[4] = new_date
            save_tasks(tasks)
            print("Success: Due date extended.\n")
        else:
            print("Invalid alteration parameter selected.")


# ==============================================================================
# 3. ADMINISTRATIVE / REPORTING MODULES
# ==============================================================================

def view_completed():
    """Administrative tool showing complete tracking lists."""
    print("\n=== ARCHIVE: COMPLETED TASKS ===")
    tasks = load_tasks()
    found = False
    
    for t in tasks:
        if t[5] == "Yes":
            found = True
            print(f"[{t[0]}] finalized tracking element: '{t[1]}'")
            
    if not found:
        print("No completed records found.")
    print()


def delete_task():
    """Administrative deletion engine clearing structural records directly."""
    print("\n=== SYSTEM DATA MUTATION: DELETE TASK ===")
    tasks = load_tasks()
    
    if not tasks:
        print("Database holds nothing to target.\n")
        return

    for idx, t in enumerate(tasks):
        print(f"Index [{idx}] | User: {t[0]} | Title: {t[1]}")

    selection = input("\nEnter index number to delete (or press Enter to cancel): ").strip()
    
    if selection.isdigit() and int(selection) < len(tasks):
        removed = tasks.pop(int(selection))
        save_tasks(tasks)
        print(f"Purged record: {removed[1]} successfully.\n")
    else:
        print("Invalid selection. Aborted tracking adjustments.\n")


def generate_reports():
    """Generates explicit structural text summaries tracking project health.

    Outputs metrics directly to task_overview.txt and user_overview.txt.
    """
    users = load_users()
    tasks = load_tasks()
    
    total_tasks = len(tasks)
    completed_count = sum(1 for t in tasks if t[5] == "Yes")
    incomplete_count = total_tasks - completed_count
    
    overdue_count = 0
    today = datetime.date.today()
    
    for t in tasks:
        if t[5] == "No":
            try:
                due = datetime.datetime.strptime(t[4], "%d %b %Y").date()
                if due < today:
                    overdue_count += 1
            except ValueError:
                pass 

    # Calculate overall task stats.
    pct_incomplete = (incomplete_count / total_tasks * 100) if total_tasks > 0 else 0
    pct_overdue = (overdue_count / total_tasks * 100) if total_tasks > 0 else 0

    # Write metrics out into task_overview.txt file format.
    with open("task_overview.txt", "w") as f:
        f.write("=========================================\n")
        f.write("             TASK OVERVIEW REPORT        \n")
        f.write("=========================================\n")
        f.write(f"Total tasks logged:               {total_tasks}\n")
        f.write(f"Completed tasks total:            {completed_count}\n")
        f.write(f"Incomplete tasks remaining:       {incomplete_count}\n")
        f.write(f"Overdue uncompleted total:        {overdue_count}\n")
        f.write(f"Percentage remaining incomplete:  {pct_incomplete:.1f}%\n")
        f.write(f"Percentage logged overdue:        {pct_overdue:.1f}%\n")

    # Generate individual data arrays for user_overview.txt file.
    with open("user_overview.txt", "w") as f:
        f.write("=========================================\n")
        f.write("             USER OVERVIEW REPORT        \n")
        f.write("=========================================\n")
        f.write(f"Total system registered users:     {len(users)}\n")
        f.write(f"Total tracked systemic tasks:      {total_tasks}\n\n")
        
        for user in users:
            user_tasks = [t for t in tasks if t[0] == user]
            u_total = len(user_tasks)
            u_done = sum(1 for t in user_tasks if t[5] == "Yes")
            u_open = u_total - u_done
            
            u_overdue = 0
            for t in user_tasks:
                if t[5] == "No":
                    try:
                        due = datetime.datetime.strptime(t[4], "%d %b %Y").date()
                        if due < today:
                            u_overdue += 1
                    except ValueError:
                        pass
            
            pct_assigned = (u_total / total_tasks * 100) if total_tasks > 0 else 0
            pct_u_done = (u_done / u_total * 100) if u_total > 0 else 0
            pct_u_open = (u_open / u_total * 100) if u_total > 0 else 0
            pct_u_over = (u_overdue / u_total * 100) if u_total > 0 else 0
            
            f.write(f"--- User Core metrics: [{user}] ---\n")
            f.write(f" Total tasks assigned:            {u_total}\n")
            f.write(f" % Share of global load:          {pct_assigned:.1f}%\n")
            f.write(f" % Status completed successfully: {pct_u_done:.1f}%\n")
            f.write(f" % Active status remaining open:  {pct_u_open:.1f}%\n")
            f.write(f" % Left uncompleted and overdue:  {pct_u_over:.1f}%\n\n")
            
    print("Success: Statistical reports output to disk files natively.\n")


def display_statistics():
    """Displays dashboard report metrics extracted from generated files."""
    print("\n=== CONSOLE REPORT METRIC STREAM ===")
    
    # Defensive programming step checking file existence status.
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports()

    print("\n--- TASK FILE METRICS ---")
    with open("task_overview.txt", "r") as f:
        print(f.read())
        
    print("\n--- USER FILE METRICS ---")
    with open("user_overview.txt", "r") as f:
        print(f.read())


# ==============================================================================
# 4. INITIALIZATION AND ACCESS SEQUENCE
# ==============================================================================

def login_sequence():
    """Loops matching login interface checking parameters until validated.

    Returns:
        str: The string username validated against local systems.
    """
    print("=========================================")
    print("      TASK MANAGER     ")
    print("=========================================")
    user_details = load_users()
    
    while True:
        username = input("Enter system user handle: ").strip()
        password = input("Enter secure access code: ").strip()
        
        if username in user_details and user_details[username] == password:
            print(f"\nWelcome back, {username}. Authority mapping granted.\n")
            return username
        
        print("Access Denied: Invalid credentials provided.\n")


# Start the application session by handling access verification.
current_user = login_sequence()

while True:
    # Route available selections dynamically depending on the current user status.
    if current_user == "admin":
        menu = input('''Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete a task
gr - generate reports
ds - display statistics
e - exit
: ''').strip().lower()
    else:
        menu = input('''Please select one of the following options:
a - add task
va - view all tasks
vm - view my tasks
e - exit
: ''').strip().lower()

    # Route programmatic inputs to their respective functionality engines.
    if menu == 'r' and current_user == "admin":
        reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(current_user)
    elif menu == 'vc' and current_user == "admin":
        view_completed()
    elif menu == 'del' and current_user == "admin":
        delete_task()
    elif menu == 'gr' and current_user == "admin":
        generate_reports()
    elif menu == 'ds' and current_user == "admin":
        display_statistics()
    elif menu == 'e':
        print('Exiting control terminal. Goodbye!!!')
        break
    else:
        print("\nInvalid choice or execution parameter missing from selection.\n")