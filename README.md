#This is a quick guide on how to clone/fork the covid19task

Requirements :  
You need to have a version of python installed
python --version

Installation:

1.  clone the git repo
    git clone https://github.com/mohammadGhanem66/covid19task

2.  Once you've cloned the repository, navigate into the repository.
    Create a virtual environment and activate it using the following commands:

    python -m venv venv
    source venv/Scripts/activate

3.  Once you've activated your virtual environment install your python packages by running:
    pip install -r requirements.txt

4.  Now let's migrate our django project:
    python manage.py makemigrations covidtask
    python manage.py migrate

5.  If there are no hitches here you should now be able to open your server by running:
    python manage.py runserver

API documntation :

- Export and import postman collection & environment variable
- Run the "Generate token" API to generate a new access token .
- Hit any API you need .

Postman collection : https://www.postman.com/mohammadghanemteam/workspace/13bd46ce-595a-4866-bc43-338817aafa50/collection/11892346-9ef1f216-c32f-455d-b887-bf44212a6f32?action=share&creator=11892346

Management Command line :

- To run the management command use the following command
  python manage.py import_cmd

Unit test

- To run the unit test use the folloing command :
  python manage.py test covidtask.tests

Have a nice day 🙂