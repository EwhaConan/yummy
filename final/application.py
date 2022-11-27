from flask import Flask, render_template, request
from database import DBhandler
import sys
application = Flask(__name__)

DB = DBhandler()


@application.route("/")
def hello():
    return render_template("list.html")

@application.route("/index")
def view_list():
    return render_template("list.html")

@application.route("/restaurantRegister")
def view_restaurantRegister():
    return render_template("restaurantRegister.html")

@application.route("/detail")
def view_detail():
    return render_template("detail.html")

@application.route("/menuRegister", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("menuRegister.html", data=data)


#@application.route("/menuRegister")
#def view_menuRegister():
    #return render_template("menuRegister.html")


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


#아래는 과제2 (11/15마감) 제출용 페이지들
@application.route("/menuSubmit", methods=['POST'])
def view_menuSubmit():
    global idx
    image_file=request.files["img"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_menu(data['foodname'], data, image_file.filename):
        return render_template("menuResult.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Menu name is already exist."
    
    
@application.route("/restaurantSubmit", methods=['POST'])
def view_restaurantSubmit():
    global idx
    image_file=request.files["file"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data['name'], data, image_file.filename):
        return render_template("result.html", data=data, image_path="static/image/"+image_file.filename) 
    else:
        return "Restaurant name already exist!"

@application.route("/reviewSubmit", methods=['POST'])
def view_reviewSubmit():
    image_file=request.files["img"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_review(data['reviewerName'], data, image_file.filename):
        return render_template("reviewResult.html", data=data, image_path="static/image/"+image_file.filename)
    else:
        return "Enter the review!"




if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
