## LMS backend setup guide  ----------------------------------
step - 1
install python >= 3.12

step - 2
create virtual environment and activate the virtual environment

for window
python -m venv venv
python\Scripts\activate

for linux/macos
python3 -m venv env
source env/bin/activate

step - 3
install requirements.txt for installing all the packages
pip install requirements.txt

step - 4
run the django server using command

python manage.py runserver