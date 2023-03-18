# from ..utils import db
# # from enum import Enum
# class Student(db.Model):
#     __tablename__ = 'student'
#     id = db.Column(db.Integer(), primary_key=True)
#     full_name = db.Column(db.String(45), nullable=False, unique=True)
#     email = db.Column(db.String(50), nullable=False, unique=True)
#     password = db.Column(db.Text(), nullable=False)

#     def __repr__(self):
#         return f"<Student{self.full_name}>"

#     def save(self):
#         db.session.add(self)
#         db.session.commit()

#     @classmethod
#     def get_by_id(cls, id):
#         return cls.query.get_or_404(id)



from .users import User
from ..utils import db

class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    matric_no = db.Column(db.String(30), unique=True)
    course = db.relationship('Course', secondary='student_course', lazy=True)
    grade = db.relationship('Grade', backref='student_grade', lazy=True)

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def __repr__(self):
        return f"<Student {self.matric_no}>"
        
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)