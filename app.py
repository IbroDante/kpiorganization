from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # For flash messages in contact form

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Simple form handling (in production, add email sending)
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        flash('Thank you for your message! We will get back to you soon.', 'success')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)