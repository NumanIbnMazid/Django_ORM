from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import Teacher, Student
import time
from django.db.models import Count, Q, F, Sum, Avg, Max, Min
# to view raw sql query
from django.db import connection

def user_teacher_and_student_list(request):
    # to view raw sql query
    queries = []
    
    # all users
    # method 1
    t1 = time.time()
    users_q1 = get_user_model().objects.all()
    t2 = time.time()
    queries.append(
        {
            "sql": users_q1.query,
            "queryString": "get_user_model().objects.all()",
            "time": t2 - t1,
            "data": users_q1
        },
    )
    # method 2
    t1 = time.time()
    users_q2 = get_user_model().objects.all().values_list('id', 'username', 'email')
    t2 = time.time()
    queries.append(
        {
            "title": "Values List",
            "sql": users_q2.query,
            "queryString": "get_user_model().objects.all().values_list('id', 'username', 'email')",
            "time": t2 - t1,
            "data": users_q2
        },
    )
    
    # union all teacher's and student's names
    notes = "The UNION operator is used to combine the result-set of two or more querysets. The querysets can be from the same or from different models. When they querysets are from different models, the fields and their datatypes should match."
    t1 = time.time()
    student_teacher_names = Teacher.objects.all().values_list('name').union(Student.objects.all().values_list( 'name'))
    t2 = time.time()
    queries.append(
        {
            "title": "Union",
            "notes": notes,
            "sql": student_teacher_names.query,
            "queryString": "Teacher.objects.all().values_list('name').union(Student.objects.all().values_list( 'name'))",
            "time": t2 - t1,
            "data": student_teacher_names
        },
    )
    
    # intersection all teacher's and student's names
    t1 = time.time()
    student_teacher_names = Teacher.objects.all().values_list('name').intersection(Student.objects.all().values_list( 'name'))
    t2 = time.time()
    queries.append(
        {
            "title": "Intersection",
            "notes": None,
            "sql": student_teacher_names.query,
            "queryString": "Teacher.objects.all().values_list('name').intersection(Student.objects.all().values_list( 'name'))",
            "time": t2 - t1,
            "data": student_teacher_names
        },
    )
    
    # Aggregate
    t1 = time.time()
    qs = get_user_model().objects.aggregate(total_users=Count('id'))
    t2 = time.time()
    queries.append(
        {
            "title": "Aggregate",
            "notes": None,
            "sql": None,
            "queryString": "get_user_model().objects.aggregate(total_users=Count('id'))",
            "time": t2 - t1,
            "data": qs
        },
    )
    
    # Annotate
    notes = """
    To perform group by in ORM style, we have to use the two methods values and annotate as follows:
    values(<col>): Mention the fields for what to group by
    annotate(<aggr function>): Mention what to aggregate using functions such as SUM, COUNT, MAX, MIN, and AVG
    """
    t1 = time.time()
    qs = get_user_model().objects.values('is_staff').annotate(user_count=Count('*'))
    t2 = time.time()
    queries.append(
        {
            "title": "Annotate",
            "notes": notes,
            "sql": qs.query,
            "queryString": "get_user_model().objects.values('is_staff').annotate(user_count=Count('*'))",
            "time": t2 - t1,
            "data": qs
        },
    )
    
    # Multiple aggregations
    notes = """
    For multiple aggregations, we need to add multiple fields by which you want to group. 
    In the below example, we have executed a query group by columns (is_active, is_staff)
    """
    t1 = time.time()
    qs = get_user_model().objects.values("is_active", "is_staff").annotate(user_count = Count("*"))
    t2 = time.time()
    queries.append(
        {
            "title": "Multiple aggregations",
            "notes": notes,
            "sql": qs.query,
            "queryString": "get_user_model().objects.values('is_active', 'is_staff').annotate(user_count = Count('*'))",
            "time": t2 - t1,
            "data": qs
        },
    )
    
    # HAVING clause
    notes = """
    The HAVING clause is used to filter groups. In the below query, I have filtered the group which has a count greater than one:
    """
    t1 = time.time()
    qs = get_user_model().objects.values("is_staff").annotate(user_count=Count("*")).filter(user_count__gt = 1)
    t2 = time.time()
    queries.append(
        {
            "title": "HAVING clause",
            "notes": notes,
            "sql": qs.query,
            "queryString": 'get_user_model().objects.values("is_staff").annotate(user_count=Count("*")).filter(user_count__gt = 1)',
            "time": t2 - t1,
            "data": qs
        },
    )
    
    # teachers = Teacher.objects.all()
    # for i, t in enumerate(teachers):
    #     t.user.email = t.user.email.replace("@", "@teacher_")
    #     print(f"updating teacher {i}...")
    #     t.user.save()
    # students = Student.objects.all()
    # for i, s in enumerate(students):
    #     s.user.email = s.user.email.replace("@", "@student_")
    #     print(f"updating student {i}...")
    #     s.user.save()
    context = {
        "queries": queries
    }
    return render(request, 'orm_view.html', context=context)
