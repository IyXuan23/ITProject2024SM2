import os
from openai import OpenAI
from flask import session


"""
File:           followup.py
Description:    This file contains all necessary functions to detect follow - up questions and rephrase them
"""

openai_api_key = os.environ.get('OPENAI_API_KEY')

def get_conversation ():
    return session.get('conversation_history',[])

def save_conversation(conversation_history : dict):
    session['conversation_history'] = conversation_history

def rephrase_question(convo : dict) -> str:
    response = OpenAI(api_key=openai_api_key).chat.completions.create(
        model="gpt-4o-mini",
        messages=convo
    ).choices[0].message.content
    return response

def is_followup_question(conversation_history : dict, new_question : str) -> bool:
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that determines if a user's new question is related to the previous conversation. Two questions are considered unrelated if they are about different subjects (with different subject names or codes) or if they pertain to different courses (a course is a program of study, and a subject is a specific unit within a course)."
        }
    ]
    messages.extend(conversation_history)
    messages.append({
        "role": "user",
        "content": (
            f"Is the following question a follow-up to our previous conversation or a new topic?\n"
            f"Question: \"{new_question}\"\n"
            "Answer with 'follow-up' or 'new topic'."
        )
    })
    response = OpenAI(api_key=openai_api_key).chat.completions.create(
        model="gpt-4o",
        messages=messages
    ).choices[0].message.content.strip().lower()

    if 'follow-up' in response:
        return True
    else:
        return False

def construct_rephrase(conversation_history : dict, followup_question : str) -> dict:
    messages = [{"role": "system",
    "content": "You are an assistant that rephrases user questions to include necessary context, such as the subject code or course code, based on the conversation. Remember, 'course' and 'subject' are not interchangeable: a course is a program of study, while a subject refers to a specific class or unit within a course."}]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": f"Based on the above conversation, rephrase my last question\n\nMy last question: \"{followup_question}\"\nRephrased question:"})
    return messages
