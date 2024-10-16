import os
from openai import OpenAI
from flask import session
from flask import Flask, jsonify


"""
File:           followup.py
Description:    This file contains all necessary functions to detect follow - up questions and rephrase them
"""

MAX_MESSAGES = 4
openai_api_key = os.environ.get('OPENAI_API_KEY')



def get_conversation ():
    return session.get('conversation_history',[])

def save_conversation(conversation_history : dict):
    system_messages = [msg for msg in conversation_history if msg['role'] == 'system']
    user_messages = [msg for msg in conversation_history if msg ['role'] != 'system']
    user_messages = user_messages[-MAX_MESSAGES:]
    conversation_history = system_messages + user_messages
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
            "content": "You are an AI assistant that determines if a user's new question is related to the previous conversation. Two questions are considered related if they are about the same subject or if they pertain to the same courses (a course is a program of study, and a subject is a specific unit within a course). Note every course has CRISCO code (do not confuse with course code)"
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

def construct_rephrasev2(conversation_history: dict, followup_question: str, keywords: str) -> dict:
    messages = [
        {
            "role": "system",
            "content": ("You are an assistant that corrects the user based on the corrected keywords provided, such as the subject code or course code, and information from the conversation. Remember, "
                        "'course' and 'subject' are not interchangeable: a course is a program of study, while a subject refers to a specific "
                        "class or unit within a course. Additionally, every course has a CRISCO code, which should not be confused with a course code.")
        }
    ]
    # Add conversation history to the message
    messages.extend(conversation_history)

    # Add the user's follow-up question and keywords
    messages.append({
        "role": "user",
        "content": (f"Based on the conversation above, correct my last question to include the following corrected keywords: \"{keywords}\". "
                    f"My last question was: \"{followup_question}\".\n\nRephrased question:")
    })
    
    return messages

def construct_rephrase(conversation_history : dict, followup_question : str) -> dict:
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that rephrases user questions to include necessary context, such as the subject code or course code, based on the conversation. Remember, 'course' and 'subject' are not interchangeable: a course is a program of study, while a subject refers to a specific class or unit within a course. Note every course has a CRISCO code (do not confuse it with a course code). "
                "In the rephrased question, do not include the following words: 'course', 'subject', 'major', 'program', 'degree', 'curriculum', 'track', '&'. Additionally, do not include any words after keywords."
            )
        }
    ]
    
    # Add conversation history to the message
    messages.extend(conversation_history)

    # Add the user's follow-up question
    messages.append({
        "role": "user",
        "content": f"Based on the above conversation, rephrase my last question\n\nMy last question: \"{followup_question}\"\nRephrased question:"
    })
    
    return messages

def generate_popup_query(user_question: str, LLMkey=openai_api_key) -> list:
    message = [{
    "role": "system",
    "content": (
        "You are an AI assistant that generates 2 similar questions based on the user's input. Ensure that the generated questions do not include the words 'course', 'program', 'major', or 'subject' or 'degree' or 'curriculum', 'track'. "
        "The format for the questions should follow these examples: "
        "1. What are the prerequisites of _______? "
        "2. What are the requirements of _______? "
        "Fill in the blanks based on the user's input."
    )
    }]
    message.append({"role": "user", "content": f"My question: {user_question}"})
    
    response = OpenAI(api_key=LLMkey).chat.completions.create(
        model="gpt-4o",
        messages=message
    ).choices[0].message.content.strip()
    response_list = [r.strip() for r in response.split('\n')]
    print(response_list)
    return response_list
