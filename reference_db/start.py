import app

if __name__ == '__main__':
    application = app.create_app()
    application.run(port=5533, debug=True)
