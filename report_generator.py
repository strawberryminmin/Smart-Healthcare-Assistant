from datetime import datetime

def generate_report(name, age, gender, emergency_contact, temperature, blood_pressure, pulse,
                    original_text, translated_text, extracted_info):

    report = []

    report.append("===== SMART HEALTHCARE REPORT =====")
    report.append(f"Date & Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("")

    # 👤 Patient Info
    report.append("---- PATIENT DETAILS ----")
    report.append(f"Name: {name}")
    report.append(f"Age: {age}")
    report.append(f"Gender: {gender}")
    report.append(f"Emergency Contact: {emergency_contact}")
    report.append("")

    # 🩺 Vitals
    report.append("---- VITAL SIGNS ----")
    report.append(f"Temperature: {temperature} °F")
    report.append(f"Blood Pressure: {blood_pressure}")
    report.append(f"Pulse Rate: {pulse} bpm")
    report.append("")

    # 🗣️ Patient Input
    report.append("---- PATIENT DESCRIPTION ----")
    report.append(f"Original Input: {original_text}")
    report.append(f"Translated Explanation: {translated_text}")
    report.append("")

    # 🧠 Structured Data (MOST IMPORTANT)
    report.append("---- STRUCTURED SYMPTOM SUMMARY ----")
    report.append("Symptoms: " + (", ".join(extracted_info["symptoms"]) if extracted_info["symptoms"] else "Not clearly specified"))
    report.append(f"Duration: {extracted_info['duration']}")
    report.append(f"Severity: {extracted_info['severity']}")
    report.append("")

    # 🚨 Risk Analysis
    report.append("---- RISK ASSESSMENT ----")
    report.append(f"Emergency Indicator: {extracted_info['emergency']}")
    report.append(f"Risk Level: {extracted_info['risk_level']}")
    report.append("")

    # 🏥 Medical Guidance
    report.append("---- PRELIMINARY MEDICAL INSIGHT ----")
    report.append(f"Possible Condition: {extracted_info['diagnosis']}")
    report.append(f"Recommended Department: {extracted_info['department']}")
    report.append("")

    # ⚕️ Action
    report.append("---- RECOMMENDED ACTION ----")
    report.append(f"Precautions / Advice: {extracted_info['precautions']}")
    report.append("")

    # 🎯 Purpose (THIS FIXES YOUR LOGIC ISSUE)
    report.append("---- PURPOSE ----")
    report.append("This report structures patient-provided symptoms into a clear format to reduce miscommunication and assist in better understanding during medical consultation.")
    report.append("")

    # ⚠️ Disclaimer
    report.append("Note: This system provides basic guidance only and does not replace professional medical diagnosis.")

    return "\n".join(report)