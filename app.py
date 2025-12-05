import psycopg2        # PostgreSQL database adapter for Python
import time            # Used to delay execution while PostgreSQL container initializes


# ----------------------------------------------------------
# FUNCTION: get_connection()
# PURPOSE: Create and return a new connection to PostgreSQL
# ----------------------------------------------------------
def get_connection():
    """
    Establish a connection to the PostgreSQL database.

    IMPORTANT:
    These values must match the PostgreSQL container settings
    (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB, and the container --name).
    """
    return psycopg2.connect(
        host="my-postgres",     # Container name of PostgreSQL (acts like hostname)
        database="studentdb",   # Database name created inside PostgreSQL
        user="student_user",    # PostgreSQL username
        password="student_pass" # PostgreSQL password
    )


# ----------------------------------------------------------
# FUNCTION: verify_connection()
# PURPOSE: Check if the DB connection works by running a test query
# ----------------------------------------------------------
def verify_connection(conn):
    """
    Run a simple SQL query (SELECT 1) to verify the connection.
    If the result is (1,), the connection is working correctly.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        return result == (1,)   # True if connection works


# ----------------------------------------------------------
# FUNCTION: create_students_table()
# PURPOSE: Create the "students" table if it does not exist
# ----------------------------------------------------------
def create_students_table(conn):
    """Create the students table if it does not already exist."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        roll_number VARCHAR(20) UNIQUE,
        name VARCHAR(100) NOT NULL,
        course VARCHAR(100),
        year INTEGER
    );
    """
    with conn.cursor() as cur:
        cur.execute(create_table_query)


# ----------------------------------------------------------
# FUNCTION: insert_student()
# PURPOSE: Insert ONE student record into the table
# ----------------------------------------------------------
def insert_student(conn, roll_number, name, course, year):
    """
    Insert a single student into the students table.

    ON CONFLICT (roll_number) DO NOTHING:
    - Prevents duplicate roll numbers
    - If the roll number already exists, the insert is skipped
    """
    insert_query = """
    INSERT INTO students (roll_number, name, course, year)
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (roll_number) DO NOTHING;
    """
    with conn.cursor() as cur:
        cur.execute(insert_query, (roll_number, name, course, year))


# ----------------------------------------------------------
# FUNCTION: get_all_students()
# PURPOSE: Retrieve all student records
# ----------------------------------------------------------
def get_all_students(conn):
    """Return all student records as a list of tuples."""
    select_query = """
    SELECT id, roll_number, name, course, year
    FROM students
    ORDER BY id;
    """
    with conn.cursor() as cur:
        cur.execute(select_query)
        return cur.fetchall()


# ----------------------------------------------------------
# FUNCTION: get_student_count()
# PURPOSE: Count total students in the table
# ----------------------------------------------------------
def get_student_count(conn):
    """Retrieve the total number of students in the system."""
    count_query = "SELECT COUNT(*) FROM students;"
    with conn.cursor() as cur:
        cur.execute(count_query)
        return cur.fetchone()[0]   # Return only the number, not a tuple


# ----------------------------------------------------------
# FUNCTION: print_students_table()
# PURPOSE: Print all students in a clean, formatted table
# ----------------------------------------------------------
def print_students_table(students):
    """Print students in a nicely formatted table."""

    if not students:   # If list is empty
        print("No students found.")
        return

    # Table headings
    headers = ("ID", "Roll No", "Name", "Course", "Year")

    # Dynamically compute column widths based on longest value
    col_widths = [len(h) for h in headers]
    for row in students:
        for i, value in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(value)))

    # Create a function to format a single row
    def format_row(row_vals):
        return " | ".join(str(v).ljust(col_widths[i]) for i, v in enumerate(row_vals))

    # Separator line (-----+-----+-----)
    separator = "-+-".join("-" * w for w in col_widths)

    # Print header and rows
    print(separator)
    print(format_row(headers))
    print(separator)
    for row in students:
        print(format_row(row))
    print(separator)


# ----------------------------------------------------------
# MAIN PROGRAM
# ----------------------------------------------------------
def main():
    conn = None  # Will hold the database connection object

    try:
        # Step 1: Give PostgreSQL time to start
        print("Waiting for PostgreSQL to be ready...")
        time.sleep(5)

        # Step 2: Connect to PostgreSQL
        print("Connecting to PostgreSQL...")
        conn = get_connection()
        print("Connection established successfully.")
        print("Connected to the database!")

        # Step 3: Verify connection is working
        if verify_connection(conn):
            print("Connection verification successful.")
        else:
            print("Connection verification FAILED. Exiting program.")
            return

        # Step 4: Create table
        create_students_table(conn)
        print("Students table is ready.")

        # Step 5: Insert a student based on user input
        print("\nEnter new student details:")

        roll_number = input("Enter Roll Number: ").strip()
        name = input("Enter Name: ").strip()
        course = input("Enter Course: ").strip()

        # Convert year into integer safely
        while True:
            try:
                year = int(input("Enter Year (1/2/3/4): "))
                break
            except ValueError:
                print("Invalid year! Please enter a number such as 1, 2, 3, or 4.")

        # Now insert the student
        insert_student(conn, roll_number, name, course, year)
        print("New student record inserted successfully.")

        # Step 6: Count students
        student_count = get_student_count(conn)
        print(f"Total students in system: {student_count}")

        # Step 7: Fetch and display all students
        students = get_all_students(conn)
        print("\nStudent List:")
        print_students_table(students)

        # Step 8: Save changes to the database
        conn.commit()
        print("Changes committed successfully.")

    except Exception as e:
        # Catches ALL possible errors (SQL errors, connection issues, etc.)
        print("An error occurred:", e)
        if conn is not None:
            conn.rollback()   # Undo uncommitted changes
            print("Transaction rolled back due to error.")
    finally:
        # Step 9: Clean up database connection
        if conn is not None:
            try:
                conn.close()
                print("Database connection closed.")
            except Exception as e:
                print("Error when closing the connection:", e)


# Entry point of the Python program
if __name__ == "__main__":
    main()
