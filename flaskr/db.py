'''
データベースを操作するために必要なコネクション(connection)ていうリモコン作成
'''
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

#コネクションの作成。一回実行すると、2回目以降は一回めのコネクションを再利用する。
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

#コネクションがあったら閉じる
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#sqlファイル(schema.sql)内のコマンドを実行する関数
def init_db():
    db = get_db()
    #相対パスでsqlファイルを指定
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#init-dbと呼ばれる、コマンドラインから使用できるコマンドを定義
@click.command('init-db')
@with_appcontext
#init_dbコマンドを実行すると、上のsqlファイルが実行が成功したことのメッセージを表示
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#__init__.pyにあるappというインスタンスにclose_dbとinit_db_command関数を登録
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
