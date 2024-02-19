from flask import Flask, request, redirect, jsonify, render_template
import sqlite3
import validators


app = Flask(__name__)


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
        function submitLink() {
            // Example placeholder function for link submission
            // In a real application, you would send a request to your backend here
            var inputLink = document.getElementById("inputLink").value;
            document.getElementById("shortenedLink").textContent = "Shortened version of " + inputLink;
            // Reset the button color after submitting
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
    """Create and return a database connection"""
    conn = sqlite3.connect('database.db')
    return conn

def init_db():
    """Initialize the database and create tables"""
    conn = create_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS url_mapping (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_url TEXT NOT NULL,
                    short_path TEXT NOT NULL
                );''')
    conn.commit()
    conn.close()

def insert_url_mapping(original_url, short_path):
    """Insert a new URL mapping record"""
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO url_mapping (original_url, short_path) VALUES (?, ?)', (original_url, short_path))
    conn.commit()
    conn.close()

def query_original_url(short_path):
    """Query the original URL based on the short path"""
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT original_url FROM url_mapping WHERE short_path=?', (short_path,))
    row = c.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['url']

        # Check if the URL is valid
        if not validators.url(original_url):
            return jsonify({'error': 'Invalid URL'}), 400  # 返回400 Bad Request

        # Handle valid URL
        conn = create_connection()
        with conn:
            cursor = conn.cursor()
            short_id = cursor.execute("INSERT INTO url_mapping (original_url, short_path) VALUES (?, '')", (original_url,)).lastrowid
            short_path = base62_encode(short_id)
            cursor.execute("UPDATE url_mapping SET short_path = ? WHERE id = ?", (short_path, short_id))
            conn.commit()
            short_url = request.host_url + short_path
            return jsonify({'short_url': short_url})

    else:  # Handle GET requests
        return render_template('index.html')  # 
        
@app.route('/<short_path>')
def redirect_to_url(short_path):
    original_url = query_original_url(short_path)
    if original_url:
        return redirect(original_url)
    return 'URL not found', 404

if __name__ == '__main__':
    init_db()  #Make sure the database and tables are created before the application starts
    app.run(debug=True)

def cleanup_test_data(original_url, short_path):
    """Remove test data based on original URL and short path"""
    conn = create_connection()
    try:
        c = conn.cursor()
        c.execute('DELETE FROM url_mapping WHERE original_url = ? AND short_path = ?', (original_url, short_path))
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()
