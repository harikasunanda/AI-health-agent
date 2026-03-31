import ollama

def analyze_lab(patient_data):
    """
    Analyze patient health data and return diagnosis
    """

    prompt = f"""
You are an AI medical assistant.

Analyze the following patient data and provide a clinical-style response.

PATIENT DATA:
{patient_data}

Provide output in this format:

1. Possible Conditions (Top 3 likely diagnoses)
2. Risk Level (Low / Moderate / High / Critical)
3. Key Observations (important abnormal values)
4. Recommended Actions (medications, tests, lifestyle)
5. Urgency (Immediate / Soon / Routine)

IMPORTANT:
- Be medically accurate
- Use simple but professional language
- Do NOT hallucinate unknown data
- If data is missing, mention it
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"


def calculate_risk(data):
    """
    Basic rule-based risk scoring (can improve later)
    """

    try:
        risk_score = 0

        if "bp" in data and data["bp"]:
            if isinstance(data["bp"], (int, float)) and data["bp"] > 140:
                risk_score += 2

        if "heart_rate" in data and data["heart_rate"]:
            if data["heart_rate"] > 100:
                risk_score += 2

        if "temperature" in data and data["temperature"]:
            if data["temperature"] > 38:
                risk_score += 2

        if "glucose" in data and data["glucose"]:
            if data["glucose"] > 180:
                risk_score += 2

        if risk_score >= 6:
            return "Critical"
        elif risk_score >= 4:
            return "High"
        elif risk_score >= 2:
            return "Moderate"
        else:
            return "Low"

    except:
        return "Unknown"


def generate_recommendation(data, risk):
    """
    Generate treatment & lifestyle suggestions
    """

    prompt = f"""
You are a medical assistant.

Patient Data:
{data}

Risk Level: {risk}

Provide:
1. Immediate actions (if needed)
2. Suggested medications (general guidance only)
3. Lifestyle recommendations
4. Follow-up tests

Keep it clear, practical, and safe.
"""

    try:
        response = ollama.chat(
            model="phi3",
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"AI Error: {str(e)}"