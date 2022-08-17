from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from apps.server.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student
)
from apps.server.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel
)

router = APIRouter()


# get => "/students/"
@router.get("/", response_description="Getting students")
async def get_students():
    try:
        students = await retrieve_students()
        
        if students:
            return ResponseModel(students, "Students data returned successfully")
        return ResponseModel(students, "Empty list")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student was no added")
    

# post => "/students/"
@router.post("/", response_description="Student data added into the database")
async def add_students(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    
    try:
        new_student = await add_student(student)
        return ResponseModel(new_student, "Student added successfully")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student was not added")


# get => "/students/:id"
@router.get("/{id}", response_description="Student data retrieved")
async def get_student(id):
    try:
        student = await retrieve_student(id)
        
        if student:
            return ResponseModel(student, "Students data retrieved")
        
        return ErrorResponseModel("Student does not exist", 404, "no student")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student was not find")
    

# put => "/students/:id"
@router.put("/{id}")
async def update_students(id:str, req: UpdateStudentModel = Body(...)):
    
    req = { k: v for k, v in req.dict().items if v is not None }

    student = await retrieve_student(id)
    
    try:
        if student:
            updated_student =  await update_student(id, req)

            return ResponseModel(updated_student, "Student updated")
        
        return ErrorResponseModel("Student does not exist", 404, "no student")
    
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student was not updated")

# delete => "/students/:id"
@router.delete("/{id}", response_description="Student data deleted from database")
async def delete_student(id: str):
    try:
        student = await retrieve_student(id)
        if student:
            deleted_student = await delete_student(id)
            
            if deleted_student:
                return ResponseModel("Student with Id: {} removed".format(id), "Student deleted successfully")
            return ErrorResponseModel(Exception, 500, "Student was not deleted")
        return ErrorResponseModel("Student does not exist", 404, "no student")
    except Exception:
        return ErrorResponseModel(Exception, 500, "Student was not deleted")
