import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = "mongodb://top_gun_lab:Topgunlab321@cluster0-shard-00-00.0o62b.mongodb.net:27017,cluster0-shard-00-01.0o62b.mongodb.net:27017,cluster0-shard-00-02.0o62b.mongodb.net:27017/?ssl=true&replicaSet=atlas-cxhbd1-shard-0&authSource=admin&retryWrites=true&w=majority"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.students

student_collection = database.get_collection("students_collection")

# helper student
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study" : student["course_of_study"],
        "year": student["year"],
        "gpa": student["gpa"],
    }

# Crud

# recuperar todos los alumnos de la db
# get => "/students"
async def retrieve_students() -> list:
    students = []
    async for student in student_collection.find():
        student.append(student_helper(student))
    return students

# Agregar nuevo estudiando a la db
#post => "/students"
async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({"_id": student.inserted_id})
    
    return student_helper(new_student)

# recuperar un alumno de la db
# get => "/students/:id"
async def retrieve_student(id: str) -> dict:
    student = await student_collection.find_one({"_id": ObjectId(id)})

    if student:
        return student_helper(student)

# actualizar un alumno de la db
# put => "/students/:id"
async def update_student(id: str, data: dict) -> dict:

    if len(data) < 1:
        return False
    
    student = await student_collection.find_one({"_id": ObjectId(id)})

    if student:
        updated_student = await student_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )

        if updated_student:
            return True
        return False

# eliminar un alumno de la db
# delete => "/students/:id"
async def delete_student(id: str):
    student = await student_collection.find_one({"_id": ObjectId(id)})

    if student:
        await student_collection.delete_one({"_id": ObjectId(id)})
        return True
