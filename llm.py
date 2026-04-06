import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_explanation(topic: str) -> str:
    prompt = f"""
    If the topic is related to education, explain "{topic}" clearly for a student.
    Use bullet points and one simple example.
    For any other topic, return: "Sorry, this topic is not supported. Please ask about education-related topics."
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    return response.text