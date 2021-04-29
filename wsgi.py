from src.web_app import init_app

app = init_app()

if __name__ == "__main__":
    print(("* Starting Flask server..."
           "please wait until server has fully started"))
    app.debug = True
    app.run()
