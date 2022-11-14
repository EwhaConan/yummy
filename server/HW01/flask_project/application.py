from flask import Flask, render_template
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/index")
def view_list():
    return render_template("index.html")

@application.route("/restaurantRegister")
def view_restaurantRegister():
    return render_template("restaurantRegister.html")

@application.route("/detail")
def view_detail():
    return render_template("detail.html")

@application.route("/menuRegister")
def view_menuRegister():
    return render_template("menuRegister.html")

@application.route("/menuView")
def view_menuView():
    return render_template("menuView.html")

@application.route("/reviewRegister")
def view_reviewRegister():
    return render_template("reviewRegister.html")

@application.route("/reviewView")
def view_reviewView():
    return render_template("reviewView.html")

@application.route("/worldCup")
def view_worldCup():
    return render_template("worldCup.html")




if __name__ == "__main__":
    application.run(host='0.0.0.0')
