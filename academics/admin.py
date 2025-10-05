from django.contrib import admin
from .models import Course, Lesson, LessonChecklistItem
from grappelli.forms import GrappelliSortableHiddenMixin

class LessonInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Lesson
    fields = ("title", "is_done", "position")
    extra = 1
    sortable_field_name = "position"

class ChecklistInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = LessonChecklistItem
    fields = ("text", "completed", "position")
    extra = 1
    sortable_field_name = "position"

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created")
    inlines = [LessonInline]

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "is_done")
    inlines = [ChecklistInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonChecklistItem)
