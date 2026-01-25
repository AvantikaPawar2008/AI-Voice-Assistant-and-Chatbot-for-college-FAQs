import speech_recognition as sr
import webbrowser
import pyttsx3  # text to speech
import json                        # to read JSON files
from datetime import datetime      # to get current day
import os                          # to build file paths safely


def load_json(filename):
    """
    This function reads a JSON file from the 'data' folder
    and returns it as a Python dictionary.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))  # folder where assistant.py is located
    file_path = os.path.join(base_dir, "data", filename)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"[ERROR] JSON decode error in: {file_path}")
        return {}
    

college_data = load_json("data1.json")


recogniser = sr.Recognizer()  # Recognise 
engine= pyttsx3.init()     # initialise pyttsx3

def speak(text):
    engine.say(text)
    engine.runAndWait()


4
def listen():
    #Listen for the wake word "Igris"
    #obtain audio from microphone
    r = sr.Recognizer()
    
     # recognize speech using Sphinx
    with sr.Microphone() as source:
        print("Listening...")
        # Adjust for background noise (helps recognition)
        r.adjust_for_ambient_noise(source, duration=0.5)
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio)
        print("You:", repr(query))   # repr() so we see exact text including spaces
        return query.lower()
    except Exception as e:
        print("[ERROR in STT]:", e)
        speak("Sorry, say it again.")
        return ""
    
#to detect query
def detect_intent(q):
    """
    This function decides what the user wants to do,
    based on simple keywords in the query string.
    """
    q = q.lower()   # convert to lowercase for easy matching

    # Timetable related
    if any(word in q for word in [
        "timetable", "schedule", "class time", "routine", "time table",
        "lecture timing", "class schedule"
    ]):
        return "timetable"
    
    #department related
    if any(word in q for word in ["department", "branch", "stream",
        "course", "engineering", "info", "details"
    ]):
        return "department"
    
    # HOD related
    if any(word in q for word in [
        "hod", "head of department", "department head", "hod name",
        "hod details"
    ]):
        return "hod"

    # Faculty related
    if any(word in q for word in [
        "faculty", "professor", "teacher", "sir", "madam", "staff",
        "faculty list", "faculty details"
    ]):
        return "faculty"

    # Open website or links
    if any(word in q for word in [
        "open", "website", "portal", "launch", "show me", "visit",
        "open link", "browser", "google", "youtube"
    ]):
        return "open_link"

    # FAQ / General Info
    if any(word in q for word in [
        "attendance", "fees", "fee", "criteria", "rules", "regulation",
        "marks", "cgpa", "sgpa", "exam", "syllabus", "subjects"
    ]):
        return "faq"

    # Greetings (new intent if needed)
    if any(word in q for word in [
        "hello", "hi", "hey", "good morning", "good evening"
    ]):
        return "greet"

    # Exit or stop
    if any(word in q for word in [
        "stop", "exit", "quit", "bye"
    ]):
        return "exit"

    return "unknown"



# handle query
def handle_intent(intent, query):
    """
    This function performs the actual action
    based on the detected intent.
    """

    # 1) Today's timetable
    if intent == "timetable":
        # get current day in short form: mon, tue, wed...
        day_code = datetime.now().strftime("%a").lower()  # e.g. "Mon" -> "mon"

        if day_code not in timetable:
            speak("No timetable found for today.")
            return

        slots = timetable[day_code]
        if not slots:
            speak("No lectures scheduled for today.")
            return

        msg = "Your timetable for today is: "
        for subject, start, end, room in slots:
            msg += f"{subject} from {start} to {end} in {room}. "
        speak(msg)
        return
    #hod
    if intent == "hod":
        speak("Please say the department name.")
        dept_name = listen()

        for dept in college_data["departments"]:
            if dept["name"].lower().split()[0] in dept_name:
                speak(f"The HOD of {dept['name']} is {dept['hod']}.")
                return

        speak("HOD information not found.")
        return
    # department
    if intent == "department":
        for dept in college_data["departments"]:
            if dept["name"].lower().split()[0] in query:
                msg = f"{dept['name']} offers: "
                for c in dept["courses"]:
                    msg += f"{c['course_name']} ({c['duration_years']} years){c['hod_name']} "
                speak(msg)
                return
        return
    
    if intent == "admissions":
        adm = college_data["admissions"]
        text = (
            f"Admission is through {adm['process']}. "
            f"UG eligibility: {adm['eligibility']['ug']}. "
            f"PG eligibility: {adm['eligibility']['pg']}."
        )
        speak(text)
        return
    
    if intent == "hostel":
        h = college_data["hostel"]
        text = (
            f"Boys hostel capacity is {h['boys_hostel']['capacity']} with "
            f"{h['boys_hostel']['rooms']} rooms. "
            f"Girls hostel capacity is {h['girls_hostel']['capacity']} with "
            f"{h['girls_hostel']['rooms']} rooms."
        )
        speak(text)
        return

    
if __name__ == "__main__":
    speak("Hello ! I am your college assistant. How can I help you?")

    while True:
        query = listen()

        # if nothing recognised, skip this loop
        if query == "":
            continue

        # EXIT CONDITIONS
        if any(phrase in query for phrase in [
            "exit", "quit", "stop", "good bye", "goodbye", "bye"
        ]):
            speak("Goodbye! Have a nice day.")
            break

        # detect what user wants
        intent = detect_intent(query)

        # perform the action
        handle_intent(intent, query)