from application import app


if __name__ == '__main__':
    # Note, per docs app.run is not good for production
    app.run(debug=True) 

