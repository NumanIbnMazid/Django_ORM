from django.contrib.auth import get_user_model
import random

from django.db import transaction
from django.core.management.base import BaseCommand
from base.models import (
    UserFactory,
    Teacher, TeacherFactory,
    Student, StudentFactory,
)

NUM_USERS = 1000
NUM_TEACHERS = 1000
NUM_STUDENTS = 1000

DEFAULT_NUM_OF_DATA = 7


class Command(BaseCommand):
    help = "Generates test data"

    def _delete_old_data(self):
        models = [
            get_user_model(), Teacher, Student
        ]

        self.stdout.write("Deleting old data...")
        for m in models:
            m.objects.all().delete()

    def _create_admin_users(self):
        self.stdout.write("Creating admin users...")
        # Default Users
        if not get_user_model().objects.filter(email__iexact='admin@admin.com').exists():
            u_admin = get_user_model()(email='admin@admin.com', username='admin')
            u_admin.set_password("admin")
            u_admin.is_staff = True
            u_admin.is_superuser = True
            u_admin.save()

    def _create_new_data(self):
        self.stdout.write("Creating new data...")
        # users
        self._create_users_data()
        # teachers
        self._create_teachers_data()
        # students
        self._create_students_data()

    def _create_users_data(self):
        self.stdout.write("Creating users...")
        
        def user_factory():
            try:
                user = UserFactory()
                return user
            except:
                print("******* Exception Occurs: Retrying... *******")
                user_factory()
        
        # Create all the users
        users = []
        for _ in range(NUM_USERS):
            self.stdout.write(f"Creating user: {_ + 1}")
            user = user_factory()
            self.stdout.write(f"ok: Created user: {user}")
            users.append(user)

    def _create_teachers_data(self):
        self.stdout.write("Creating teachers...")
        
        def teacher_factory():
            try:
                teacher = TeacherFactory()
                return teacher
            except:
                print("******* Exception Occurs: Retrying... *******")
                teacher_factory()
        
        # Create all the users
        teachers = []
        for _ in range(NUM_TEACHERS):
            self.stdout.write(f"Creating teachers: {_ + 1}")
            teacher = teacher_factory()
            self.stdout.write(f"ok: Created teacher: {teacher}")
            teachers.append(teacher)

    def _create_students_data(self):
        self.stdout.write("Creating students...")
        
        def student_factory():
            try:
                student = StudentFactory()
                return student
            except:
                print("******* Exception Occurs: Retrying... *******")
                student_factory()
                
        # Create all the users
        students = []
        for _ in range(NUM_STUDENTS):
            self.stdout.write(f"Creating students: {_ + 1}")
            student = student_factory()
            self.stdout.write(f"ok: Created student: {student}")
            students.append(student)

    @transaction.atomic
    def handle(self, *args, **kwargs):
        # delete old data
        self._delete_old_data()
        # create admin users
        self._create_admin_users()
        # create new data
        self._create_new_data()
