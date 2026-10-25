from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = "dev-secret-key"

# Dummy function so {{ csrf_token() }} in your form doesn't crash Flask
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=lambda: "dummy-csrf-token")

@app.route('/')
def index():
    return render_template('index.html')

# Catch-all route so clicking links or submitting forms won't break the page
@app.route('/submit-enquiry', methods=['GET', 'POST'])
@app.route('/<path:dummy>')
def fallback(dummy=None):
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)