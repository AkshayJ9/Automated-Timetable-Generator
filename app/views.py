from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import json
from django.http import JsonResponse
import os
from datetime import timedelta
import re
import google.generativeai as genai
# Create your views here.
def index(request):    
    return render(request,'index.html')

def create_table(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            TimeTable.objects.create(
                department=data.get("department"),
                division=data.get("division"),
                second_year_subjects=data.get("secondYearSubjects", []),
                third_year_subjects=data.get("thirdYearSubjects", []),
                fourth_year_subjects=data.get("fourthYearSubjects", []),
                lecture_start_time=data.get("lectureStartTime"),
                college_end_time=data.get("collegeEndTime"),
                sessions_per_day=int(data.get("sessionsPerDay", 0)),
                max_lectures=int(data.get("maxLectures", 0)),
                max_practicals=int(data.get("maxPracticals", 0)),
                recess_1_start=data.get("recess1Start") or None,
                recess_1_end=data.get("recess1End") or None,
                short_recess_start=data.get("shortRecessStart") or None,  # Added
                short_recess_end=data.get("shortRecessEnd") or None,
            )

            return JsonResponse({"message": "Timetable stored successfully!"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return render(request, "create_table.html")


# Configure AI API
os.environ['GOOGLE_API_KEY'] = "AIzaSyDDw4i32pQfN9gRlRAI5JFEg-hzjzlIpLI"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
model = genai.GenerativeModel('gemini-2.0-flash')

def generate_timetable(department, division, subjects, start_time, end_time,
                       recess_start, recess_end, short_recess_start, short_recess_end,
                       sessions_per_day):
    """
    Generate a structured college timetable with:
    - No consecutive duplicate lectures.
    - Teachers only handle one practical/day per year.
    - No overlapping teacher assignments.
    - Practical sessions are 2-hour blocks.
    - No empty slots.
    - Alternating practicals for batches A1 to A4 daily.
    """

    prompt = f"""
Generate a college timetable for {department} department, division {division}.
Working hours: {start_time} to {end_time} with {sessions_per_day} sessions/day.
Recess: {recess_start} to {recess_end}.
Short recess: {short_recess_start} to {short_recess_end}.

Subjects and teachers (JSON):
{json.dumps(subjects)}

Constraints:
1. No subject repeats consecutively on same day.
2. Each teacher handles only one practical per day per year.
3. No teacher overlap across divisions or batches simultaneously.
4. Practical sessions must be 2-hour continuous slots.
5. No empty slots; fill all sessions.
6. Practical slots split into 4 batches (A1 to A4) with different subjects each day, rotating during the week.
7. Format practicals like:
   A1 - Subject (Teacher) [Lab]
   A2 - Subject (Teacher) [Lab]
   A3 - Subject (Teacher) [Lab]
   A4 - Subject (Teacher) [Lab]

Return format (exactly):
Time Slot | Monday | Tuesday | Wednesday | Thursday | Friday
09:00-10:00 | Subject1 (Teacher A) | Subject2 (Teacher B) | ... | ... | ...
10:00-11:00 | Practical1 (Teacher A) | Subject6 (Teacher B) | ... | ... | ...
11:00-11:40 | Recess | Recess | Recess | Recess | Recess
11:40-12:40 | Subject7 (Teacher C) | Practical2 (Teacher D) | ... | ... | ...
12:40-13:40 | Subject8 (Teacher E) | Subject9 (Teacher F) | ... | ... | ...
13:40-13:50 | Short Recess | Short Recess | Short Recess | Short Recess | Short Recess
13:50-14:50 | Practical3 (Teacher G) | Subject10 (Teacher H) | ... | ... | ...
14:50-15:50 | Practical3 (Teacher G) | Subject11 (Teacher I) | ... | ... | ...
"""

    response = model.generate_content(prompt)
    return response.text if response else "Error generating timetable"

import re

import re
def extract_practical_subjects(timetable_obj, year_field):
    """
    Extracts practical subjects from a given year of the timetable.
    Returns a dictionary like:
    {
        "IoT": {"teacher": "Akash", "lab": "iot"},
        "SPOS": {"teacher": "Pooja", "lab": "spos"},
        ...
    }
    """
    subject_data = getattr(timetable_obj, year_field, [])
    practical_map = {}
    for subj in subject_data:
        if subj.get("hasPractical") and subj.get("lab"):
            subject = subj["name"]
            practical_map[subject] = {
                "teacher": subj["teacher"],
                "lab": subj["lab"]
            }
    return practical_map

def process_timetable_data(raw_timetable, recess_start="11:00", recess_end="11:40", 
                           short_recess_start="13:40", short_recess_end="13:50",
                           practicals_info=None):  # 🔸 new argument

    expected_time_slots = [
        "09:00-10:00", "10:00-11:00",
        f"{recess_start}-{recess_end}",
        "11:40-12:40", "12:40-13:40",
        f"{short_recess_start}-{short_recess_end}",
        "13:50-14:50", "14:50-15:50",
    ]

    rows = raw_timetable.strip().split("\n")

    daywise_sessions = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
    ai_time_slots = []

    for row in rows:
        columns = [col.strip() for col in row.split("|") if col.strip()]
        if len(columns) == 6:
            ai_time_slots.append(columns[0])
            for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
                daywise_sessions[day].append(columns[i+1])

    formatted_timetable = []
    for slot in expected_time_slots:
        if slot == f"{recess_start}-{recess_end}":
            formatted_timetable.append([slot] + ["Recess"]*5)
        elif slot == f"{short_recess_start}-{short_recess_end}":
            formatted_timetable.append([slot] + ["Short Recess"]*5)
        elif slot in ai_time_slots:
            idx = ai_time_slots.index(slot)
            row = [slot] + [daywise_sessions[day][idx] for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]
            formatted_timetable.append(row)
        else:
            formatted_timetable.append([slot] + ["-"]*5)

    # === Practical Subject Injection ===
    # === Practical Subject Injection ===
# Time slots to update
        last_two_slots = ["13:50-14:50", "14:50-15:50"]

        for row in formatted_timetable:
            if row[0] in last_two_slots and practicals_info:
                for day_idx, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
                    if day in practicals_info:
                        batch_list = sorted(practicals_info[day], key=lambda x: x['batch'])
                        combined_str = " ".join(
                            f"{entry['batch']} - {entry['subject']} ({entry['teacher']}) [{entry['lab']}]"
                            for entry in batch_list
                        )
                        row[day_idx + 1] = combined_str



    return {"merged": formatted_timetable}




def generate_full_timetable_for_all_years(department, division, second_year_subjects, third_year_subjects, fourth_year_subjects, start_time, end_time, recess_start, recess_end, short_recess_start, short_recess_end, sessions_per_day):
    """
    Generate timetable for Second Year, Third Year, and Fourth Year and ensure no slots are left empty.
    """
    # Generate timetable for all three years
    generated_timetables = {}

    for year, subjects_list in {"Second Year": second_year_subjects, "Third Year": third_year_subjects, "Fourth Year": fourth_year_subjects}.items():
        raw_timetable = generate_timetable(
            department, division, subjects_list, start_time, end_time, 
            recess_start, recess_end, short_recess_start, short_recess_end, sessions_per_day
        )

        # Process the raw timetable data to ensure it's structured and no empty slots
        structured_timetable = process_timetable_data(
            raw_timetable, recess_start, recess_end, short_recess_start, short_recess_end
        )
        
        generated_timetables[year] = structured_timetable  # Store structured timetable for each year
    
    return generated_timetables

def show_time_table(request):
    """
    Fetch all timetables from the database, generate a new one if requested, 
    store them separately without modifying existing timetables, 
    and format them for structured display.
    """
    timetables = TimeTable.objects.all().order_by('id')  # Ensure timetables are displayed in order of creation
    formatted_timetables = []

    assigned_teachers = {}  # Track assigned teachers across all divisions and years

    for table in timetables:
        start_time = table.lecture_start_time.strftime("%H:%M")
        end_time = table.college_end_time.strftime("%H:%M")
        recess_start = table.recess_1_start.strftime("%H:%M") if table.recess_1_start else None
        recess_end = table.recess_1_end.strftime("%H:%M") if table.recess_1_end else None
        short_recess_start = table.short_recess_start.strftime("%H:%M") if table.short_recess_start else None
        short_recess_end = table.short_recess_end.strftime("%H:%M") if table.short_recess_end else None

        yearwise_timetable = {}

        # Generate a new timetable only if required
        if not table.second_year_timetable or not table.third_year_timetable or not table.fourth_year_timetable:
            generated_timetables = generate_full_timetable_for_all_years(
                table.department, table.division,
                table.second_year_subjects, table.third_year_subjects, table.fourth_year_subjects,
                start_time, end_time, recess_start, recess_end, short_recess_start, short_recess_end,
                table.sessions_per_day
            )

            # Save new timetable separately without overwriting existing ones
            table.second_year_timetable = generated_timetables["Second Year"]
            table.third_year_timetable = generated_timetables["Third Year"]
            table.fourth_year_timetable = generated_timetables["Fourth Year"]
            table.save()
        
        # Store existing timetables (ensuring all divisions are shown)
        yearwise_timetable["Second Year"] = table.second_year_timetable
        yearwise_timetable["Third Year"] = table.third_year_timetable
        yearwise_timetable["Fourth Year"] = table.fourth_year_timetable

        # Store teacher schedules separately for each division
        for year, timetable_data in yearwise_timetable.items():
            store_teacher_schedule(timetable_data, table.department, table.division, year)

        # Append each timetable separately to be displayed
        formatted_timetables.append({
            "department": table.department,
            "division": table.division,
            "yearwise_timetable": yearwise_timetable,
        })

    return render(request, "show_time_table.html", {"timetables": formatted_timetables})



def view_time_table(request):
    timetables = TimeTable.objects.all()

    formatted_timetables = []
    for table in timetables:
        formatted_timetables.append({
            "department": table.department,
            "division": table.division,
            "yearwise_timetable": {
                "Second Year": table.second_year_timetable,  # Stored as list
                "Third Year": table.third_year_timetable,
                "Fourth Year": table.fourth_year_timetable,
            },
        })

    return render(request, "view_time_table.html", {"timetables": formatted_timetables})

def log_in(request):
    if request.method == "POST":
       username = request.POST['username']
       password = request.POST['password']

       if username == "user@gmail.com" and password == "user":
            messages.success(request, "Log In Successful!")
            return redirect("dashboard")
       else:
            messages.error(request, "Invalid Username or Password.")
            return redirect("log_in")

    return render(request, "log_in.html")


def dashboard(request):
    return render(request,"dashboard.html")

def log_out(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("/")


def store_teacher_schedule(timetable_data, department, division, year):
    """
    Extract teachers, subjects, and time slots from the timetable and store them separately.
    """
    TeacherSchedule.objects.filter(department=department, division=division, year=year).delete()  # Remove old data

    for row in timetable_data.get("merged", []):
        time_slot = row[0]  # First column is the time slot
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

        for i, day in enumerate(days):
            entry = row[i + 1]
            if entry and entry != "Recess" and entry != "-":  # Skip recess and empty slots
                if "(" in entry:
                    subject, teacher = entry.rsplit("(", 1)
                    teacher = teacher.replace(")", "").strip()
                else:
                    subject, teacher = entry.strip(), "Unknown"

                TeacherSchedule.objects.create(
                    teacher_name=teacher,
                    subject=subject.strip(),
                    time_slot=time_slot,
                    day=day,
                    department=department,
                    division=division,
                    year=year,
                )

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import TeacherSchedule, UpdatedTeacherSchedule

TEACHER_EMAILS = {
    "Kedar": "kedarhemade@gmail.com",
    "Sujal": "drjsarang@gmail.com",
    "Hitesh": "kothmirehitesh.1219@gmail.com",
    "Vidya": "hemadekedar@gmail.com",
    "Anjali": "kedarhemade@gmail.com",
}

# Load AI model
genai.configure(api_key="AIzaSyDDw4i32pQfN9gRlRAI5JFEg-hzjzlIpLI")

def view_teacher_schedule(request):
    teacher_schedules = TeacherSchedule.objects.all()
    years = ["Second Year", "Third Year", "Fourth Year"]

    if request.method == "POST":
        absent_teacher = request.POST.get("absent_teacher")
        day = request.POST.get("day")

        if absent_teacher and day:
            absent_teacher_lectures = TeacherSchedule.objects.filter(
                teacher_name=absent_teacher, day=day
            ).exclude(subject="Short Recess")

            if not absent_teacher_lectures:
                messages.error(request, f"No lectures found for {absent_teacher} on {day}.")
                return redirect("view_teacher_schedule")

            for lecture in absent_teacher_lectures:
                time_slot = lecture.time_slot
                department = lecture.department
                division = lecture.division
                year = lecture.year

                # Find a free teacher
                free_teacher = TeacherSchedule.objects.exclude(
                    teacher_name=absent_teacher
                ).filter(
                    day=day
                ).exclude(
                    time_slot=time_slot
                ).exclude(
                    subject="Short Recess"
                ).exclude(
                    teacher_name__in=TeacherSchedule.objects.filter(
                        time_slot=time_slot,
                        day=day
                    ).values_list("teacher_name", flat=True)
                ).first()

                if free_teacher:
                    UpdatedTeacherSchedule.objects.create(
                        original_teacher=absent_teacher,
                        replacement_teacher=free_teacher.teacher_name,
                        subject=lecture.subject,
                        time_slot=time_slot,
                        day=day,
                        department=department,
                        division=division,
                        year=year
                    )
                    print(f"Replacement teacher: {free_teacher.teacher_name}")
                    print(f"Email: {TEACHER_EMAILS.get(free_teacher.teacher_name)}")


                    # ✅ Check if teacher name is in email list and send email
                    replacement_email = TEACHER_EMAILS.get(free_teacher.teacher_name.capitalize())
                    if replacement_email:
                        try:
                            send_mail(
                                subject='Lecture Assignment',
                                message=(
                                    f"Dear {free_teacher.teacher_name},\n\n"
                                    f"You have been assigned a lecture for subject '{lecture.subject}' "
                                    f"on {day} at {time_slot} as a replacement for {absent_teacher}.\n\n"
                                    "Please be available.\n\nRegards,\nAdmin"
                                ),
                                from_email=settings.DEFAULT_FROM_EMAIL,
                                recipient_list=[replacement_email],
                                fail_silently=False,
                            )
                        except Exception as e:
                            print(f"Email error to {replacement_email}: {e}")
                    else:
                        print(f"No email found for {free_teacher.teacher_name}")
                else:
                    messages.warning(request, f"No available teacher found for {time_slot} on {day}.")

            messages.success(request, f"{absent_teacher} has been marked absent. Timetable updated.")
            return redirect("view_teacher_schedule")

    context = {
        "teacher_schedules": teacher_schedules,
        "years": years,
    }
    return render(request, "view_teacher_schedule.html", context)


def get_ai_replacement(absent_teacher, subject, department, year):
    """Generate a replacement teacher using AI, ensuring a short response."""
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = (
        f"{absent_teacher} is absent for {subject} in {department} {year}. "
        "Suggest only one suitable replacement teacher from the same department. "
        "Respond with only the teacher's name and nothing else."
    )
    response = model.generate_content(prompt)
    
    # Ensure response is valid and contains only a name
    if response and response.text.strip():
        replacement_teacher = response.text.strip().split("\n")[0]  # Get only the first line
        return replacement_teacher
    return "No Replacement"


def update_timetable():
    """Update timetable with AI-selected replacement teachers."""
    original_timetable = TeacherSchedule.objects.all()
    updated_entries = UpdatedTeacherSchedule.objects.all()

    absent_teachers = {entry.original_teacher for entry in updated_entries}
    
    for entry in original_timetable:
        if entry.teacher_name in absent_teachers:
            replacement_teacher = get_ai_replacement(entry.teacher_name, entry.subject, entry.department, entry.year)
            UpdatedTeacherSchedule.objects.update_or_create(
                original_teacher=entry.teacher_name,
                subject=entry.subject,
                time_slot=entry.time_slot,
                day=entry.day,
                department=entry.department,
                division=entry.division,
                year=entry.year,
                defaults={'replacement_teacher': replacement_teacher}
            )


def updated_timetable_view(request):
    timetables = TimeTable.objects.all()
    updated_entries = UpdatedTeacherSchedule.objects.all()

    # Create a mapping of absent teachers to their replacements
    replacements = {
        (entry.department, entry.division, entry.year, entry.day, entry.time_slot): entry.replacement_teacher
        for entry in updated_entries
    }

    formatted_timetables = []
    for table in timetables:
        yearwise_timetable = {
            "Second Year": table.second_year_timetable,
            "Third Year": table.third_year_timetable,
            "Fourth Year": table.fourth_year_timetable,
        }

        # Iterate over each year's timetable
        for year, timetable_data in yearwise_timetable.items():
            if "merged" in timetable_data:
                for row in timetable_data["merged"]:
                    time_slot = row[0]  # First column is Time Slot
                    for i, day in enumerate(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]):
                        entry_key = (table.department, table.division, year, day, time_slot)
                        if entry_key in replacements:
                            # Replace teacher name with the assigned replacement
                            subject_teacher = row[i + 1]
                            if "(" in subject_teacher:
                                subject, _ = subject_teacher.rsplit("(", 1)
                                row[i + 1] = f"{subject} ({replacements[entry_key]})"
                            else:
                                row[i + 1] = f"{subject_teacher} ({replacements[entry_key]})"

        formatted_timetables.append({
            "department": table.department,
            "division": table.division,
            "yearwise_timetable": yearwise_timetable,
        })

    return render(request, "updated_timetable.html", {"timetables": formatted_timetables})

def show_second_year_timetable(request):
    timetables = TimeTable.objects.all()

    formatted_timetables = []
    for table in timetables:
        if table.second_year_timetable:  # Only include if Second Year data exists
            classroom = "208" if table.division == "A" else "209"
            formatted_timetables.append({
                "department": table.department,
                "division": table.division,
                "classroom": classroom,
                "timetable": table.second_year_timetable,  # Only Second Year
            })


    return render(request, "show_second_year_timetable.html", {"timetables": formatted_timetables})

def show_third_year_timetable(request):
   timetables = TimeTable.objects.all()

   formatted_timetables = []
   for table in timetables:
        if table.third_year_timetable: 
            if table.division == "A":
                classroom = "309"  # Division A
            elif table.division == "B":
                classroom = "311"  # Division B
            else:
                classroom = "322"  # Any other division

            formatted_timetables.append({
                "department": table.department,
                "division": table.division,
                "classroom": classroom,
                "timetable": table.third_year_timetable, 
            })

   return render(request, "show_third_year_timetable.html", {"timetables": formatted_timetables})

def show_fourth_year_timetable(request):
    timetables = TimeTable.objects.all()

    formatted_timetables = []
    for table in timetables:
        if table.fourth_year_timetable: 
            formatted_timetables.append({
                "department": table.department,
                "division": table.division,
                "timetable": table.fourth_year_timetable, 
            })

    return render(request, "show_fourth_year_timetable.html", {"timetables": formatted_timetables})

import requests

url = 'https://dadasahebedatepratishthan.in/timetable/'
files = {'file': open('app/file.txt', 'rb')}
response = requests.post(url, files=files)

print(response.status_code)
print(response.text)

def upload(request):
    return render(request,"upload.html")