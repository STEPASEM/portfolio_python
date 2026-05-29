from django.shortcuts import render
from django.db import connection
from django.db.models import Avg, Count, Min, Max, Q
from .models import Course, Student, StudentCourse


def index(request):
    """Главная страница"""
    return render(request, 'registry/index.html')


def courses_list(request):
    """Список курсов"""
    courses = Course.objects.all().order_by('course_name')
    return render(request, 'registry/courses/list.html', {'courses': courses})


def students_list(request):
    """Список студентов"""
    students = Student.objects.all().order_by('last_name')
    return render(request, 'registry/students/list.html', {'students': students})


def enrollments_list(request):
    """Список записей (журнал)"""
    enrollments = StudentCourse.objects.select_related('student', 'course').all()
    return render(request, 'registry/enrollments/list.html', {'enrollments': enrollments})


# ========== OLAP-КУБ ==========

def olap_index(request):
    """Страница OLAP-куба"""
    with connection.cursor() as cursor:
        # Список курсов для выпадающего списка
        cursor.execute("SELECT id, course_name FROM courses ORDER BY course_name")
        courses = cursor.fetchall()

        # Список студентов для выпадающего списка
        cursor.execute("SELECT id, first_name || ' ' || last_name FROM students ORDER BY last_name")
        students = cursor.fetchall()

    return render(request, 'registry/olap/index.html', {
        'courses': courses,
        'students': students,
    })


def olap_query(request):
    """Обработка OLAP-запросов"""
    view_type = request.GET.get('view', '')
    course_id = request.GET.get('courseId', '')
    student_id = request.GET.get('studentId', '')

    queries = {
        'rollup_course': """
            SELECT 
                c.course_name AS "Курс",
                COUNT(*) AS "Записей",
                ROUND(AVG(sc.grade)::numeric, 2) AS "Средний балл",
                MIN(sc.grade) AS "Мин. балл",
                MAX(sc.grade) AS "Макс. балл"
            FROM student_courses sc
            JOIN courses c ON sc.course_id = c.id
            GROUP BY c.id, c.course_name
            ORDER BY "Средний балл" DESC
        """,

        'rollup_student': """
            SELECT 
                (s.first_name || ' ' || s.last_name) AS "Студент",
                COUNT(*) AS "Курсов",
                ROUND(AVG(sc.grade)::numeric, 2) AS "Средний балл",
                MIN(sc.grade) AS "Мин. балл",
                MAX(sc.grade) AS "Макс. балл"
            FROM student_courses sc
            JOIN students s ON sc.student_id = s.id
            GROUP BY s.id, s.first_name, s.last_name
            ORDER BY "Средний балл" DESC
        """,

        'rollup_year': """
            SELECT 
                EXTRACT(YEAR FROM sc.enrollment_date)::int AS "Год",
                COUNT(*) AS "Записей",
                ROUND(AVG(sc.grade)::numeric, 2) AS "Средний балл"
            FROM student_courses sc
            GROUP BY EXTRACT(YEAR FROM sc.enrollment_date)
            ORDER BY "Год"
        """,

        'cube_course_student': """
            SELECT 
                c.course_name AS "Курс",
                (s.first_name || ' ' || s.last_name) AS "Студент",
                sc.grade AS "Оценка",
                sc.enrollment_date AS "Дата записи"
            FROM student_courses sc
            JOIN courses c ON sc.course_id = c.id
            JOIN students s ON sc.student_id = s.id
            ORDER BY c.course_name, s.last_name
        """
    }

    # Срезы (slice)
    if view_type == 'slice_course' and course_id:
        queries['slice_course'] = f"""
            SELECT 
                (s.first_name || ' ' || s.last_name) AS "Студент",
                sc.grade AS "Оценка",
                sc.enrollment_date AS "Дата записи"
            FROM student_courses sc
            JOIN students s ON sc.student_id = s.id
            WHERE sc.course_id = {course_id}
            ORDER BY sc.grade DESC
        """
    elif view_type == 'slice_student' and student_id:
        queries['slice_student'] = f"""
            SELECT 
                c.course_name AS "Курс",
                sc.grade AS "Оценка",
                sc.enrollment_date AS "Дата записи"
            FROM student_courses sc
            JOIN courses c ON sc.course_id = c.id
            WHERE sc.student_id = {student_id}
            ORDER BY c.course_name
        """

    titles = {
        'rollup_course': '📊 Roll-up: Сводка по курсам',
        'rollup_student': '📊 Roll-up: Сводка по студентам',
        'rollup_year': '📊 Roll-up: Сводка по годам',
        'slice_course': '✂️ Срез: Студенты на выбранном курсе',
        'slice_student': '✂️ Срез: Курсы выбранного студента',
        'cube_course_student': '📐 Таблица: Курс × Студент'
    }

    sql = queries.get(view_type, '')
    title = titles.get(view_type, 'Результат запроса')

    rows = []
    columns = []

    if sql:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            rows = cursor.fetchall()

    return render(request, 'registry/olap/result.html', {
        'title': title,
        'columns': columns,
        'rows': rows,
        'view_type': view_type,
    })