# A FULL BLOWN ONLINE MAGAZINE WITH RICH  INTERNAL FEATURES BUILT IN

This is an online magazine website with built-in **AUTOMATED EMAIL SENDER to send personalised news updates to subscribers**. Users can subscribe to their preferred kinds of news.

During production stage, **Google Cloud** is used to serve media files.
Visit website https://tidings.herokuapp.com/

## Follow these steps to run this project on your local machine

1. Clone repo and execute the following commands on your shell/terminal

```json
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
2. Fill in the necessary data in .env file
3. Go to settings.py in blogman directory and change value of DEBUG to True
