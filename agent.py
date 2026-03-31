import ollama

def analyze_lab(patient_data):

    prompt = f"""
You are an AI clinical assistant.

Analyze the patient data and provide a medical assessment.

PATIENT DETAILS:
- Age: {patient_data.get("patient_age")}
- Gender: {patient_data.get("patient_gender")}

VITALS:
- BP: {patient_data.get("systolic_bp")}/{patient_data.get("diastolic_bp")}
- Pulse: {patient_data.get("pulse")}
- SpO2: {patient_data.get("spo2")}
- Temperature: {patient_data.get("temperature")}
- Respiratory Rate: {patient_data.get("respiratoryrate")}
- BMI: {patient_data.get("bmi")}

SYMPTOMS:
{patient_data.get("doctorsymptoms")}

LAB RESULTS:
{patient_data.get("labtestresult")}

Provide:

1. Possible Conditions (Top 3)
2. Risk Level (Low / Moderate / High / Critical)
3. Key Abnormal Findings
4. Recommended Actions
5. Urgency Level

Be medically safe and avoid overconfidence.
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"