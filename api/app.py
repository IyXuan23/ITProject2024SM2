import os
from functools import wraps
from flask import Flask, jsonify, Response, request, session
from flask_cors import CORS
import flask
import psycopg2
from psycopg2 import sql
from openai import OpenAI
from dependencies.cache import MemoryCache
from dependencies.vanna import VannaDefault
from dependencies.followup import *
import secrets
from dependencies.correct import correct_subject 


"""
File:           app.py
Description:    This file contains all necessary functions for Flask to execute when the user send "GET" request and VANNA training functions.
"""

                            ####################### SET UP #######################
cache = MemoryCache()
app = Flask(__name__, static_url_path='')


openai_api_key = os.environ.get('OPENAI_API_KEY')
vanna_api_key = os.environ.get('VANNA_API_KEY')
vanna_model_name = os.environ.get('VANNA_MODEL_NAME')

 



CORS(app, resources={r"/api/*": {"origins": "*"}})
app.secret_key = secrets.token_hex()

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

@app.route('/api/v0/generate_sql', methods=['GET'])
def generate_sql():
    user_question = flask.request.args.get('question')
    previous_convo = get_conversation()

    # Determine if this is a new conversation
    if previous_convo:
        # Determine whether the question is a follow - up question
        if not is_followup_question(previous_convo, user_question):
            # If not, reset the conversation history then rephrase user's question 
            print("RESET")
            previous_convo = []
            messages = construct_rephrase(previous_convo, user_question)
            rephrased_question = rephrase_question(messages)
            previous_convo = [{"role": "system",
                "content": "You are a university handbook assistant chatbot, you help student find information, " 
                "you are providing formal and precise response corresponding to the user input, " 
                "you are now asked to convert the following text into a more colloquial response and do not include 'sure', response in markdown format. " 
                "Please use the context provided in the system output to answer " 
                "(If system output is empty or none, inform user that there is no available information)."}]
            save_conversation(previous_convo)
        else:
            messages = construct_rephrase(previous_convo, user_question)
            rephrased_question = rephrase_question(messages)
    else:
        messages = construct_rephrase(previous_convo, user_question)
        rephrased_question = rephrase_question(messages)
        messages=[
                {"role": "system",
                "content": "You are a university handbook assistant chatbot, you help student find information, " 
                "you are providing formal and precise response corresponding to the user input, " 
                "you are now asked to convert the following text into a more colloquial response and do not include 'sure', response in markdown format. " 
                "Please use the context provided in the system output to answer "
                "(If system output is empty or none, inform user that there is no available information)."}]
        previous_convo.extend(messages)
        save_conversation(previous_convo)
    
    # Generate the SQL query from the user REPHRASED question
    sql = vn.generate_sql(rephrased_question)

    # Debug 
    print(previous_convo)  
    print(rephrased_question)
    print(sql)
  
    valid = is_sql_valid(sql)
    if valid:
        
        # Establish the database connection
        conn = psycopg2.connect(
        database="postgres",
        user="postgres.seqkcnapvgkwqbqipqqs",
        password="IT Web Server12",
        host="aws-0-ap-southeast-2.pooler.supabase.com",
        port=6543
        )

        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()

        # Get column names from the cursor description
        column_names = [desc[0] for desc in cur.description]

        # Initialize a dictionary with column names as keys and empty lists as values
        result_dict = {col_name: [] for col_name in column_names}

        # Populate the dictionary with data
        for row in rows:
            for col_name, value in zip(column_names, row):
                result_dict[col_name].append(value)

        # Close the cursor and the connection
        cur.close()
        conn.close()

        # Remove columns that have no data (all values are None or empty)
        filtered_result_dict = {}
        for col_name, data_list in result_dict.items():
            if any(value not in (None, '', []) for value in data_list):
                filtered_result_dict[col_name] = data_list

        # Debug
        print(filtered_result_dict)

        client = OpenAI(
            api_key=openai_api_key)
      
        # Pass the user's query and fetched data to LLM
        previous_convo.append({"role": "user", "content": f"User input: {rephrased_question}"})
        previous_convo.append({"role": "assistant", "content": f"System output: {filtered_result_dict}"})
        response = client.chat.completions.create(
            model="gpt-4o",
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
        "response": "Sorry, I can't provide any information. Please try again.",
    })
                        

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
