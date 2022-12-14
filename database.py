import pyrebase
import json

class DBhandler:
    def __init__(self):
        with open('./authentication/firebase_auth.json') as f:
            config=json.load(f)
        
        firebase = pyrebase.initialize_app(config)
        self.db = firebase.database()
        
    #restaurant check
    def restaurant_duplicate_check(self, name):
        restaurants = self.db.child("restaurant").get()
        if str(restaurants.val()) == "None": # 예외 처리 : DB에 등록된 맛집이 하나도 없는 상황
            return True
        
        for res in restaurants.each():
            value = res.val()
            if value['name'] == name:
                return False
        return True

    
    def insert_restaurant(self, name, data, img_path):
        restaurant_info = {
            "name": name,
            "addr":data['addr'],
            "tel":data['tel'],
            "category":data['category'],
            "money":data['money'],
            "park":data['park'],
            "time":data['time'],
            "site":data['site'],
            "img_path":img_path
        }
        if self.restaurant_duplicate_check(name):
            self.db.child("restaurant").push(restaurant_info)
            print(data, img_path)
            return True
        else:
            return False
        
    #menu check
    
    def menu_duplicate_check(self, foodname):
        menus = self.db.child("menu").get()

        if str(menus.val()) == "None": # 예외 처리 : DB에 등록된 메뉴가 하나도 없는 상황
            return True
        
        for res in menus.each():
            value = res.val()
            if value['foodname'] == foodname:
                return False
        return True
    
    
    def insert_menu(self, foodname, data, img_path):
        menu_info = {
            "foodname":foodname,
            "res_name":data['res_name'],
            "foodprice":data['foodprice'],
            "allergy":data['allergy'],
            "vegan":data['vegan'],
            "img_path":"/static/image/"+img_path
        }

        self.db.child("menu").push(menu_info)
        print(data, img_path)
        return True
        
        #if self.menu_duplicate_check(foodname):
         #   self.db.child("menu").push(menu_info)
          #  print(data, img_path)
           # return True
        #else:
         #   return False
        
    #review check
    
    #식당 이름 넘겨받기
    #넘겨 받은 후, 밑에 주석처리 한 함수 다시 풀기
    def insert_review(self, reviewerName, data, img_path):
        review_info = {
            "reviewerName": reviewerName,
            "name":data['name'],
            "menu":data['menu'],
            "text":data['text'],
            "rating":data['rating'],
            "img_path":img_path
        }
        self.db.child("review").push(review_info)
        print(data, img_path)
        return True
    
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        if str(restaurants) == "None":
            return "None"
        return restaurants
    
    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        
        if str(restaurants.val()) == "None":
            return "None"
        
        target_value=""
        for res in restaurants.each():
            value=res.val()
            
            if value['name'] == name:
                target_value=value
        return target_value


   # def get_food(self):
       ## menus = self.db.child("menu").get().val()
       # return menus

    def get_food_byname(self, name):
        restaurants = self.db.child("menu").get()
        target_value=[]
        
        if str(restaurants.val()) == "None": # 예외 처리 : DB에 등록된 메뉴가 아예 없을 때
            return "None"
        
        for res in restaurants.each():
            value = res.val()
            print(value)
            if value.get("res_name") == name:
                target_value.append(value)

        if target_value == []: # 예외 처리 : 해당 맛집에 등록된 메뉴가 없을 때
            return "None"

        return target_value

    def get_review_byname(self, name):
        restaurants = self.db.child("review").get()
        target_value=[]
        
        if str(restaurants.val()) == "None": # 예외 처리 : DB에 등록된 리뷰가 아예 없을 때
            return "None"
        
        for res in restaurants.each():
            value=res.val()
            print(value)
            if value.get("name") == name:
                target_value.append(value)
        
        if target_value == []: # 예외 처리 : 해당 맛집에 등록된 리뷰가 없을 때
            return "None"
        
        return target_value
        
        
    def get_avgrate_byname(self, name):
        reviews = self.db.child("review").get()
        rates=[]

        if str(reviews.val()) == "None": # 예외 처리 : DB에 등록된 리뷰가 아예 없을 때
            return "None"
        
        for res in reviews.each():
            value=res.val()
            if value['name']==name:
                rates.append(float(value['rating']))
                
        if len(rates) <= 0: # 예외 처리 : 해당 맛집에 등록된 리뷰가 없을 때
            return "None"
        else :
            return round(sum(rates)/len(rates) ,1 )
        
        
    def insert_user(self, data, pw):
        user_info={
            "id":data['id'],
            "pw":pw,
            "nickname":data['nickname']
        }
        if self.user_duplicate_check(str(data['id'])):
            self.db.child("user").push(user_info)
            print(data)
            return True
        else:
            return False
        
    def user_duplicate_check(self, id_string):
        users=self.db.child("user").get()
        
        print("users###", users.val())
        if(str(users.val())) == "None":#first registeration
            return True
        else:
            for res in users.each():
                value=res.val()
                
            if value['id'] == id_string:
                return False
        return True
   
    def find_user(self, id_, pw_):
        users = self.db.child("user").get()
        target_value=[]
        for res in users.each():
            value = res.val()
        if value['id'] == id_ and value['pw'] == pw_:
            return True
        return False