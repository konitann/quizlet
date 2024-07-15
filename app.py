from flask import Flask, render_template, request, redirect, url_for, session
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
        
        if user and check_password_hash(user.password, password):
            session['username'] = username
            return redirect(url_for('mypage'))
        else:
            return 'ユーザー名またはパスワードが正しくありません。'
    
    return render_template('login.html')

@app.route("/mypage")
def mypage():
    if 'username' in session:
        username = session['username']
        return f"""
        {username} さん、ログインしました！<br>
        <a href="{url_for('create_question')}">問題作成ページ</a><br>
        <a href="{url_for('view_my_questions')}">作った問題閲覧ページ</a><br>
        <a href="{url_for('view_all_questions')}">問題一覧</a><br>
        <a href="{url_for('view_all_answers')}">解答一覧</a><br>
        <form action="{url_for('logout')}" method="post">
            <button type="submit">ログアウト</button>
        </form>
        """
    else:
        return redirect(url_for('login'))

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    choice1 = db.Column(db.String(200), nullable=False)
    choice2 = db.Column(db.String(200), nullable=False)
    choice3 = db.Column(db.String(200), nullable=False)
    choice4 = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(100), nullable=False)

@app.route("/create_question", methods=['GET', 'POST'])
def create_question():
    if 'username' in session:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            choice1 = request.form['choice1']
            choice2 = request.form['choice2']
            choice3 = request.form['choice3']
            choice4 = request.form['choice4']
            answer = request.form['answer']
            username = session['username']
            
            new_question = Question(
                title=title,
                content=content,
                choice1=choice1,
                choice2=choice2,
                choice3=choice3,
                choice4=choice4,
                answer=answer,
                username=username
            )
            
            try:
                with app.app_context():
                    db.session.add(new_question)
                    db.session.commit()
                return redirect(url_for('mypage'))
            except Exception as e:
                return f'問題の保存中にエラーが発生しました: {e}'
        
        return render_template('create_question.html')
    else:
        return redirect(url_for('login'))

@app.route("/view_my_questions")
def view_my_questions():
    if 'username' in session:
        username = session['username']
        questions = Question.query.filter_by(username=username).all()
        return render_template('created_questions.html', questions=questions)
    else:
        return redirect(url_for('login'))


@app.route("/view_all_questions")
def view_all_questions():
    return "問題一覧ページ"

@app.route("/view_all_answers")
def view_all_answers():
    return "解答一覧ページ"

if __name__ == "__main__":
    # データベースを作成
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8080, debug=True)
