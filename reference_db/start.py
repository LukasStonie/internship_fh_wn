import app

application = app.create_app()
application.run(port=5533, debug=True)
