from django.db import models
from django.utils import timezone
import datetime

# Модель для курсов
class Course(models.Model):
    course_name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(verbose_name="Описание", blank=True, null=True)
    credits = models.IntegerField(verbose_name="Кредиты")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата создания")

    class Meta:
        db_table = 'courses'
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['course_name']

    def __str__(self):
        return self.course_name


# Модель для студентов
class Student(models.Model):
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(max_length=100, unique=True, verbose_name="Email")
    birth_date = models.DateField(verbose_name="Дата рождения")
    enrollment_date = models.DateField(default=datetime.date.today, verbose_name="Дата зачисления")

    class Meta:
        db_table = 'students'
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


# Модель для связи студент-курс (оценки)
class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Студент")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс")
    grade = models.DecimalField(max_digits=3, decimal_places=2, verbose_name="Оценка")
    enrollment_date = models.DateField(default=datetime.date.today, verbose_name="Дата записи")

    class Meta:
        db_table = 'student_courses'
        verbose_name = "Запись на курс"
        verbose_name_plural = "Записи на курсы"
        ordering = ['-enrollment_date']
        constraints = [
            models.CheckConstraint(
                condition=models.Q(grade__gte=0) & models.Q(grade__lte=5),
                name="grade_between_0_and_5"
            ),
            models.UniqueConstraint(
                fields=["student", "course"],
                name="unique_student_course"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.course}: {self.grade}"