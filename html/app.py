from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
import sqlite3
import validators
import bcrypt
from oauth2client import client, crypt  # 确保已经安装了oauth2client库




app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # 使用强密钥


HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    
    <title>Web Link Shorten</title>
    <style>
        body {
            text-align: center;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }
        .container {
            width: 50%;
            margin: 0 auto;
        }
        table {
            border: 1px solid black;
            border-collapse: collapse;
            width: 100%;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid black;
            padding: 10px;
            text-align: left;
        }
        .button {
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border: none;
            background-color: #4CAF50; /* Green */
            color: white;
            transition: background-color 0.3s;
        }
        .button-clicked {
            background-color: #555555; /* Dark Gray */
        }
    </style>
    <script>
        function changeButtonColor() {
            var button = document.getElementById("submitButton");
            button.classList.add("button-clicked");
        }

        function resetButtonColor() {
            var button = document.getElementById("submitButton");
            button.classList.remove("button-clicked");
        }
    </script>
</head>
<body>

    <div class="container">
        <h2>Web Link Shorten</h2>
        <form id="linkForm">
            <table>
                <tr>
                    <th>Input your link</th>
                    <th>Your shorten link</th>
                </tr>
                <tr>
                    <td>
                        <input type="text" id="inputLink" placeholder="Input link">
                        <button type="button" id="submitButton" class="button" onclick="changeButtonColor(); submitLink();"
                                onmouseleave="resetButtonColor()">Submit</button>
                    </td>
                    <td><span id="shortenedLink">Your shorten link is here</span></td>
                </tr>
            </table>
        </form>
    </div>
    
    <script>
        # function submitLink() {
        #     // Example placeholder function for link submission
        #     // In a real application, you would send a request to your backend here
        #     var inputLink = document.getElementById("inputLink").value;
        #     document.getElementById("shortenedLink").textContent = "Shortened version of " + inputLink;
        #     // Reset the button color after submitting
        #     resetButtonColor();
        # }
        
        function submitLink() {
    var inputLink = document.getElementById("inputLink").value;
     if (!isValidUrl(inputLink)) {
                alert("It is not a correct URL form please check your input.");
                return;
            }
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: 'url=' + encodeURIComponent(inputLink)
    })
    .then(response => {
        if (!response.ok) {
            if(response.status === 400) {
                // 处理400 Bad Request响应
                return response.json().then(data => {
                    alert(data.error);
                });
            }
            throw new Error('Request failed with status: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        document.getElementById("shortenedLink").textContent = data.short_url;
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred: ' + error.message);
    });

    resetButtonColor();
}
    </script>
    
    </body>
</html>
'''
def base62_encode(num, base=62):
    characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    base62 = ''
    while num > 0:
        num, i = divmod(num, base)
        base62 = characters[i] + base62
    return base62

def create_connection():
    """创建并返回一个数据库连接"""
    conn = sqlite3.connect('database.db')
    return conn

# def init_db():
#     """初始化数据库，创建表"""
#     conn = create_connection()
#     c = conn.cursor()
#     c.execute('''CREATE TABLE IF NOT EXISTS url_mapping (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     original_url TEXT NOT NULL,
#                     short_path TEXT NOT NULL
#                 );''')
#     conn.commit()
#     conn.close()
def init_db():
    """初始化数据库并创建表。"""
    conn = create_connection()
    c = conn.cursor()

    # 创建或确保 url_mapping 表存在
    c.execute('''
        CREATE TABLE IF NOT EXISTS url_mapping (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_url TEXT NOT NULL,
            short_path TEXT NOT NULL
        );
    ''')

    # 创建或确保 users 表存在
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')

    conn.commit()
    conn.close()


def insert_url_mapping(original_url, short_path):
    """插入一条新的URL映射记录"""
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO url_mapping (original_url, short_path) VALUES (?, ?)', (original_url, short_path))
    conn.commit()
    conn.close()

def query_original_url(short_path):
    """根据短路径查询原始URL"""
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT original_url FROM url_mapping WHERE short_path=?', (short_path,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None


def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def check_password(hashed_password, user_password):
    """Check if the provided password matches the hashed one."""
    return bcrypt.checkpw(user_password.encode(), hashed_password)

def create_connection():
    """Create and return a database connection."""
    # Replace 'database.db' with your actual database file
    conn = sqlite3.connect('database.db')
    return conn

def register_user(username, email, password):
    """Register a new user with the given username, email, and password."""
    conn = create_connection()
    try:
        c = conn.cursor()
        # Assuming you have a function to hash the password
        hashed_password = hash_password(password)
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError as e:
        # This happens if the username or email is already in use
        return False
    finally:
        conn.close()
    return True

def check_user(username, password):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT password FROM users WHERE username=?', (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password(user[0], password):
        return True
    return False

def cleanup_test_data(original_url, short_path):
    """clean up data while testing"""
    conn = create_connection()
    sql = 'DELETE FROM url_mapping WHERE original_url = ? AND short_path = ?'
    try:
        c = conn.cursor()
        c.execute(sql, (original_url, short_path))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     if request.method == 'POST':
#         original_url = request.form['url']
#         conn = create_connection()
#         with conn:
#             cursor = conn.cursor()
#             # 先生成短路径
#             short_id = cursor.execute("INSERT INTO url_mapping (original_url, short_path) VALUES (?, '')", (original_url,)).lastrowid
#             short_path = base62_encode(short_id)
#             # 然后立即更新刚刚插入的记录的short_path
#             cursor.execute("UPDATE url_mapping SET short_path = ? WHERE id = ?", (short_path, short_id))
#             conn.commit()
#             short_url = request.host_url + short_path
#             return jsonify({'short_url': short_url})
#     # POST请求的处理逻辑保持不变
#     else:
#         return render_template('index.html')

# @app.route('/<short_path>')
# def redirect_to_url(short_path):
#     original_url = query_original_url(short_path)
#     if original_url:
#         return redirect(original_url)
#     return 'URL not found', 404

# if __name__ == '__main__':
#     init_db()  # 确保数据库和表在应用启动前已创建
#     app.run(debug=True)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']

        # 检查URL是否有效
        if not validators.url(original_url):
            return jsonify({'error': 'Invalid URL'}), 400  # 返回400 Bad Request

        # 处理有效URL
        conn = create_connection()
        with conn:
            cursor = conn.cursor()
            short_id = cursor.execute("INSERT INTO url_mapping (original_url, short_path) VALUES (?, '')", (original_url,)).lastrowid
            short_path = base62_encode(short_id)
            cursor.execute("UPDATE url_mapping SET short_path = ? WHERE id = ?", (short_path, short_id))
            conn.commit()
            short_url = request.host_url + short_path
            return jsonify({'short_url': short_url})

    else:  # 处理GET请求
        return render_template('index.html')  # 

@app.route('/<short_path>')
def redirect_to_url(short_path):
    original_url = query_original_url(short_path)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if register_user(username, email, password):
            return redirect('/login')
        else:
            return 'Registration failed. The username or email may already be in use.', 400
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
           session['username'] = username  # Storing username in session
           return render_template('logout.html')
        else:
            return 'Login failed. Check your username and password.', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # 清除用户名
    session.pop('user_id', None)  # 如果您还设置了这个，也清除
    return render_template('index.html')
    #return redirect(url_for('login'))  # 或者重定向到您希望的页面

#google
@app.route('/google-login', methods=['POST'])
def google_login():
    token = request.form['idtoken']
    try:
        idinfo = client.verify_id_token(token, "926635167420-4lou1l0scb3qco72m9v8aqkh4g9qpl9h.apps.googleusercontent.com")

        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise crypt.AppIdentityError("Wrong issuer.")

        userid = idinfo['sub']
        # 假设您想使用 Google 用户的邮箱作为用户名
        session['username'] = idinfo.get('email', 'Unknown')

        # 返回重定向的URL
        return jsonify({'redirect': url_for('logout')})

    except crypt.AppIdentityError:
        return '无效的登录尝试', 401


if __name__ == '__main__':
    init_db()  # 
    app.run(debug=True)