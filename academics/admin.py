from django.contrib import admin
from django.db.models import Count
from .models import Course, Lesson, LessonChecklistItem, Enrollment
from grappelli.forms import GrappelliSortableHiddenMixin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

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

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    fields = ("student", "enrolled_at")
    readonly_fields = ("enrolled_at",)
    extra = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # limit the student dropdown to users in Group "Students" if it exists,
        # otherwise show all users. Keeps compatibility with default auth.
        if db_field.name == "student":
            from django.contrib.auth import get_user_model
            from django.contrib.auth.models import Group

            User = get_user_model()
            try:
                kwargs["queryset"] = Group.objects.get(name="Students").user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

class CourseAdminForm(forms.ModelForm):
    # dynamic queryset will be set in get_form()
    students_to_add = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Students to add (manual select)",
        help_text="Pick specific students to enroll in this course."
    )
    enroll_all = forms.BooleanField(
        required=False,
        label="Enroll all students",
        help_text='When checked, all users in the "Students" group (or all users) will be enrolled.'
    )

    class Meta:
        model = Course
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            teachers_qs = Group.objects.get(name="Teachers").user_set.all()
        except Group.DoesNotExist:
            teachers_qs = User.objects.all()
        self.fields["teacher"].queryset = teachers_qs

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("title", "created", "lesson_count")
    search_fields = ("title", "description")
    list_filter = (HasLessonsFilter, "created")
    list_per_page = 10
    ordering = ("-created",)
    inlines = [LessonInline, EnrollmentInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # set students_to_add queryset to Students group if present, else all users
        try:
            students_qs = Group.objects.get(name="Students").user_set.all()
        except Group.DoesNotExist:
            students_qs = User.objects.all()
        form.base_fields["students_to_add"].queryset = students_qs
        return form

    def save_model(self, request, obj, form, change):
        # save course first
        super().save_model(request, obj, form, change)

        # handle enroll all or manual selection
        try:
            enroll_all = form.cleaned_data.get("enroll_all")
            selected = form.cleaned_data.get("students_to_add") or []
        except Exception:
            enroll_all = False
            selected = []

        if enroll_all:
            try:
                students_qs = Group.objects.get(name="Students").user_set.all()
            except Group.DoesNotExist:
                students_qs = User.objects.all()
            for u in students_qs:
                Enrollment.objects.get_or_create(student=u, course=obj)
        else:
            for u in selected:
                Enrollment.objects.get_or_create(student=u, course=obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(_lesson_count=Count("lessons"))

    def lesson_count(self, obj):
        return getattr(obj, "_lesson_count", obj.lessons.count())
    lesson_count.short_description = "Lessons"

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "is_done")
    search_fields = ("title", "content", "course__title")
    list_filter = ("course", "is_done")
    list_select_related = ("course",)
    list_per_page = 10
    ordering = ("course", "position")
    inlines = [ChecklistInline]

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonChecklistItem)
admin.site.register(Enrollment)
