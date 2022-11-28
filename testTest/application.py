from flask import Flask, render_template, request, redirect, url_for
from database import DBhandler
import sys
application = Flask(__name__)
app = Flask(__name__)

DB = DBhandler()


@application.route("/")
def hello():
    # return render_template("list.html")
    return redirect(url_for("view_list", page=0))
    
@application.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int) # 페이지 인덱스
    limit = 9 # 한 페이지에 식당 최대 9개
    
    start_idx = limit * page # 이 페이지의 식당 인덱스 (시작)
    end_idx = limit * (page + 1) # 이 페이지의 식당 인덱스 (끝)
    
    data = DB.get_restaurants()
    total_count = len(data) # 레스토랑 총 개수
    page_count = int(((total_count + 8)/ limit)) # 페이지 총 개수
    data = dict(list(data.items())[start_idx:end_idx])
    
    return render_template("list.html", page=page, limit=limit, page_count=page_count, total_count=total_count, datas=data.items())

@application.route("/restaurantRegister")
def view_restaurantRegister():
    return render_template("restaurantRegister.html")

@application.route("/menuRegister", methods=['POST'])
def reg_menu():
    data=request.form
    print(data)
    return render_template("menuRegister.html", data=data)

@application.route("/menuView")
def view_menuView():
    return render_template("menuView.html")

@application.route("/reviewRegister", methods=['POST'])
def view_reviewRegister():
    data=request.form
    return render_template("reviewRegister.html", data=data)

@application.route("/reviewView", methods=['POST'])
def view_reviewView():
    data=request.form
    return render_template("reviewView.html", data=data)

@application.route("/worldCup")
def view_worldCup():
    return render_template("worldCup.html")


#아래는 과제2 (11/15마감) 제출용 페이지들
@application.route("/menuSubmit", methods=['POST'])
def view_menuSubmit():
    global idx
    image_file=request.files["file"]
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
    
    if DB.insert_restaurant(data, data, image_file.filename):
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

@app.route('/dynamicurl/<variable_name>')
def DynamicUrl(variable_name):
    return str(variable_name)

@application.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    
    print("####data:", data)
    return render_template("detail.html", data=data, avg_rate = avg_rate)
    
@application.route("/list_foods/<name>/", methods=['POST'])
def view_foods(name):
   
    data = DB.get_food_byname(str(name))
  #  #tot_count = len(data)
   # #page_count = len(data)
    return render_template("menuView.html", datas=data)


if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)
