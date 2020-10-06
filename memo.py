'''
SQLiteデータベース（および殆どのPythonの他のデータベースライブラリ）を使って作業するとき最初にすることは、
データベースへの接続（connection）の作成です。
どのような問合せ（queries）や操作（operations）も、
connectionを使用しながら実施され、作業が終了した後はconnectionが閉じられ（close）ます。
'''

'''
[mvcフレームワーク]
m = model　データ処理と操作
v = view　　出力部。returnのとこ。
c = controller　modelとviewを繋ぐ管理者
https://se-shine.net/what-mvc/#MVC-3
'''
#controller
@bp.route('/register', methods=('GET', 'POST'))
#model
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    #view
    return render_template('auth/register.html')

'''
Blueprintとは
(目的)ブループリントはアプリケーションを構造化するため
(行動)Pythonフォルダをモジュール化するモジュール
(結果)アプリケーションのURLを分けて管理できる
https://creepfablic.site/2019/08/13/python-flask-blueprint/

下記のような記述で127.0.0.1:5000にアクセスした際は，
127.0.0.1:5000ではHELLOと出力
127.0.0.1:5000/makeではSuccessと出力されます。
'''
#--------------------------------
#app.py(メインで実行させるファイル)
# Flaskのインポート
from flask import Flask
#他モジュール(.py)のインポート
from app_module import module_api  #追加モジュール

app = Flask(__name__)

#他モジュール(.py)から呼び出す
app.register_blueprint(module_api)

#あとはレンダリング等の処理を記述
@app.route('/')
def login():
    return "HELLO"

#--------------------------------------
#app_module.py(モジュール化させたいPythonファイル)
# Flaskのインポート，Blueprintのインポート
from flask import Flask, Blueprint

#Blueprintでモジュールの登録
module_api = Blueprint('app_module', __name__)

#レンダリング処理を記述
@module_api.route("/make")
def module_make():
    return "Success"
#----------------------------
'''
おまけ　67行目
url_prefix='追加したいpath'で、127.0.0.1:5000/add/makeでSuccessの表示が可能となりました。
'''
module_api = Blueprint('app_module', __name__, url_prefix='/add')

'''
○ファイルの理解
auth.py
○フォルダの理解
auth　　　
template　htmlのファイル作成
'''

#render_template()   これより前に処理を書き、処理後、()に、templateを投げて、()内のファイルを表示させる。

'''
・動的と静的とは
実行してみないと変数や属性に代入されているオブジェクトの型がわからないのが「動的型付け」
実行する前から変数や属性に代入されているオブジェクトの型がわかっているのが「静的型付け」
'''

'''
・jinjaとは  https://python.ms/dynamic-and-static/#_1-%E9%81%95%E3%81%84
htmlファイルをPythonを使って操作することができるflask内の機能
htmlファイルにある
{{ }}には、静的ファイル(定義済みのファイル)
{% %}には、Pythonの構文が書ける
'''