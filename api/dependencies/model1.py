from openai import OpenAI
import re
import os

openai_api_key = os.environ.get('OPENAI_API_KEY')


def ask_gpt_for_keywords(question):
    messages = [
        {"role": "system", "content": (
            "You are an assistant that extracts the key field (such as pre-requisites, subject code, assessments, "
            "dates and times, contact information, overview, aims, etc.) and the full course name from user questions. "
            "Please return two lines:\n"
            "Key Field: [extracted field]\n"
            "Key Subject: [extracted course name]\n\n"
            "Examples:\n"
            "User: What are the pre-requisites for Calculus 1?\n"
            "Assistant:\nKey Field: pre-requisites\nKey Subject: Calculus 1\n\n"
            "User: Tell me about the assessments in Introduction to Programming.\n"
            "Assistant:\nKey Field: assessments\nKey Subject: Introduction to Programming\n\n"
            "User: I need the contact information for Advanced Physics.\n"
            "Assistant:\nKey Field: contact information\nKey Subject: Advanced Physics\n\n"
            "Now, extract the key field and full course name from this question:"
        )},
        {"role": "user", "content": question}
    ]

    response = OpenAI(api_key=openai_api_key).chat.completions.create(
        model="gpt-4o",  # Ensure you have access to this model
        messages=messages,
        max_tokens=50,
        temperature=0.3
    ).choices[0].message.content.strip()

    # Use regex to extract Key Field and Key Subject
    match = re.search(r'Key Field:\s*(.*)\nKey Subject:\s*(.*)', response, re.IGNORECASE)
    if match:
        key_field = match.group(1).strip()
        key_subject = match.group(2).strip()
        return f"Key Field: {key_field}\nKey Subject: {key_subject}"
    else:
        raise ValueError("Invalid response format from GPT model.")
    