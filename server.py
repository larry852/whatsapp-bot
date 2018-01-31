from flask import Flask, render_template, request
import bot


app = Flask(__name__)


@app.route('/')
def init():
    qr = bot.init()
    return render_template('login.html', qr=qr)


@app.route('/contacts')
def get_contacts():
    if bot.login():
        bot.contacts = bot.get_contacts()
    return render_template('contacts.html', total_contacts=len(bot.contacts))


@app.route('/message', methods=['POST', 'GET'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        bot.send_message(message)
        return render_template('finish.html')
    else:
        return render_template('message.html')


if __name__ == "__main__":
    app.run()
