from django.conf import settings
from django.db import models
from django.db.models import Count, Q, Avg
from decimal import Decimal
from ckeditor.fields import RichTextField

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    end_date = models.DateField(null=True, blank=True, verbose_name="End Date")
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="teaching_courses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Teacher"
    )
    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        through="Enrollment", 
        related_name="courses", 
        blank=True,
        verbose_name="Students"
    )

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["title"]

    def __str__(self):
        return self.title

    def enroll(self, user):
        Enrollment.objects.get_or_create(student=user, course=self)

    def is_enrolled(self, user):
        return self.enrollments.filter(student=user).exists()

    def get_progress_for_student(self, student):
        total_lessons = self.lessons.count()
        if total_lessons == 0:
            return Decimal('0.00')
        
        completed_lessons = self.lessons.filter(is_done=True).count()
        
        return Decimal(str(round((completed_lessons / total_lessons) * 100, 2)))

    def get_completion_status(self, student):
        lessons = self.lessons.all()
        total = lessons.count()
        
        if total == 0:
            return {
                'total': 0,
                'completed': 0,
                'percentage': Decimal('0.00'),
                'is_complete': False
            }
        
        completed = lessons.filter(is_done=True).count()
        percentage = Decimal(str(round((completed / total) * 100, 2)))
        
        return {
            'total': total,
            'completed': completed,
            'percentage': percentage,
            'is_complete': completed == total
        }


class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = RichTextField(blank=True)
    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)
    is_done = models.BooleanField(default=False)
    scheduled_date = models.DateField(null=True, blank=True, verbose_name="Scheduled Date")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "Lesson"
        verbose_name_plural = "Lessons"

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        for enrollment in self.course.enrollments.all():
            old_progress = enrollment.calculate_progress()
            enrollment.update_completion_status()

    def get_average_progress(self):
        enrolled_students = self.course.students.all()
        if not enrolled_students.exists():
            return Decimal('0.00')
        
        completed_count = LessonProgress.objects.filter(
            lesson=self,
            completed=True,
            student__in=enrolled_students
        ).count()
        
        return Decimal(str(round((completed_count / enrolled_students.count()) * 100, 2)))


class LessonChecklistItem(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="checklist", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    class Meta:
        ordering = ["position", "id"]
        verbose_name = "Lesson Checklist"
        verbose_name_plural = "Lesson Checklists"

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        total = self.lesson.checklist.count()
        completed = self.lesson.checklist.filter(completed=True).count()
        
        if total > 0 and completed == total:
            self.lesson.is_done = True
            self.lesson.save()
        elif completed < total and self.lesson.is_done:
            self.lesson.is_done = False
            self.lesson.save()


class Enrollment(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name="enrollments", 
        on_delete=models.CASCADE,
        verbose_name="Student"
    )
    course = models.ForeignKey(
        Course, 
        related_name="enrollments", 
        on_delete=models.CASCADE,
        verbose_name="Course"
    )
    enrolled_at = models.DateTimeField(auto_now_add=True, verbose_name="Enrolled At")
    completed = models.BooleanField(default=False, verbose_name="Completed")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")

    class Meta:
        unique_together = ("student", "course")
        ordering = ("-enrolled_at",)
        verbose_name = "Student Enrollment"
        verbose_name_plural = "Student Enrollments"

    def __str__(self):
        return f"{self.student} -> {self.course}"

    def calculate_progress(self):
        total_lessons = self.course.lessons.count()
        if total_lessons == 0:
            return Decimal('0.00')
        
        completed_lessons = self.course.lessons.filter(is_done=True).count()
        
        return Decimal(str(round((completed_lessons / total_lessons) * 100, 2)))

    def update_completion_status(self):
        from django.utils import timezone
        
        total = self.course.lessons.count()
        if total == 0:
            return
        
        completed = self.course.lessons.filter(is_done=True).count()
        
        if completed == total and not self.completed:
            self.completed = True
            self.completed_at = timezone.now()
            self.save()
        elif completed < total and self.completed:
            self.completed = False
            self.completed_at = None
            self.save()


class LessonProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="lesson_progress",
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        Lesson,
        related_name="student_progress",
        on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "lesson")
        verbose_name = "Lesson Progress"
        verbose_name_plural = "Lesson Progress"
        ordering = ["lesson__position"]

    def __str__(self):
        status = "Complete" if self.completed else "Incomplete"
        return f"{self.student} - {self.lesson.title} - {status}"

    def get_progress_percentage(self):
        return Decimal('100.00') if self.completed else Decimal('0.00')

    def save(self, *args, **kwargs):
        if self.completed and not self.completed_at:
            from django.utils import timezone
            self.completed_at = timezone.now()
        elif not self.completed:
            self.completed_at = None
        
        super().save(*args, **kwargs)
        
        try:
            enrollment = Enrollment.objects.get(
                student=self.student,
                course=self.lesson.course
            )
            enrollment.update_completion_status()
        except Enrollment.DoesNotExist:
            pass
