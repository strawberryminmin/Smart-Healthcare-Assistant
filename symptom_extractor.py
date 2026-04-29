def extract_health_info(text, temperature="", pulse=""):
    text_lower = text.lower()

    symptom_keywords = {
        "fever": "Fever",
        "cough": "Cough",
        "headache": "Headache",
        "cold": "Cold",
        "stomach pain": "Stomach Pain",
        "vomiting": "Vomiting",
        "dizziness": "Dizziness",
        "chest pain": "Chest Pain",
        "breathing problem": "Breathing Problem",
        "sore throat": "Sore Throat",
        "body pain": "Body Pain",
        "fatigue": "Fatigue"
    }

    detected_symptoms = []
    for key, value in symptom_keywords.items():
        if key in text_lower:
            detected_symptoms.append(value)

    duration_keywords = [
        "since yesterday",
        "for 1 day",
        "for 2 days",
        "for 3 days",
        "for 4 days",
        "for 5 days",
        "for one week",
        "for 2 weeks",
        "since morning",
        "since last night"
    ]

    detected_duration = "Not specified"
    for item in duration_keywords:
        if item in text_lower:
            detected_duration = item
            break

    severity_keywords = ["mild", "moderate", "severe", "continuous", "high"]
    detected_severity = "Not specified"
    for item in severity_keywords:
        if item in text_lower:
            detected_severity = item.capitalize()
            break

    emergency_keywords = ["chest pain", "breathing problem", "unconscious", "fainting", "heavy bleeding"]
    emergency_alert = "No"
    for item in emergency_keywords:
        if item in text_lower:
            emergency_alert = "Yes"
            break

    diagnosis = "Please consult a doctor for proper medical advice."
    department = "General Physician"
    precautions = "Take rest, stay hydrated, and monitor symptoms."
    risk_level = "Low"

    if "fever" in text_lower and "cough" in text_lower:
        diagnosis = "Possible flu or viral infection."
        department = "General Physician"
        precautions = "Drink fluids, rest well, and consult a doctor if fever continues."
        risk_level = "Medium"

    elif "headache" in text_lower and "fever" in text_lower:
        diagnosis = "Possible viral fever."
        department = "General Physician"
        precautions = "Take rest, drink water, and seek medical advice if symptoms worsen."
        risk_level = "Medium"

    elif "stomach pain" in text_lower or "vomiting" in text_lower:
        diagnosis = "Possible gastric or digestive issue."
        department = "Gastroenterology"
        precautions = "Avoid oily food, drink clean water, and consult a doctor if pain continues."
        risk_level = "Medium"

    elif "sore throat" in text_lower or "cold" in text_lower:
        diagnosis = "Possible throat or common cold infection."
        department = "ENT"
        precautions = "Take warm fluids, rest, and avoid cold food items."
        risk_level = "Low"

    elif "chest pain" in text_lower or "breathing problem" in text_lower:
        diagnosis = "Possible emergency condition."
        department = "Emergency / Cardiology"
        precautions = "Seek immediate medical help."
        risk_level = "High"

    try:
        temp_value = float(temperature) if temperature else 0
        pulse_value = int(pulse) if pulse else 0

        if temp_value >= 102 or pulse_value > 120:
            risk_level = "High"
        elif temp_value >= 100:
            if risk_level == "Low":
                risk_level = "Medium"
    except:
        pass

    ai_summary = f"Patient reports {', '.join(detected_symptoms) if detected_symptoms else 'no specific symptoms'}. Duration: {detected_duration}. Severity: {detected_severity}. Risk Level: {risk_level}. Recommended Department: {department}."

    return {
        "symptoms": detected_symptoms,
        "duration": detected_duration,
        "severity": detected_severity,
        "emergency": emergency_alert,
        "diagnosis": diagnosis,
        "department": department,
        "precautions": precautions,
        "risk_level": risk_level,
        "ai_summary": ai_summary
    }