from flask import Flask, render_template, request, url_for, redirect
import bot


app = Flask(__name__)

id_last_contact = None
current_token = None

valid_tokens = [
    '9b676be0fe3a7c76a9301b0ea3322f906c62c8f8',
    '29d39f512b14177402b73715e9a4c0fc02a1da5d',
    '3f0c61e93a7aa5ca8a8dd270629611416b843515',
    '0feba91df6ad71c724598d59b65937824d4e8e16',
    '3a781b98ae5fc32e8c040434cfda8a8f694a89c9',
]


def require_token(func):
    def check_token(*args, **kwargs):
        if current_token in valid_tokens:
            return func(*args, **kwargs)
        else:
            return render_template('index.html', unauthorized=True)
    check_token.__name__ = func.__name__
    return check_token


@app.route('/', methods=['POST', 'GET'])
def index():
    global id_last_contact
    global valid_tokens
    global current_token
    if request.method == 'POST':
        current_token = request.form.get('token')
        id_last_contact = request.form.get('id_last_contact')
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login')
@require_token
def login():
    qr = bot.init()
    return render_template('login.html', qr=qr)


@app.route('/contacts')
@require_token
def get_contacts():
    try:
        if bot.login():
            bot.contacts = bot.get_contacts()
            if id_last_contact:
                index_last_contact = next((index for index, contact in enumerate(bot.contacts) if contact.id == id_last_contact), None)
                bot.contacts = bot.contacts[index_last_contact:] if index_last_contact else bot.contacts
        return render_template('contacts.html', total_contacts=len(bot.contacts))
    except Exception:
        return redirect(url_for('login'))


@app.route('/message', methods=['POST', 'GET'])
@require_token
def send_message():
    global current_token
    if request.method == 'POST':
        message = request.form.get('message')
        last_contact = bot.send_message(message)
        if last_contact is not None:
            current_token = None
            return render_template('break.html', last_contact=last_contact)
        current_token = None
        return render_template('finish.html')
    return render_template('message.html')


if __name__ == "__main__":
    app.run(debug=True)
