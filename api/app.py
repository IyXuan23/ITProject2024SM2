import os
from dotenv import load_dotenv
from functools import wraps
from flask import Flask, jsonify, Response, request, session
from flask_cors import CORS
import flask
import psycopg2
from psycopg2 import sql
from openai import OpenAI
from cache import MemoryCache
from dependencies.vanna import VannaDefault
from followup import *

# TODO: Implement a functionality to manage cookie (session) size

"""
File:           app.py
Description:    This file contains all necessary functions for VANNA to generate a SQL query from the user's input
"""

                            ####################### SET UP #######################
cache = MemoryCache()
load_dotenv()
app = Flask(__name__, static_url_path='')

openai_api_key = os.environ.get('OPENAI_API_KEY')
vanna_api_key = os.environ.get('VANNA_API_KEY')
# For testing, set the secret_key to any number (e.g: '1')
app.secret_key = '9999'


#vanna_model_name = "unimelbhtesting"
vanna_model_name = "unimelb-handbook-chatbot"


vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)

                            ####################### CACHES & COOKIES #######################
@app.before_request
def make_session_non_permanent():
    # Ensure that the session is cleared when the browser is closed
    session.permanent = False 

def requires_cache(fields):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            id = request.args.get('id')

            if id is None:
                return jsonify({"type": "error", "error": "No id provided"})
            
            for field in fields:
                if cache.get(id=id, field=field) is None:
                    return jsonify({"type": "error", "error": f"No {field} found"})
            
            field_values = {field: cache.get(id=id, field=field) for field in fields}
            
            # Add the id to the field_values
            field_values['id'] = id

            return f(*args, **field_values, **kwargs)
        return decorated
    return decorator


                            ####################### MAIN FUNCTIONS #######################

def is_sql_valid(sql_query:str) -> bool:
    try:
        # 使用您的数据库连接参数
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres.seqkcnapvgkwqbqipqqs",
            password="IT Web Server12",
            host="aws-0-ap-southeast-2.pooler.supabase.com",
            port=6543
        )
        cur = conn.cursor()
        conn.set_session(autocommit=False)
        try:
            cur.execute(sql.SQL("EXPLAIN {}").format(sql.SQL(sql_query)))
            conn.rollback() 
            return True
        except psycopg2.Error as e:
            conn.rollback()
            return False
        finally:
            cur.close()
    except psycopg2.Error as e:
        return False
    finally:
        if conn:
            conn.close()

# TODO: Implement a functionality to manage cookie (session) size
@app.route('/api/v0/generate_sql', methods=['GET'])
def generate_sql():
    user_question = flask.request.args.get('question')
    previous_convo = get_conversation()
    print(previous_convo)
    
    if previous_convo:
        # Determine whether the question is a follow - up question
        if is_followup_question(previous_convo, user_question):
            messages = construct_rephrase(previous_convo, user_question)
            rephrased_question = rephrase_question(messages)
        
        # If the user change topic, the convo history will be reset
        else:
            print("RESET")
            previous_convo = [{"role": "system",
                "content": "You are a university handbook assistant chatbot, you help student find subject information, you are providing formal and precise response corresponding to the user input, you are now asked to convert the following text into a more colloquial response and do not include 'sure', response in markdown format."},]
            save_conversation(previous_convo)
            rephrased_question = user_question
    else:
        messages=[
                {"role": "system",
                "content": "You are a university handbook assistant chatbot, you help student find subject information, you are providing formal and precise response corresponding to the user input, you are now asked to convert the following text into a more colloquial response and do not include 'sure', response in markdown format."},
                ]
        previous_convo.extend(messages)
        save_conversation(previous_convo)
        rephrased_question = user_question
    
    # Generate the SQL query from the user REPHRASED question
    sql = vn.generate_sql(rephrased_question)
    print(rephrased_question)
    print(sql)
    valid = is_sql_valid(sql)

    if valid:

        # Fetch info from database
        conn = psycopg2.connect(database="postgres",user="postgres.seqkcnapvgkwqbqipqqs",password="IT Web Server12",host="aws-0-ap-southeast-2.pooler.supabase.com",port=6543)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.close()
        
        client = OpenAI(
            api_key=openai_api_key)
        
        # Pass the user's query and fetched data to LLM
        previous_convo.append({"role": "user", "content": f"User input: {rephrased_question}"})
        previous_convo.append({"role": "assistant", "content": f"System output: {result}"})
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=previous_convo
        ).choices[0].message.content
        previous_convo.append({"role": "assistant", "content": response})

        # Save conversation
        save_conversation(previous_convo)
        
        # Return the OpenAI response as a JSON response
        return jsonify({
            "response": response,
        })
    return jsonify({
        "response": sql,
    })


@app.route('/api/v0/run_sql', methods=['GET'])
@requires_cache(['sql'])
def run_sql(id: str, sql: str):
    try:
        df = vn.run_sql(sql=sql)

        cache.set(id=id, field='df', value=df)

        return jsonify(
            {
                "type": "df", 
                "id": id,
                "df": df.head(10).to_json(orient='records'),
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})
                        
                        ####################### FIXED FOLLOW - UP QUESTIONS #######################

@app.route('/api/v0/generate_questions', methods=['GET'])
def generate_questions():
    generate_questions = vn.generate_questions()
    return jsonify({
        "type": "question_list",
        "questions": generate_questions,
        "header": "Here are some questions you can ask:"
        })

@app.route('/api/v0/generate_followup_questions', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_followup_questions(id: str, df, question, sql):
    followup_questions = vn.generate_followup_questions(question=question, sql=sql, df=df)

    cache.set(id=id, field='followup_questions', value=followup_questions)

    return jsonify(
        {
            "type": "question_list", 
            "id": id,
            "questions": followup_questions,
            "header": "Here are some followup questions you can ask:"
        })

@app.route('/api/v0/load_question', methods=['GET'])
@requires_cache(['question', 'sql', 'df', 'fig_json', 'followup_questions'])
def load_question(id: str, question, sql, df, fig_json, followup_questions):
    try:
        return jsonify(
            {
                "type": "question_cache", 
                "id": id,
                "question": question,
                "sql": sql,
                "df": df.head(10).to_json(orient='records'),
                "fig": fig_json,
                "followup_questions": followup_questions,
            })

    except Exception as e:
        return jsonify({"type": "error", "error": str(e)})

                        ####################### TRAINING #######################

@app.route('/api/v0/get_training_data', methods=['GET'])
def get_training_data():
    df = vn.get_training_data()

    return jsonify(
    {
        "type": "df", 
        "id": "training_data",
        "df": df.head(25).to_json(orient='records'),
    })

@app.route('/api/v0/remove_training_data', methods=['POST'])
def remove_training_data():
    # Get id from the JSON body
    id = flask.request.json.get('id')

    if id is None:
        return jsonify({"type": "error", "error": "No id provided"})

    if vn.remove_training_data(id=id):
        return jsonify({"success": True})
    else:
        return jsonify({"type": "error", "error": "Couldn't remove training data"})

@app.route('/api/v0/train', methods=['POST'])
def add_training_data():
    question = flask.request.json.get('question')
    sql = flask.request.json.get('sql')
    ddl = flask.request.json.get('ddl')
    documentation = flask.request.json.get('documentation')

    try:
        id = vn.train(question=question, sql=sql, ddl=ddl, documentation=documentation)

        return jsonify({"id": id})
    except Exception as e:
        print("TRAINING ERROR", e)
        return jsonify({"type": "error", "error": str(e)})

                        ####################### UTILS #######################

@app.route('/api/v0/download_csv', methods=['GET'])
@requires_cache(['df'])
def download_csv(id: str, df):
    csv = df.to_csv()

    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 f"attachment; filename={id}.csv"})

@app.route('/api/v0/generate_plotly_figure', methods=['GET'])
@requires_cache(['df', 'question', 'sql'])
def generate_plotly_figure(id: str, df, question, sql):
    try:
        code = vn.generate_plotly_code(question=question, sql=sql, df_metadata=f"Running df.dtypes gives:\n {df.dtypes}")
        fig = vn.get_plotly_figure(plotly_code=code, df=df, dark_mode=False)
        fig_json = fig.to_json()

        cache.set(id=id, field='fig_json', value=fig_json)

        return jsonify(
            {
                "type": "plotly_figure", 
                "id": id,
                "fig": fig_json,
            })
    except Exception as e:
        # Print the stack trace
        import traceback
        traceback.print_exc()

        return jsonify({"type": "error", "error": str(e)})

@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/api/v0/get_question_history', methods=['GET'])
def get_question_history():
    return jsonify({"type": "question_history", "questions": cache.get_all(field_list=['question']) })

                        ####################### CONTROL #######################

if __name__ == '__main__':
    app.run(debug=True)







