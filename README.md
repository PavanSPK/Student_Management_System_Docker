# Student Management System in Docker (Python + PostgreSQL)

This project demonstrates how a Python application running inside Docker can communicate with a PostgreSQL database container. It performs basic student management operations:

- Creates a database table
- Accepts student details from the user
- Inserts a new student record
- Displays all students in a formatted table

-----------------------------------------------------------------------------------------------------

## 1. Project Overview

The setup uses two containers:

1. **PostgreSQL Container** – Stores student information.
2. **Python App Container** – Connects to PostgreSQL, accepts user input, performs INSERT + SELECT queries, and displays results.

Both containers communicate over a custom Docker network.

-----------------------------------------------------------------------------------------------------

## 2. Project Structure

```text
student-management-docker/
│── app.py
│── Dockerfile
│── README.md
│── screenshots/   
```

-----------------------------------------------------------------------------------------------------

## 3. Project Explanation

### **3.1 Database Connection**

```python
conn = psycopg2.connect(
    host="my-postgres",
    database="studentdb",
    user="student_user",
    password="student_pass"
)
```

**Explanation:**
* `host="my-postgres"` → must equal the PostgreSQL container name
* `studentdb`, `student_user`, `student_pass` → must match environment variables used when starting Postgres
* The Python container resolves `my-postgres` automatically because both containers share the same network

-----------------------------------------------------------------------------------------------------

### **3.2 Creating the Students Table**

```sql
CREATE TABLE IF NOT EXISTS students (
    id SERIAL PRIMARY KEY,
    roll_number VARCHAR(20) UNIQUE,
    name VARCHAR(100),
    course VARCHAR(100),
    year INTEGER
);
```

**Explanation:**
* `IF NOT EXISTS` prevents duplicate table creation
* `roll_number` is unique → avoids duplicate student entries
* `SERIAL` auto-increments `id`

-----------------------------------------------------------------------------------------------------

### **3.3 Inserting Student Data (User Input)**

```python
roll = input("Enter Roll Number: ")
name = input("Enter Name: ")
course = input("Enter Course: ")
year = int(input("Enter Year: "))

# SQL INSERT
INSERT INTO students (roll_number, name, course, year) 
VALUES (%s, %s, %s, %s);
```

**Explanation:**
* Python collects student information interactively
* Inserts exactly one record
* Later printed in a formatted table

-----------------------------------------------------------------------------------------------------

### **3.4 Displaying Data**

```sql
SELECT id, roll_number, name, course, year FROM students;
```

Printed using a custom formatting function:

```
ID | Roll No | Name      | Course  | Year
---------------------------------------
1  | S001    | Pavan     | DevOps  | 1
```

-----------------------------------------------------------------------------------------------------

## 4. Dockerfile (Essential Only)

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY app.py .
RUN pip install psycopg2-binary
CMD ["python", "app.py"]
```

**Explanation:**
* Uses lightweight Python base image
* Copies your app inside container
* Installs PostgreSQL driver
* Runs your script automatically

-----------------------------------------------------------------------------------------------------

## 5. Create Docker Network

```bash
docker network create student-network
```

**Why?** Allows Python container to resolve PostgreSQL by container name (`my-postgres`).

![network](https://github.com/PavanSPK/Student_Management_System_Docker/blob/f42e63d75fc513aaef77ba1b658b542a18137245/screenshots/network.png)

-----------------------------------------------------------------------------------------------------

## 6. Start PostgreSQL Container

```bash
docker run -d \
  --name my-postgres \
  --network student-network \
  -e POSTGRES_USER=student_user \
  -e POSTGRES_PASSWORD=student_pass \
  -e POSTGRES_DB=studentdb \
  postgres
```

**Explanation:**
* `--name my-postgres` → must match Python `host`
* Database automatically created at startup

![postgresl](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/postgres.png)

![ps](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/ps.png)

-----------------------------------------------------------------------------------------------------

## 7. Build Python App Image

```bash
docker build -t student-app .
```

![build](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/build.png)

### Images

![dockerimages](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/dockerimages.png)

-----------------------------------------------------------------------------------------------------

## 8. Run the App (Interactive mode required)

```bash
docker run -it --rm --network student-network student-app
```

### Sample Interaction

```
Enter Roll Number: 4
Enter Name: Kumar
Enter Course: DevOps
Enter Year: 3
```

![run](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/run.png)

-----------------------------------------------------------------------------------------------------

## 9. Push Image to Docker Hub

```bash
docker login
docker tag student-app yourusername/student-app:latest
docker push yourusername/student-app:latest
```

![dockerhubpush](https://github.com/PavanSPK/Student_Management_System_Docker/blob/cc417b79bbb103f6301b252ed8eab478ad0c7a8a/screenshots/dockerhubpush.png)

-----------------------------------------------------------------------------------------------------

## 10. Troubleshooting

### Error: *host "my-postgres" not found*
You did not attach Python container to the same network.

### Error: *password not specified*
PostgreSQL requires `POSTGRES_PASSWORD`.

### Error: *connection refused*
PostgreSQL container is still starting; run again after 3–5 seconds.

-----------------------------------------------------------------------------------------------------

## 11. Cleanup

```bash
docker rm -f my-postgres
docker network rm student-network
docker rmi student-app
```

-----------------------------------------------------------------------------------------------------

## 12. What This Project Teaches

* How Python connects to PostgreSQL inside Docker
* How Docker networks work
* How containers talk using hostnames
* How to Dockerize Python apps
* How to push custom Docker images to Docker Hub

-----------------------------------------------------------------------------------------------------

## Author
**PavanSPK**  
GitHub: [@PavanSPK](https://github.com/PavanSPK) 
