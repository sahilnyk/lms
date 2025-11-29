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
    verbose_name = "Student Enrollment"
    verbose_name_plural = "Student Enrollments"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
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
        
        # Teacher field - limit to Teachers group
        try:
            teachers_qs = Group.objects.get(name="Teachers").user_set.all()
        except Group.DoesNotExist:
            teachers_qs = User.objects.all()
        self.fields["teacher"].queryset = teachers_qs
        self.fields["teacher"].label = "Assign Teacher"
        self.fields["teacher"].help_text = "Select a teacher from the Teachers group to assign to this course."

        # Set students_to_add queryset to Students group
        try:
            students_qs = Group.objects.get(name="Students").user_set.all()
        except Group.DoesNotExist:
            students_qs = User.objects.all()
        self.fields["students_to_add"].queryset = students_qs

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("title", "teacher", "created", "lesson_count", "student_count")
    search_fields = ("title", "description", "teacher__username", "teacher__first_name", "teacher__last_name")
    list_filter = (HasLessonsFilter, "created", "teacher")
    list_per_page = 10
    ordering = ("-created",)
    inlines = [LessonInline, EnrollmentInline]
    
    fieldsets = (
        ("Course Information", {
            "fields": ("title", "description")
        }),
        ("Teacher Assignment", {
            "fields": ("teacher",),
            "description": "Assign a teacher from the Teachers group to this course."
        }),
        ("Student Enrollment", {
            "fields": ("students_to_add", "enroll_all"),
            "classes": ("collapse",),
            "description": "Manually enroll students or enroll all students at once."
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        # Save course first
        super().save_model(request, obj, form, change)

        # Handle student enrollment
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
        return qs.annotate(
            _lesson_count=Count("lessons", distinct=True),
            _student_count=Count("enrollments", distinct=True)
        )

    def lesson_count(self, obj):
        return getattr(obj, "_lesson_count", obj.lessons.count())
    lesson_count.short_description = "Lessons"
    lesson_count.admin_order_field = "_lesson_count"

    def student_count(self, obj):
        return getattr(obj, "_student_count", obj.enrollments.count())
    student_count.short_description = "Students"
    student_count.admin_order_field = "_student_count"

class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "position", "is_done")
    search_fields = ("title", "content", "course__title")
    list_filter = ("course", "is_done")
    list_select_related = ("course",)
    list_per_page = 10
    ordering = ("course", "position")
    inlines = [ChecklistInline]

class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrolled_at")
    search_fields = ("student__username", "student__first_name", "student__last_name", "course__title")
    list_filter = ("enrolled_at", "course")
    list_select_related = ("student", "course")
    readonly_fields = ("enrolled_at",)
    list_per_page = 25  # Pagination
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            try:
                kwargs["queryset"] = Group.objects.get(name="Students").user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class TeacherAssignedAdmin(admin.ModelAdmin):
    """
    Admin view to see all courses assigned to teachers
    """
    list_display = ("course_title", "teacher_name", "student_count", "lesson_count", "created")
    search_fields = ("title", "description", "teacher__username", "teacher__first_name", "teacher__last_name")
    list_filter = ("teacher", "created")
    list_select_related = ("teacher",)
    list_per_page = 25  # Pagination
    ordering = ("-created",)
    
    def has_add_permission(self, request):
        # No adding from this view - use Course admin
        return False
    
    def has_delete_permission(self, request, obj=None):
        # No deleting from this view - use Course admin
        return False
    
    def get_queryset(self, request):
        qs = Course.objects.filter(teacher__isnull=False).annotate(
            _lesson_count=Count("lessons", distinct=True),
            _student_count=Count("enrollments", distinct=True)
        )
        return qs
    
    def course_title(self, obj):
        return obj.title
    course_title.short_description = "Course"
    course_title.admin_order_field = "title"
    
    def teacher_name(self, obj):
        if obj.teacher:
            return f"{obj.teacher.get_full_name() or obj.teacher.username}"
        return "-"
    teacher_name.short_description = "Teacher"
    teacher_name.admin_order_field = "teacher__username"
    
    def student_count(self, obj):
        return getattr(obj, "_student_count", 0)
    student_count.short_description = "Students"
    student_count.admin_order_field = "_student_count"
    
    def lesson_count(self, obj):
        return getattr(obj, "_lesson_count", 0)
    lesson_count.short_description = "Lessons"
    lesson_count.admin_order_field = "_lesson_count"

# Register models
admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonChecklistItem)

# Register with custom names
class EnrollmentAdminProxy(Enrollment):
    class Meta:
        proxy = True
        verbose_name = "Student Enrollment"
        verbose_name_plural = "Student Enrollments"

class TeacherAssignedProxy(Course):
    class Meta:
        proxy = True
        verbose_name = "Teacher Assignment"
        verbose_name_plural = "Teacher Assigned"

admin.site.register(EnrollmentAdminProxy, StudentEnrollmentAdmin)
admin.site.register(TeacherAssignedProxy, TeacherAssignedAdmin)
