from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import DBhandler
import hashlib
import sys
app = Flask(__name__)
app.config["SECRET_KEY"] = "yummy"

DB = DBhandler()

top5_list = [] #전역변수라 걱정

@app.before_first_request
def top5_chart():
    datas = DB.get_restaurants()
    rating_dic = {}

    for data in datas.items():
        name = data[1]["name"]
        avg_rate = DB.get_avgrate_byname(str(name))
        if avg_rate == "None":
            avg_rate = 0
        rating_dic[name] = avg_rate
    sorted_dic = sorted(rating_dic.items(), key = lambda item: item[1], reverse=True)

    for i in range(min(5, len(rating_dic))):
        top5_list.append(sorted_dic[i][0])

# route: 시작 페이지
@app.route("/")
def hello():
    # return render_template("list.html")
    return redirect(url_for("view_list", page=0))

# route: 맛집 리스트    
@app.route("/list")
def view_list():
    page = request.args.get("page", 0, type=int) # 페이지 인덱스
    limit = 9 # 한 페이지에 식당 최대 9개
    
    start_idx = limit * page # 이 페이지의 식당 인덱스 (시작)
    end_idx = limit * (page + 1) # 이 페이지의 식당 인덱스 (끝)
    
    data = DB.get_restaurants()
    
    if str(data) == "None": # 예외 처리 : DB에 등록된 맛집이 하나도 없는 상황
        flash("등록된 맛집이 없습니다. 당신의 맛집을 공유해주세요.")
        return redirect(url_for('view_restaurantRegister'))
        
    total_count = len(data) # 레스토랑 총 개수
    page_count = int(((total_count + 8)/ limit)) # 페이지 총 개수
    data = dict(list(data.items())[start_idx:end_idx])

    # print (data)    
    return render_template("list.html", page=page, limit=limit, page_count=page_count, total_count=total_count, datas=data.items(), top5_list=top5_list)


# route: 맛집 등록
@app.route("/restaurantRegister")
def view_restaurantRegister():  
    return render_template("restaurantRegister.html" , top5_list=top5_list)


# route: 메뉴 등록
@app.route("/menuRegister", methods=['POST'])
def reg_menu():
    data=request.form
    # print(data)
    return render_template("menuRegister.html", data=data, top5_list=top5_list)


# route: 리뷰 등록
@app.route("/reviewRegister", methods=['POST'])
def view_reviewRegister():
    data=request.form
    return render_template("reviewRegister.html", data=data, top5_list=top5_list)


# route: 점메추/저메추
@app.route("/worldCup")
def view_worldCup():
    datas = DB.get_restaurants()
    #print(datas)
    dic = []
    for data in datas.items() :
        dic.append(data[1])
    return render_template("worldCup.html", datas = dic, top5_list=top5_list)

# 메뉴/맛집/리뷰 등록 과정에서 DB 받아오는 중간 페이지 (3개)
# 메뉴 등록 과정에서
@app.route("/menuSubmit", methods=['POST'])
def view_menuSubmit():
    global idx
    image_file=request.files["file"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_menu(data['foodname'], data, image_file.filename):
        return view_foods(data["res_name"])
    else:
        return "Menu name is already exist."
    
    
# 맛집 등록 과정에서
@app.route("/restaurantSubmit", methods=['POST'])
def view_restaurantSubmit():
    global idx
    image_file=request.files["file"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_restaurant(data["name"], data, image_file.filename):
        #return render_template("result.html", data=data, image_path="static/image/"+image_file.filename) 
        return redirect(url_for('view_list'))
    else:
        return "Restaurant name already exist!"


# 리뷰 등록 과정에서
@app.route("/reviewSubmit", methods=['POST'])
def view_reviewSubmit():
    image_file=request.files["img"]
    image_file.save("./static/image/{}".format(image_file.filename))
    data=request.form
    
    if DB.insert_review(data['reviewerName'], data, image_file.filename):

        return view_reviewVView(data['name'])
        
    else:
        return "Enter the review!"


# 동적 라우팅
# 각 식당의 경로로 페이지가 라우팅 되도록 필요한 페이지.
@app.route('/dynamicurl/<variable_name>')
def DynamicUrl(variable_name):
    return str(variable_name)


# route: 맛집 상세페이지
@app.route("/view_detail/<name>/")
def view_restaurant_detail(name):
    data = DB.get_restaurant_byname(str(name))
    avg_rate = DB.get_avgrate_byname(str(name))
    
    if str(data) == "None": # 예외 처리
        flash("올바르지 않은 맛집 이름입니다.")
        return redirect(url_for('view_list'))
    # if str(avg_rate) == "None": # 예외 처리
    #     avg_rate = "평점을 계산할 리뷰가 없습니다."
    
    # print("####data:", data)
    return render_template("detail.html", data=data, avg_rate = avg_rate, top5_list=top5_list)
  
    
# route : 메뉴 조회
@app.route("/list_foods/<name>/")
def view_foods(name):
    data = DB.get_food_byname(str(name))
    
    if str(data) == "None": # 예외 처리
        flash("등록된 메뉴가 없습니다.")
        return redirect(url_for('handle_db_none_error', name=name, error_page="메뉴 조회"))
        
    #tot_count = len(data)
    #page_count = len(data)sss
    data = {i : data[i] for i in range(len(data))}
    # print (data)
    return render_template("menuView.html", datas=data.items(), name=name, top5_list=top5_list)

# 에러 처리 페이지 : db에서 받아오는 값이 없을 때 (none)
@app.route("/db_none_error/<name>/<error_page>")
def handle_db_none_error(name, error_page):
    return render_template("db_none_error.html", name=name, error_page=error_page, top5_list=top5_list)

# route : 리뷰 조회
@app.route("/view_reviewVView/<name>/")
def view_reviewVView(name):
    data = DB.get_review_byname(str(name))
    
    if str(data) == "None": # 예외 처리
        flash("등록된 리뷰가 없습니다.")
        return redirect(url_for('handle_db_none_error', name=name, error_page="리뷰 조회"))
    
    data = {i : data[i] for i in range(len(data))}
    
    return render_template("reviewView.html", datas=data.items(), name=name, top5_list=top5_list)



# route: 회원가입
@app.route("/signup")
def signup():
    return render_template("signup.html", top5_list=top5_list)

# 회원가입 시 입력받은 정보를 처리하는 페이지
@app.route("/signup_post", methods=['POST'])
def register_user():
    data=request.form
    pw=request.form['pw']
    pw_hash=hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.insert_user(data, pw_hash):
        return render_template("login.html", top5_list=top5_list)
    else:
        flash("이미 존재하는 아이디입니다! 다른 아이디를 사용해주세요")
    return render_template("signup.html", top5_list=top5_list)

# route: 로그인
@app.route("/login")
def login():
    return render_template("login.html", top5_list=top5_list)

# 로그인 시 입력받은 정보를 처리하는 페이지
@app.route("/login_confirm", methods=['POST'])
def login_user():
    id_=request.form['id']
    pw=request.form['pw']
    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()
    if DB.find_user(id_,pw_hash):   
        session['id']=id_
        return redirect(url_for('view_list'))
    else:
        flash("Wrong ID or PW!")
        return render_template("login.html", top5_list=top5_list)

@app.route("/logout")
def logout_user():
    session.clear()
    return redirect(url_for('view_list'))

    
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
