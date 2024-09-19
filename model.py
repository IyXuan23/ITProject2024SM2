import openai

def ask_gpt_for_keywords(question):
    
    response = openai.ChatCompletion.create(
        model="gpt-4", 
        messages=[
             {"role": "system", "content": "You are an assistant that extracts the key field (such as pre-requisites, subject code, assessments, dates and times, contact information, overview, aims, etc.) and the full course name from user questions. Please return two lines: the first line should contain 'Key Field:', and the second line should contain 'Key Subject:'."},
            {"role": "user", "content": f"Extract the key field and full course name from this question: {question}"}
        ],
        max_tokens=50,  
        temperature=0.7 
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    return answer
