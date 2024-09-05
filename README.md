# Data Importing
1. To use, please first enter the following command into Shell or Terminal: source myenv/bin/activate (mac); myenv\Scripts\activate (window).
1. To use, please first enter the following command into Shell or Terminal: source myenv/bin/activate (mac); myenv\Scripts\activate (window).
2. If you are using an IDE like Visual Studio Code, ensure that it is using the Python interpreter from your virtual environment.
3. To run any script, please type ./myenv/bin/python ImportScripts/[script_name].py into Shell or Ternimal.
4. To delete data from a table please type ./myenv/bin/python ImportScripts/table_reset.py [name_of_the_table]
5. When you are done please type: deactivate

OR 

Install psycopg2 using: pip install psycopg2. (Try pip3 install psycopg2 if doesn't work) -> Can't confirm.