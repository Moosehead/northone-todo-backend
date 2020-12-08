# northone-todo-backend
Northone backend to-do assessment 

# Setup
1. Create a virtual envrionment `python -m venv venv`
2. Activate the virtual envrionment `source venv/bin/activate`
3. Install dependencies from requirements.txt `pip install -r requirements.txt`
4. To run navigate to root directory and run `python manage.py runserver` (don't worry about migrations we are using a remote database)

# To run console script
1. Make sure server is running on your desired localhost and port (e.g http://127.0.0.1:8000/) 
2. Run shell script `./ep_test.sh`

# To run Tests 
1. To run tests`python manage.py test`

# View Swagger documentation of endpoints
1. Make sure django server is running
2. docs served on http://127.0.0.1:8000/docs/

# Project Docs
-Status as 0 represents to the client pending tasks 
-Status as 1 represents to the client completed tasks
- due date input format is `2020-12-02 09:15:32`
