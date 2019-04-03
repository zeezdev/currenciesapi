from app.create_app import create_app

app = create_app()


# Start a development web server if executed from the command line
if __name__ == "__main__":
    # Manage the command line parameters such as:
    # - python manage.py runserver
    # - python manage.py db
    from app import manager
    #
    manager.run()
