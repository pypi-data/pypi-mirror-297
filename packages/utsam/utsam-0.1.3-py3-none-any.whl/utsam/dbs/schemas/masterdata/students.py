from dataclasses import dataclass

@dataclass
class PgStudentsTable:
    name: str = "students"
    student_id: str = 'student_id'
    canvas_student_id: str = 'canvas_student_id'
    student_name: str = 'student_name'
    student_email: str = 'staff_id'
    student_status: str = 'staff_id'
