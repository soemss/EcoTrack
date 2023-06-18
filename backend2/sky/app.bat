@echo on
call setup.bat
py -m venv env
CALL env\Scripts\activate
set FLASK_APP=app.py
python -m flask run --host=0.0.0.0 --port=8000
