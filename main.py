from dotenv import load_dotenv
load_dotenv()
import os 


from fastapi import FastAPI
from pydantic import BaseModel
from database import get_db_connection


app = FastAPI()


class StudentCreate(BaseModel):
    name: str
    age: int

@app.get("/debug")
def debug():
    return {
        "host": os.getenv("DB_HOST"),
        "name": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT"),
    }
@app.get("/")
def read_root():
    return {"Hello": "Este es otro servicio"}
@app.get("/students")
def read_students():
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM students")
        
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        students = [dict(zip(columns, row)) for row in rows]
        
        cursor.close()
        db.close()
        return {"students": students}
    except Exception as e:
        return {"error": str(e)}
    
@app.post("/students")
def create_student(student: StudentCreate):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO students (name, age) VALUES (%s, %s) RETURNING id",
            (student.name, student.age)
        )
        student_id = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        return {"id": student_id, "name": student.name, "age": student.age}
    except Exception as e:
        return {"error": str(e)}
    