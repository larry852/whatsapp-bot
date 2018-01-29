from flask import Flask, render_template, request
import bot


app = Flask(__name__)


@app.route('/')
def root():
    return render_template('index.html', url='#')


@app.route('/start')
def init():
    qr = bot.init()
    return render_template('index.html', qr=qr, url='#qr')


@app.route('/contacs')
def get_contacts():
    if bot.login():
        login = True
        while bot.contacts is None:
            bot.contacts = bot.get_contacts()
    else:
        login = False
    return render_template('index.html', login=login, total_contacts=len(bot.contacts))


@app.route('/message', methods=['POST'])
def send_message():
    done = False
    if request.method == 'POST':
        message = request.form.get('message')
        bot.send_message(message)
        done = True
    return render_template('index.html', done=done)
