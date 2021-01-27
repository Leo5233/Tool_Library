import pymysql
from flask import Flask, request, render_template
from flask import url_for, redirect
from flask_login import LoginManager, UserMixin, login_user
from flask_login import logout_user, login_required, current_user

# 執行logout_user()會跳過user_loader 
app = Flask(__name__)
#flask_login會使用到session要配上secret_key
app.secret_key = "your_secret_key" 
# secret_key 要配上 user_loader 或 request_loader
login_manager = LoginManager(app) 
# 等於login_manager = LoginManager()
# login_manager.init_app(app)

#撈資料庫
conn = pymysql.connect(host='localhost', user='my', database='test', password='root', charset='utf8')
cur = conn.cursor()
cur.execute("SELECT EM_USERID, EM_PSW FROM EMPLOYEE;")
users = cur.fetchall()
usersinfo = {'user_id':[i[0] for i in users], 'password':[i[1] for i in users]}
cur.close()
conn.close()

# 每次發送request都會跑一次@login_manager.user_loader 
# 如果最後return None 就會跑@login_manager.request_loader
# 這裡面產生的UserMixin()物件會是自動激活狀態(.is_active .is_authenticated都會改T)，如果最後return UserMixin()物件 表示登入成功
# 就不會再去跑@login_manager.request_loader
@login_manager.user_loader
def user_loader(user_id):# user_id為表單資料的['user_id']
    # user_loader是特殊method，雖然接受的是UserMixin() 但會自動取出其中的.id屬性
    print("檢查登入狀態")
    user = UserMixin()
    user.id = user_id # 產生新的UserMixin()預設是沒有.id這個東西，但在自身的method中卻需要用到, 要補給他才會在current_user.id有紀錄
    # user.is_anonymous 匿名用戶為T 登入用戶為 F
    # user.is_active 帳號啟用 且 登入成功
    # user.get_id() == user.id
    # .is_authenticated是個T/F 這個是辨認有無登入的關鍵 為T時才可以使用@login_required method
    return user

# 只有這裡接收的到request的表單資料
@login_manager.request_loader
def request_loader(request):
    pass

@app.route('/', methods=['GET'])
def home():
    return render_template("login.html")

# 必須將表單資料POST到這個callback驗證帳密
@app.route("/login", methods=['POST'])
def verify():
    print('try login')
    user_id = request.form['user_id']# Flask.request
    if ((user_id in usersinfo['user_id']) 
            and (request.form['password'] == users[usersinfo['user_id'].index(user_id)][1])):
        # 如果帳密符合資料庫內容 就產生一個UserMixin()紀錄Session 存取id
        user = UserMixin()
        user.id = user_id
        # 會將Session送到@login_manager.user_loader 將其激活
        login_user(user)#需要@login_manager.user_loader來接收資料 
        print('驗證成功')
        return redirect(url_for('success'))# 這裡的from_start是指method名稱
    else:
        return redirect(url_for('fail'))

@app.route('/logout')
def logout():
    print("logout")
    logout_user()# 會先去跑一次@login_manager.user_loader
    # 接著會將Session資訊刪掉 user.is_authenticated 改回False
    return render_template('login.html') 

@app.route("/success")
@login_required # 加上這行若沒登入卻要連的話會出現302物件已(自動)移動，url會改變成待login狀態
def success():
    a = current_user.id
    print(a)
    return render_template('home.html')

@app.route("/fail", methods=['GET','POST'])
def fail():
    print("帳密不正確")
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run()
