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
            "img_path":"static/image/"+img_path
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
        for res in menus.each():
            if res.key()==foodname:
                return False
        return True
    
    
    def insert_menu(self, foodname, data, img_path):
        menu_info = { 
            "restaurant":data['restaurantName'],
            "foodprice":data['foodprice'],
            "allergy":data['allergy'],
            "vegan":data['vegan'],
            "img_path":img_path
        }
        if self.menu_duplicate_check(foodname):
            self.db.child("menu").child(foodname).set(menu_info)
            print(data, img_path)
            return True
        else:
            return False
        
    #review check
    
    #식당 이름 넘겨받기
    #넘겨 받은 후, 밑에 주석처리 한 함수 다시 풀기
    def insert_review(self, reviewerName, data, img_path):
        review_info = {
            
            "menu":data['menu'],
            "text":data['text'],
            "rating":data['rating'],
            "img_path":img_path
        }
        self.db.child("review").child(reviewerName).set(review_info)
        print(data, img_path)
        return True
    
    def get_restaurants(self):
        restaurants = self.db.child("restaurant").get().val()
        return restaurants
    
    def get_restaurant_byname(self, name):
        restaurants = self.db.child("restaurant").get()
        target_value=""
        for res in restaurants.each():
            value=res.val()
            
            if value['name'] == name:
                target_value=value
            return target_value
        
    #def get_avgrate_byname(self, name):
        #reviews = self.db.child("review").get()
        #rates=[]
        #for res in reviews.each():
            #value=res.val()
            #if value['menu']==name:
                #rates.append(float(value['rate']))
            #return sum(rates)/len(rates)
    
        
    
        
