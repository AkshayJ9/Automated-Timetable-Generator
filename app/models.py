from django.db import models

class TimeTable(models.Model):
    department = models.CharField(max_length=100)
    division = models.CharField(max_length=10)
    second_year_subjects = models.JSONField(default=list)  # Use list for subjects
    third_year_subjects = models.JSONField(default=list)
    fourth_year_subjects = models.JSONField(default=list)
    lecture_start_time = models.TimeField()
    college_end_time = models.TimeField()
    sessions_per_day = models.IntegerField()
    max_lectures = models.IntegerField()
    max_practicals = models.IntegerField()
    recess_1_start = models.TimeField(null=True, blank=True)
    recess_1_end = models.TimeField(null=True, blank=True)
    short_recess_start = models.TimeField(null=True, blank=True)  # Added
    short_recess_end = models.TimeField(null=True, blank=True)

    second_year_timetable = models.JSONField(default=dict, blank=True)
    third_year_timetable = models.JSONField(default=dict, blank=True)
    fourth_year_timetable = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return f"{self.department} - {self.division}"


class TeacherSchedule(models.Model):
    teacher_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    time_slot = models.CharField(max_length=20)  # Example: "09:00-10:00"
    day = models.CharField(max_length=10)  # Monday, Tuesday, etc.
    department = models.CharField(max_length=100)
    division = models.CharField(max_length=10)
    year = models.CharField(max_length=20)  # Second Year, Third Year, Fourth Year

    def __str__(self):
        return f"{self.teacher_name} - {self.subject} - {self.time_slot} ({self.day})"
    
class UpdatedTeacherSchedule(models.Model):
    original_teacher = models.CharField(max_length=100)
    replacement_teacher = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100)
    practical = models.BooleanField(default=False)
    time_slot = models.CharField(max_length=50)
    day = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    division = models.CharField(max_length=10)
    year = models.CharField(max_length=20)  