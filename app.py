from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True  # テンプレートの自動リロードを有効化する場合
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key_here'  # 実際のアプリでは安全な方法で設定してください


db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/")
def index():
    return render_template('que_top.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        
        new_user = User(username=username, password=hashed_password)
        
        try:
            with app.app_context():
                db.session.add(new_user)
                db.session.commit()
            return redirect(url_for('login'))
        except Exception as e:
            return f'登録中にエラーが発生しました: {e}'
    
    return render_template('que_signup.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            if check_password_hash(user.password, password):
                return f'{username} さん、ログインしました！'
            else:
                return 'パスワードが正しくありません。'
        else:
            return 'ユーザーが見つかりません。'
    
    return render_template('login.html')

if __name__ == "__main__":
    # データベースを作成
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
