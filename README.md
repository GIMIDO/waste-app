## How to run server

To start the server (in DEBUG mode) you need to perform several actions:

- Open the project folder in CMD


- Create migrations:

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

- Create a superuser to access the Django administration panel:

  ```
  python manage.py createsuperuser
  ```

- Start the server:

  ```
  python manage.py runserver
  ```

  or

  ```
  python manage.py runserver ip_address:port
  ```

- Go to the suggested link

## How to switch to Django admin panel

Go to `/admin` and enter superuser credentials