from django.db import models

# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

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
