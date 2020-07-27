from app import app


@app.route('/check/')
def check():
    return "Success"
