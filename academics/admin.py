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
    teachers_to_assign = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Teachers", is_stacked=False),
        label="Teachers (assign using dual-list)",
        help_text="Select teachers to assign to this course. The first selected teacher will be set as the primary teacher."
    )
    
    students_to_add = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        widget=admin.widgets.FilteredSelectMultiple("Students", is_stacked=False),
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
        self.fields["teachers_to_assign"].queryset = teachers_qs
        
        # Pre-populate if teacher already assigned
        if self.instance.pk and self.instance.teacher:
            self.fields["teachers_to_assign"].initial = [self.instance.teacher.pk]

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
    ordering = ("-created",)
    inlines = [LessonInline, EnrollmentInline]
    
    fieldsets = (
        ("Course Information", {
            "fields": ("title", "description"),
        }),
        ("Schedule & Timing", {
            "fields": ("start_date", "end_date"),
        }),
        ("Teacher Assignment", {
            "fields": ("teachers_to_assign",),
        }),
        ("Student Enrollment", {
            "fields": ("students_to_add", "enroll_all"),
            "classes": ("collapse",),
        }),
    )

    def save_model(self, request, obj, form, change):
        # Handle teacher assignment
        teachers_to_assign = form.cleaned_data.get("teachers_to_assign")
        if teachers_to_assign:
            # Set first selected teacher as primary teacher
            obj.teacher = teachers_to_assign[0]
        
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
    list_display = ("title", "course", "scheduled_date", "position", "is_done", "completion_rate")
    search_fields = ("title", "content", "course__title")
    list_filter = ("course", "is_done", "scheduled_date")
    list_select_related = ("course",)
    list_per_page = 10
    ordering = ("course", "position")
    inlines = [ChecklistInline]
    
    fieldsets = (
        ("Lesson Information", {
            "fields": ("course", "title", "content"),
        }),
        ("Scheduling", {
            "fields": ("scheduled_date", "position"),
        }),
        ("Status", {
            "fields": ("is_done",),
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

class LessonChecklistForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label="Course (optional)",
        help_text="Select a course to filter lessons. If selected, only lessons from this course will appear in the lesson dropdown."
    )
    
    class Meta:
        model = LessonChecklistItem
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk and self.instance.lesson:
            self.fields['course'].initial = self.instance.lesson.course
        
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lesson'].queryset = Lesson.objects.filter(course_id=course_id).order_by('position')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.lesson:
            self.fields['lesson'].queryset = Lesson.objects.filter(course=self.instance.lesson.course).order_by('position')

class LessonChecklistAdmin(admin.ModelAdmin):
    form = LessonChecklistForm
    list_display = ("text", "lesson", "course_name", "completed", "position")
    search_fields = ("text", "lesson__title", "lesson__course__title")
    list_filter = ("completed", "lesson__course")
    list_select_related = ("lesson", "lesson__course")
    list_per_page = 25
    ordering = ("lesson__course", "lesson__position", "position")
    
    fieldsets = (
        ("Checklist Item Information", {
            "fields": ("course", "lesson", "text", "completed"),
        }),
        ("Ordering", {
            "fields": ("position",),
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
    list_per_page = 25
    
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
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        required=False,
        label="Course (optional)",
        help_text="Select a course to filter lessons and students."
    )
    
    students_to_add = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        required=False,
        label="Students (manual select)",
        help_text="Select specific students to track progress."
    )
    
    add_all_students = forms.BooleanField(
        required=False,
        label="Add all enrolled students",
        help_text="Automatically add all students enrolled in the selected course."
    )
    
    mark_all_complete = forms.BooleanField(
        required=False,
        label="Mark all lessons complete",
        help_text="Mark all lessons in the selected course as complete for the selected students."
    )
    
    class Meta:
        model = LessonProgress
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk and self.instance.lesson:
            self.fields['course'].initial = self.instance.lesson.course
        
        try:
            students_qs = Group.objects.get(name="Students").user_set.all()
        except Group.DoesNotExist:
            students_qs = User.objects.all()
        self.fields['students_to_add'].queryset = students_qs
        
        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lesson'].queryset = Lesson.objects.filter(course_id=course_id).order_by('position')
                self.fields['student'].queryset = User.objects.filter(enrollments__course_id=course_id).distinct()
                self.fields['students_to_add'].queryset = User.objects.filter(enrollments__course_id=course_id).distinct()
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.lesson:
            self.fields['lesson'].queryset = Lesson.objects.filter(course=self.instance.lesson.course).order_by('position')

class LessonProgressAdmin(admin.ModelAdmin):
    form = LessonProgressForm
    list_display = ("student", "lesson", "course_name", "completed_status", "completed_at", "last_accessed")
    search_fields = ("student__username", "student__first_name", "student__last_name", "lesson__title", "lesson__course__title")
    list_filter = ("completed", "lesson__course", "completed_at")
    list_select_related = ("student", "lesson", "lesson__course")
    readonly_fields = ("completed_at", "last_accessed")
    list_per_page = 50
    
    fieldsets = (
        ("Progress Tracking Setup", {
            "fields": ("course",),
        }),
        ("Student Selection", {
            "fields": ("student", "students_to_add", "add_all_students"),
        }),
        ("Lesson & Completion", {
            "fields": ("lesson", "completed", "mark_all_complete"),
        }),
        ("Timestamps", {
            "fields": ("completed_at", "last_accessed"),
            "classes": ("collapse",),
        }),
    )
    
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        add_all = form.cleaned_data.get('add_all_students', False)
        mark_all = form.cleaned_data.get('mark_all_complete', False)
        selected_students = form.cleaned_data.get('students_to_add', [])
        course = form.cleaned_data.get('course')
        
        students_to_process = []
        
        if add_all and obj.lesson:
            students_to_process = list(obj.lesson.course.students.all())
        elif selected_students:
            students_to_process = list(selected_students)
        
        if students_to_process and obj.lesson:
            if mark_all:
                course_to_use = course or obj.lesson.course
                for student in students_to_process:
                    for lesson in course_to_use.lessons.all():
                        LessonProgress.objects.update_or_create(
                            student=student,
                            lesson=lesson,
                            defaults={'completed': True}
                        )
            else:
                for student in students_to_process:
                    LessonProgress.objects.get_or_create(
                        student=student,
                        lesson=obj.lesson,
                        defaults={'completed': obj.completed}
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
    ordering = ("-created",)
    
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
