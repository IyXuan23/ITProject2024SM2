import openai
import re

def ask_gpt_for_keywords(question):
    prompt = (
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
        "Now, extract the key field and full course name from this question:\nUser: {question}"
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=50,
        temperature=0.3
    )

    answer = response['choices'][0]['message']['content'].strip()
    
    match = re.search(r'Key Field:\s*(.*)\nKey Subject:\s*(.*)', answer, re.IGNORECASE)
    if match:
        key_field = match.group(1).strip()
        key_subject = match.group(2).strip()
        return f"Key Field: {key_field}\nKey Subject: {key_subject}"
    else:
        raise ValueError("Invalid response format from GPT model.")