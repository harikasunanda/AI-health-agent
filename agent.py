import ollama

def analyze_lab(patient_data):
    prompt = f"""
    Analyze hospital consultation data.

    Data:
    {patient_data}

    Provide:
    - Doctor workload insights
    - Specialty demand
    - Any unusual patterns
    """

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]


def calculate_risk(data):
    return "Moderate"


def generate_recommendation(data, risk):
    prompt = f"""
    Based on this consultation data:
    {data}

    Risk level: {risk}

    Suggest improvements for hospital operations.
    """

    response = ollama.chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]