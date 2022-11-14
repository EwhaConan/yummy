from flask import Flask, render_template, request
import sys
application = Flask(__name__)


@application.route("/")
def hello():
    return render_template("index.html")

@application.route("/index")
def view_list():
    
    
    .3
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


#아래는 과제2 (11/15마감) 제출용 페이지들
@application.route("/menuSubmit", methods=['POST'])
def view_menuSubmit():
    image_file=request.files["menuImg"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    print(data)
    return "입력값이 POST방식으로 잘 넘어왔는지 확인하는 페이지입니다. 여기 말고 터미널을 확인해주세요."

@application.route("/restaurantSubmit", methods=['POST'])
def view_restaurantSubmit():
    image_file=request.files["restaurantImg"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    return render_template("result.html", data=data, image_file_name=image_file.filename)

@application.route("/reviewSubmit", methods=['POST'])
def view_reviewSubmit():
    image_file=request.files["reviewImg"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    print(data)
    return "입력값이 POST방식으로 잘 넘어왔는지 확인하는 페이지입니다. 여기 말고 터미널을 확인해주세요."
    




if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
