from django.contrib import admin
from django.db.models import Count, Q
from django.utils.html import format_html
from .models import Course, Lesson, LessonChecklistItem, Enrollment, LessonProgress
from grappelli.forms import GrappelliSortableHiddenMixin
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    fields = ("student", "completed", "completed_at", "last_accessed")
    readonly_fields = ("completed_at", "last_accessed")
    extra = 0
    can_delete = False

class LessonInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = Lesson
    fields = ("position", "title", "is_done", "scheduled_date")
    extra = 1
    sortable_field_name = "position"
    ordering = ["position"]

class ChecklistInline(GrappelliSortableHiddenMixin, admin.TabularInline):
    model = LessonChecklistItem
    fields = ("position", "text", "completed")
    extra = 1
    sortable_field_name = "position"
    ordering = ["position"]

class EnrollmentInline(admin.TabularInline):
    model = Enrollment
    fields = ("student", "enrolled_at", "progress_display", "completed")
    readonly_fields = ("enrolled_at", "progress_display")
    extra = 1
    verbose_name = "Student Enrollment"
    verbose_name_plural = "Student Enrollments"

    def progress_display(self, obj):
        if obj.pk:
            percentage = float(obj.calculate_progress())
            if percentage == 100:
                color = "#4caf50"
            elif percentage >= 50:
                color = "#ff9800"
            else:
                color = "#f44336"
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}</span>',
                color, str(round(percentage, 2)) + '%'
            )
        return "-"
    progress_display.short_description = "Progress"

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
        widget=admin.widgets.FilteredSelectMultiple("Students", is_stacked=False),
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
        self.fields["teacher"].label = "Assign Teacher"
        self.fields["teacher"].help_text = "Select a teacher from the Teachers group to assign to this course."

        try:
            students_qs = Group.objects.get(name="Students").user_set.all()
        except Group.DoesNotExist:
            students_qs = User.objects.all()
        self.fields["students_to_add"].queryset = students_qs

class CourseAdmin(admin.ModelAdmin):
    form = CourseAdminForm
    list_display = ("title", "teacher", "start_date", "end_date", "created", "lesson_count", "student_count", "avg_completion")
    search_fields = ("title", "description", "teacher__username", "teacher__first_name", "teacher__last_name")
    list_filter = (HasLessonsFilter, "created", "teacher", "start_date", "end_date")
    list_per_page = 10
    ordering = ("title",)
    inlines = [LessonInline, EnrollmentInline]
    
    fieldsets = (
        ("Course Information", {
            "fields": ("title", "description"),
        }),
        ("Schedule & Timing", {
            "fields": ("start_date", "end_date"),
        }),
        ("Teacher Assignment", {
            "fields": ("teacher",),
        }),
        ("Student Enrollment", {
            "fields": ("students_to_add", "enroll_all"),
            "classes": ("collapse",),
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

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

    def avg_completion(self, obj):
        enrollments = obj.enrollments.all()
        if not enrollments:
            return "-"
        
        total_progress = sum(float(e.calculate_progress()) for e in enrollments)
        avg = total_progress / enrollments.count()
        
        if avg == 100:
            color = "#4caf50"
        elif avg >= 50:
            color = "#ff9800"
        else:
            color = "#f44336"
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, str(round(avg, 2)) + '%'
        )
    avg_completion.short_description = "Avg Progress"

class LessonAdmin(admin.ModelAdmin):
    list_display = ("position", "title", "course", "is_done", "scheduled_date", "completion_rate")
    list_editable = ("is_done",)
    search_fields = ("title", "content", "course__title")
    list_filter = ("course", "is_done", "scheduled_date")
    list_select_related = ("course",)
    list_per_page = 50
    ordering = ("course__title", "position")
    inlines = [ChecklistInline]
    
    fieldsets = (
        ("Lesson Information", {
            "fields": ("course", "title", "content", "position"),
        }),
        ("Status & Schedule", {
            "fields": ("is_done", "scheduled_date"),
        }),
    )

    def completion_rate(self, obj):
        total_enrolled = obj.course.enrollments.count()
        if total_enrolled == 0:
            return "-"
        
        completed = LessonProgress.objects.filter(
            lesson=obj,
            completed=True
        ).count()
        
        percentage = round((completed / total_enrolled) * 100, 2)
        
        if percentage == 100:
            color = "#4caf50"
        elif percentage >= 50:
            color = "#ff9800"
        else:
            color = "#f44336"
        
        return format_html(
            '<span style="color: {};">{}/{} ({})</span>',
            color, completed, total_enrolled, str(percentage) + '%'
        )
    completion_rate.short_description = "Completion"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "course":
            kwargs["queryset"] = Course.objects.all().order_by('title')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class LessonChecklistForm(forms.ModelForm):
    class Meta:
        model = LessonChecklistItem
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['lesson'].queryset = Lesson.objects.select_related('course').order_by('course__title', 'position')
        self.fields['lesson'].label_from_instance = lambda obj: f"{obj.course.title} - {obj.title}"

class LessonChecklistAdmin(admin.ModelAdmin):
    form = LessonChecklistForm
    list_display = ("position", "text", "lesson", "course_name", "completed")
    list_editable = ("completed",)
    search_fields = ("text", "lesson__title", "lesson__course__title")
    list_filter = ("completed", "lesson__course")
    list_select_related = ("lesson", "lesson__course")
    list_per_page = 50
    ordering = ("lesson__course__title", "lesson__position", "position")
    
    fieldsets = (
        ("Checklist Item Information", {
            "fields": ("lesson", "text", "position", "completed"),
        }),
    )
    
    def course_name(self, obj):
        return obj.lesson.course.title if obj.lesson else "-"
    course_name.short_description = "Course"
    course_name.admin_order_field = "lesson__course__title"

class StudentEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "progress_bar", "completed", "enrolled_at", "completed_at")
    search_fields = ("student__username", "student__first_name", "student__last_name", "course__title")
    list_filter = ("completed", "enrolled_at", "course")
    list_select_related = ("student", "course")
    readonly_fields = ("enrolled_at", "progress_bar", "completed_at")
    list_per_page = 50
    ordering = ("course__title", "student__username")
    
    fieldsets = (
        ("Enrollment Information", {
            "fields": ("student", "course", "enrolled_at"),
        }),
        ("Progress Tracking", {
            "fields": ("progress_bar", "completed", "completed_at"),
        }),
    )
    
    def progress_bar(self, obj):
        percentage = float(obj.calculate_progress())
        
        if percentage == 100:
            color = "#4caf50"
        elif percentage >= 50:
            color = "#ff9800"
        else:
            color = "#f44336"
        
        width_str = str(int(percentage))
        pct_str = str(round(percentage, 1))
        
        return format_html(
            '<div style="width:100px; background:#e0e0e0; border-radius:3px;">'
            '<div style="width:{}%; background:{}; height:20px; border-radius:3px; text-align:center; color:white; font-weight:bold; line-height:20px;">'
            '{}'
            '</div></div>',
            width_str, color, pct_str + '%'
        )
    progress_bar.short_description = "Progress"
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            try:
                kwargs["queryset"] = Group.objects.get(name="Students").user_set.all()
            except Group.DoesNotExist:
                kwargs["queryset"] = User.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class LessonProgressForm(forms.ModelForm):
    class Meta:
        model = LessonProgress
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['lesson'].queryset = Lesson.objects.select_related('course').order_by('course__title', 'position')
        self.fields['lesson'].label_from_instance = lambda obj: f"{obj.course.title} - {obj.title}"
        
        try:
            students_qs = Group.objects.get(name="Students").user_set.all()
        except Group.DoesNotExist:
            students_qs = User.objects.all()
        self.fields['student'].queryset = students_qs

class LessonProgressAdmin(admin.ModelAdmin):
    form = LessonProgressForm
    list_display = ("student", "lesson", "course_name", "completed_status", "completed_at", "last_accessed")
    search_fields = ("student__username", "student__first_name", "student__last_name", "lesson__title", "lesson__course__title")
    list_filter = ("completed", "lesson__course", "completed_at")
    list_select_related = ("student", "lesson", "lesson__course")
    readonly_fields = ("completed_at", "last_accessed")
    list_per_page = 50
    ordering = ("lesson__course__title", "lesson__position", "student__username")
    
    fieldsets = (
        ("Progress Tracking", {
            "fields": ("student", "lesson", "completed"),
        }),
        ("Timestamps", {
            "fields": ("completed_at", "last_accessed"),
            "classes": ("collapse",),
        }),
    )
    
    def course_name(self, obj):
        return obj.lesson.course.title
    course_name.short_description = "Course"
    course_name.admin_order_field = "lesson__course__title"
    
    def completed_status(self, obj):
        if obj.completed:
            return format_html('<span style="color: #4caf50; font-weight: bold;">Complete</span>')
        return format_html('<span style="color: #f44336;">Incomplete</span>')
    completed_status.short_description = "Status"

class TeacherAssignedAdmin(admin.ModelAdmin):
    list_display = ("course_title", "teacher_name", "start_date", "end_date", "student_count", "lesson_count", "avg_progress", "created")
    search_fields = ("title", "description", "teacher__username", "teacher__first_name", "teacher__last_name")
    list_filter = ("teacher", "created", "start_date", "end_date")
    list_select_related = ("teacher",)
    list_per_page = 25
    ordering = ("title",)
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
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

    def avg_progress(self, obj):
        enrollments = obj.enrollments.all()
        if not enrollments:
            return "-"
        
        total = sum(float(e.calculate_progress()) for e in enrollments)
        avg = total / enrollments.count()
        
        if avg == 100:
            color = "#4caf50"
        elif avg >= 50:
            color = "#ff9800"
        else:
            color = "#f44336"
            
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, str(round(avg, 2)) + '%'
        )
    avg_progress.short_description = "Avg Progress"

admin.site.register(Course, CourseAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonChecklistItem, LessonChecklistAdmin)
admin.site.register(LessonProgress, LessonProgressAdmin)

class EnrollmentAdminProxy(Enrollment):
    class Meta:
        proxy = True
        verbose_name = "Student Enrollment"
        verbose_name_plural = "Student Enrollments"

class TeacherAssignedProxy(Course):
    class Meta:
        proxy = True
        verbose_name = "Teacher Assignment"
        verbose_name_plural = "Teacher Assignments"

admin.site.register(EnrollmentAdminProxy, StudentEnrollmentAdmin)
admin.site.register(TeacherAssignedProxy, TeacherAssignedAdmin)
