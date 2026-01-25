# web_assist.py
import json
import os
from datetime import datetime

# --- Load Data ---
def load_json(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", filename)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {}

college_data = load_json("data1.json")

# --- Logic Functions ---
def detect_intent(q):
    q = q.lower()
    if any(word in q for word in ["timetable", "schedule", "class time", "routine", "time table",
        "lecture timing", "class schedule"]):
        return "timetable"
    
    if any(word in q for word in ["hod", "head of department", "department head", "hod name",
        "hod details"]):
        return "hod"
    
    if any(word in q for word in ["program", "course", "degree", "undergraduate", "postgraduate",
        "bachelor", "master", "phd"]):
        return "programs"
    
    if any(word in q for word in ["department", "branch", "stream",
        "course", "engineering"  ]):
        return "department"
    
    if any(word in q for word in ["hello", "hi", "hey", "good morning", "good evening"]):
        return "greet"
    
    if any(word in q for word in ["admission", "apply", "eligibility", "entrance exam", "cet", "jee", "dates"]):
        return "admissions"

    if any(word in q for word in ["hostel", "stay", "accommodation", "dorm", "rooms", "living", "residence","boys hostel","girls hostel"]):
        return "hostel"
    
    if any(word in q for word in ["facility","facilities" ,"lab", "library", "wifi", "canteen", "sports", "sport","gym"]):
        return "facilities"
    if any(word in q for word in ["event", "fest", "spectrum", "swartarang", "kshitij", "technical fest","tech fest","cultural fest"]):
        return "events"
    if any(word in q for word in ["contact", "phone", "email", "address", "location", "where is"]):
        return "contact"
    if any(word in q for word in ["placement","placements","jobs","job opportunities", "recruiters","companies","placement companies",
    "campus placement","placement record", "package","salary","average package","highest package","ctc"]):
         return "placements"
    if any(word in q for word in ["clubs","club", "teams", "student groups", "organization", "society", "extra-curricular"
  " team red baron", "team kratos racing", "team solarium", "team ambush", "team automatons ",
  "team maverick india", "team anantam", "the coding club"]):
        return "clubs"
    if any(word in q for word in ["stop", "exit", "bye"]):
        return "exit"
    return "unknown"

def get_response(intent, query):
    # 1. Greetings
    if intent == "greet":
        return (f"Hello! Welcome to {college_data['college']['short_name']}."
                " I’m your virtual college assistant, here to help you with admissions, departments, facilities, and more. How can I assist you today?"
        )

    # 2. HOD Information
    elif intent == "hod":
        for dept in college_data.get("departments", []):
            if dept["name"].lower().split()[0] in query:
                return (f"The Head of the {dept['name']} Department is {dept['hod']}."
                        " Let me know if you’d like details about courses or facilities in this department.")
        return "Please specify the department, such as Computer, IT, or Mechanical."

    # 3. Department & Course Details
    elif intent == "department":
        for dept in college_data.get("departments", []):
            if dept["name"].lower().split()[0] in query:
                course = dept["courses"][0]
                return ( f"The {dept['name']} Department offers the {course['course_name']} program. "
                         f"The annual intake is {course['intake']} students, and the yearly fee is {course['fees_per_year']} rupees. "
                         f"The department is headed by {dept['hod']}.")
        return "Which department would you like to know about? We offer Computer, Information Technology, Civil, Mechanical, and more."

    # 4. Programs Offered
    elif intent == "programs":
        mode=college_data.get("programs",{})
        if any(word in query for word in ["undergraduate", "bachelor", "b.tech"]):
            return "Our undergraduate programs include B.Tech in Computer Science, Information Technology, Civil Engineering, and Mechanical Engineering."
        elif any(word in query for word in ["postgraduate", "master", "m.tech"]):
            return "We offer postgraduate M.Tech programs in Computer Science, Structural Engineering, and Thermal Engineering."
        elif any(word in query for word in ["phd", "doctorate"]):
            return "PhD programs are available in multiple disciplines, including Computer Science, Civil Engineering, and Mechanical Engineering."
        else:
           return "We offer Undergraduate (B.Tech), Postgraduate (M.Tech), and PhD programs. Which level are you interested in?"
    # 5. Admissions
    elif intent == "admissions":
        adm = college_data.get("admissions", {})
        if any(word in query for word in ["date", "when"]):
           return f"Admissions begin on {adm['important_dates']['form_start']}, and the last date to apply is {adm['important_dates']['last_date']}."
        elif any(word in query for word in ["exam", "how"]):
            exams = ", ".join(adm["entrance_exams"])
            return f"Admissions are conducted through {adm['process']}. Applicants need to appear for entrance exams such as {exams}."
        else:
            return f"For undergraduate programs, the eligibility criteria are: {adm['eligibility']['ug']}."


    # 5. Hostel Information
    elif intent == "hostel":
        h = college_data.get("hostel", {})
        if "girl" in query:
           return f"Our girls’ hostel accommodates {h['girls_hostel']['capacity']} students, with an annual fee of {h['girls_hostel']['fees_per_year']} rupees."
        elif"boy" in query:
           return f"Our boys’ hostel has a capacity of {h['boys_hostel']['capacity']} students, and the annual fee is {h['boys_hostel']['fees_per_year']} rupees."
        else:
            return (
                       f"We provide separate hostels for boys and girls. "
                        f"The girls’ hostel accommodates {h['girls_hostel']['capacity']} students, "
                        f"while the boys’ hostel can house {h['boys_hostel']['capacity']} students."
                        f"Both hostels offer amenities like Wi-Fi, a mess, and recreational areas.")


    # 6. Facilities
    elif intent == "facilities":
        fac = college_data.get("facilities", {})
        if "lab" in query:
            labs = ", ".join(fac["laboratories"][:5])
            return f"Our campus has well-equipped laboratories including {labs}, along with several advanced research labs."
        elif "sport" in query:
            sports = ", ".join(fac["sports"])
            return f"We offer excellent sports facilities such as {sports}, encouraging both fitness and team spirit."
        else:
            return (f"Our college offers a variety of facilities including a modern library, "
                    f"state-of-the-art laboratories, high-speed Wi-Fi across the campus, "
                    f"a hygienic canteen, and extensive sports amenities.")

    # 7. Events & Fests
  
    elif intent == "events":
        events_list = college_data.get("events", [])
        
        found_event = None
        for e in events_list:
            if e['name'].lower() in query.lower():
                found_event = e
                break
        if found_event:
            return f"{found_event['name']} is a {found_event['type']} event, usually conducted in the month of {found_event['month']}."
        elif events_list:
            all_names = ", ".join([e['name'] for e in events_list])
            return f"Our major college events include {all_names}. Which event would you like to know more about?"
        else:
            return "Currently, there are no upcoming events listed."

    # 8. Contact & Location
    elif intent == "contact":
        con = college_data.get("contact", {})
        return f"You can contact the college at {con['phone']} or visit the campus at {con['address']}. I can also help with directions if needed."


    # 9. Timetable
    elif intent == "timetable":
        return "The class timetable is available on the official college portal under the Academics section."


    # 10. Placements
    elif intent == "placements":
           pl= college_data.get("placements", {})
           if any(word in query for word in ["average", "package", "salary"]):
            return f"The average placement package offered to students is around {pl['average_package']} per annum."
           elif any(word in query for word in ["recruiters", "job", "companies", "hiring", "offers","placements"]):
             recruiters = ", ".join(pl["top_recruiters"][:5])
           return ( f"The placement rate is approximately 80–85%. "
                    f"Top recruiters include {recruiters}, along with many other reputed companies.")
  

    # 11. Clubs and Student Teams
    elif intent == "clubs":
        clubs_list = college_data.get("clubs", [])
        for club in clubs_list:
            if club['clubName'].lower() in query.lower():
                return f"{club['clubName']}: {club['Description']}"
        if clubs_list:
            club_names = ", ".join([c['clubName'] for c in clubs_list])
            return f"We have several student clubs including: {club_names}. Which one would you like to know more about?"
        
        return "I couldn't find any information about student clubs right now."

    return "I’m sorry, I don’t have information on that yet. You can ask me about departments, admissions, placements, facilities, or campus life."
    