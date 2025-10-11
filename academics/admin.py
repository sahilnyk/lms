from django.contrib import admin
from django.db.models import Count
from .models import Course, Lesson, LessonChecklistItem
from grappelli.forms import GrappelliSortableHiddenMixin

class LessonInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Lesson
    fields = ("title", "is_done", "position")
    extra = 1
    sortable_field_name = "position"

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]


class ChecklistInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = LessonChecklistItem
    fields = ("text", "completed", "position")
    extra = 1
    sortable_field_name = "position"

class HasLessonsFilter(admin.SimpleListFilter):
    title = "has lessons"
    parameter_name = "has_lessons"

    def lookups(self, request, model_admin):
        return (("yes", "Has lessons"), ("no", "No lessons"))

    def queryset(self, request, queryset):
        val = self.value()
        if val == "yes":
            return queryset.annotate(_cnt=Count("lessons")).filter(_cnt__gt=0)
        if val == "no":
            return queryset.annotate(_cnt=Count("lessons")).filter(_cnt__exact=0)
        return queryset

class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "created", "lesson_count")
    search_fields = ("title", "description")
    list_filter = (HasLessonsFilter, "created")
    list_per_page = 10
    ordering = ("-created",)
    inlines = [LessonInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_lesson_count=Count("lessons"))

    def lesson_count(self, obj):
        return getattr(obj, "_lesson_count", obj.lessons.count())
    lesson_count.short_description = "Lessons"

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "is_done")
    search_fields = ("title", "content", "course__title")
    list_filter = ("course", "is_done")
    list_select_related = ("course",)
    list_per_page = 10
    ordering = ("course", "position")
    inlines = [ChecklistInline]

    class Media:
        js = [
            "/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js",
            "/static/js/tinymce_setup.js",
        ]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonChecklistItem)
