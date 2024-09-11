import os
from functools import wraps
from flask import Flask, jsonify, Response, request, redirect, url_for
import flask
from cache import MemoryCache
import psycopg2
from openai import OpenAI
from vanna.remote import VannaDefault

app = Flask(__name__, static_url_path='')

openai_api_key = os.getenv('OPENAI_API_KEY')
vanna_api_key = os.getenv('VANNA_API_KEY')

# SETUP
cache = MemoryCache()
vanna_model_name = 	"unimelb-handbook-chatbot"

# class MyVanna(VannaDB_VectorStore, OpenAI_Chat):
#     def __init__(self, config=None):
#         MY_VANNA_MODEL = vanna_model_name
#         VannaDB_VectorStore.__init__(self, vanna_model=MY_VANNA_MODEL, vanna_api_key=api_key, config=config)
#         OpenAI_Chat.__init__(self, config=config)
#
# vn = MyVanna(config={'api_key': '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', 'model': 'gpt-4o-mini'})

vn = VannaDefault(model=vanna_model_name, api_key=vanna_api_key)
vn.connect_to_postgres(dbname="postgres",user="postgres.seqkcnapvgkwqbqipqqs",password="IT Web Server12",host="aws-0-ap-southeast-2.pooler.supabase.com",port=6543)
# NO NEED TO CHANGE ANYTHING BELOW THIS LINE
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

@app.route('/api/v0/generate_questions', methods=['GET'])
def generate_questions():
    generate_questions = vn.generate_questions()
    return jsonify({
        "type": "question_list",
        "questions": generate_questions,
        "header": "Here are some questions you can ask:"
        })

@app.route('/api/v0/generate_sql', methods=['GET'])
def generate_sql():
    user_question = flask.request.args.get('question')
    # Step 1: Generate the SQL query from the user question
    sql = vn.generate_sql(user_question)

    valid = vn.is_sql_valid(sql=sql)

    if valid:
        conn = psycopg2.connect(database="postgres",user="postgres.seqkcnapvgkwqbqipqqs",password="IT Web Server12",host="aws-0-ap-southeast-2.pooler.supabase.com",port=6543)
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()

        cur.close()
        conn.close()

        client = OpenAI(
            api_key=openai_api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system",
                "content": "You are a university handbook assistant chatbot, you help student find subject information, you are providing formal and precise response corresponding to the user input, you are now asked to convert the following text into a more colloquial response and do not include 'sure', response in markdown format."},
                {"role": "user", "content": f"User input: {user_question}"},
                {"role": "assistant", "content": f"System output: {result}"}
            ]
        ).choices[0].message.content
        return jsonify({
            "response": response
        })

    # Step 5: Return the OpenAI response as a JSON response
    return jsonify({
        "response": "Sorry, I can't answer that question currently."
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

@app.route('/api/v0/get_question_history', methods=['GET'])
def get_question_history():
    return jsonify({"type": "question_history", "questions": cache.get_all(field_list=['question']) })

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(debug=True)
