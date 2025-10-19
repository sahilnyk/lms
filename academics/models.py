from django.conf import settings
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    students = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="Enrollment", related_name="courses", blank=True
    )

    def __str__(self):
        return self.title

    def enroll(self, user):
        Enrollment.objects.get_or_create(student=user, course=self)

    def is_enrolled(self, user):
        return self.enrollments.filter(student=user).exists()

    def enrollment_date_for(self, user):
        return self.enrollments.filter(student=user).values_list("enrolled_at", flat=True).first()

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.title

# optional
class LessonChecklistItem(models.Model):
    lesson = models.ForeignKey(Lesson, related_name="checklist", on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    position = models.PositiveSmallIntegerField("Position", null=True, blank=True)

    class Meta:
        ordering = ["position", "id"]

    def __str__(self):
        return self.text

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="enrollments", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="enrollments", on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ("-enrolled_at",)

    def __str__(self):
        return f"{self.student} -> {self.course} at {self.enrolled_at}"
