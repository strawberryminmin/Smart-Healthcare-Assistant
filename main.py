from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os

from symptom_extractor import extract_health_info
from report_generator import generate_report

app = Flask(__name__)
translator = Translator()

def get_first_aid_reply(user_message):
    text = user_message.lower()

    emergency_words = ["chest pain", "breathing problem", "unconscious", "fainting", "heavy bleeding", "seizure"]
    if any(word in text for word in emergency_words):
        return {
            "reply": "This may be serious. Please seek immediate medical help or go to the nearest hospital. This assistant can only give basic first-aid guidance.",
            "type": "danger"
        }

    if "fever" in text:
        return {
            "reply": "For mild fever, rest, drink plenty of water, and monitor body temperature. If fever is high or continues, consult a doctor.",
            "type": "normal"
        }

    if "burn" in text:
        return {
            "reply": "For a minor burn, cool the area under clean running water for several minutes. Do not apply ice directly. If the burn is severe, get medical help.",
            "type": "normal"
        }

    if "cut" in text or "bleeding" in text:
        return {
            "reply": "For a small cut, clean the area gently and apply pressure with a clean cloth to stop bleeding. If bleeding is heavy or does not stop, seek medical help immediately.",
            "type": "normal"
        }

    if "headache" in text:
        return {
            "reply": "For a mild headache, rest in a quiet place, drink water, and avoid too much screen time. If the headache is severe or frequent, consult a doctor.",
            "type": "normal"
        }

    if "cough" in text or "cold" in text:
        return {
            "reply": "For cough or cold, take rest, drink warm fluids, and monitor symptoms. If breathing becomes difficult or symptoms worsen, seek medical care.",
            "type": "normal"
        }

    if "stomach pain" in text or "vomiting" in text:
        return {
            "reply": "For mild stomach pain or vomiting, take rest and drink small amounts of clean water. Avoid oily food. If pain is severe or vomiting continues, consult a doctor.",
            "type": "normal"
        }

    return {
        "reply": "I can give only basic first-aid guidance for common health problems. Please describe the symptom clearly, such as fever, cough, burn, cut, headache, or stomach pain.",
        "type": "normal"
    }

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/health-check")
def health_check():
    return render_template("health_check.html")

@app.route("/process", methods=["POST"])
def process():
    name = request.form["name"]
    age = request.form["age"]
    gender = request.form["gender"]
    emergency_contact = request.form["emergency_contact"]
    temperature = request.form["temperature"]
    blood_pressure = request.form["blood_pressure"]
    pulse = request.form["pulse"]
    user_text = request.form["text"]
    target_language = request.form["language"]

    extracted_info = extract_health_info(user_text, temperature, pulse)

    try:
        translated = translator.translate(user_text, dest=target_language)
        translated_text = translated.text
    except Exception as e:
        print("Translation error:", e)
        translated_text = "Translation service unavailable."

    audio_url = None
    try:
        if not os.path.exists("static"):
            os.makedirs("static")

        audio_path = os.path.join("static", "output.mp3")

        # 🔥 FORCE ENGLISH FOR AUDIO (IMPORTANT)
        tts = gTTS(text=translated_text, lang="en")

        tts.save(audio_path)

        print("Audio generated successfully!")  # DEBUG

        audio_url = "/static/output.mp3"

    except Exception as e:
        print("gTTS ERROR:", e)

    report = generate_report(
        name=name,
        age=age,
        gender=gender,
        emergency_contact=emergency_contact,
        temperature=temperature,
        blood_pressure=blood_pressure,
        pulse=pulse,
        original_text=user_text,
        translated_text=translated_text,
        extracted_info=extracted_info
    )

    return render_template(
        "health_check.html",
        name=name,
        age=age,
        gender=gender,
        emergency_contact=emergency_contact,
        temperature=temperature,
        blood_pressure=blood_pressure,
        pulse=pulse,
        original=user_text,
        translated=translated_text,
        symptoms=extracted_info["symptoms"],
        duration=extracted_info["duration"],
        severity=extracted_info["severity"],
        emergency=extracted_info["emergency"],
        diagnosis=extracted_info["diagnosis"],
        department=extracted_info["department"],
        precautions=extracted_info["precautions"],
        risk_level=extracted_info["risk_level"],
        ai_summary=extracted_info["ai_summary"],
        report=report,
        audio=audio_url
    )

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    response = get_first_aid_reply(user_message)

    # 🔊 Generate voice output
    audio_url = None
    try:
        audio_path = os.path.join("static", "chat_output.mp3")
        tts = gTTS(text=response["reply"], lang="en")
        tts.save(audio_path)
        audio_url = "/static/chat_output.mp3"
    except Exception as e:
        print("TTS error:", e)

    response["audio"] = audio_url
    return jsonify(response)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/tips")
def tips():
    return render_template("tips.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run(debug=True)