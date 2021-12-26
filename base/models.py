from django.db import models
from django.contrib.auth import get_user_model
import factory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger


class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('email', 'username')

    username = factory.Faker("name")
    email = factory.Faker("email")
    password = factory.PostGenerationMethodCall('set_password', 'test12345')
    
    def __str__(self) -> str:
        return self.username + " - " + self.email


class Teacher(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="user_teacher")
    name = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name
    

class TeacherFactory(DjangoModelFactory):
    class Meta:
        model = Teacher

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    
    def __str__(self) -> str:
        return self.name

class Student(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name="user_student")
    name = models.CharField(max_length=100)
    roll = models.IntegerField()
    age = models.IntegerField()
    
    def __str__(self) -> str:
        return self.name
    
class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("name")
    roll = factory.Sequence(lambda n: n)
    age = FuzzyInteger(18, 80)
    
    def __str__(self) -> str:
        return self.name