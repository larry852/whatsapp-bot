from flask import Flask, render_template, request, url_for, redirect
import bot


app = Flask(__name__)


@app.route('/')
@app.route('/<again>')
def init(again=None):
    bot.again = True if again else False
    qr = bot.init()
    return render_template('login.html', qr=qr)


@app.route('/contacts')
def get_contacts():

    if bot.login():
        if not bot.again:
            bot.contacts = bot.get_contacts()
    return render_template('contacts.html', total_contacts=len(bot.contacts))


@app.route('/message', methods=['POST', 'GET'])
def send_message():
    if request.method == 'POST':
        message = request.form.get('message')
        last_contact = bot.send_message(message)
        if last_contact is not None:
            index = bot.contacts.index(last_contact)
            bot.contacts = bot.contacts[index:]
            return redirect(url_for('init', again='again'))
        return render_template('finish.html')
    else:
        return render_template('message.html')


if __name__ == "__main__":
    app.run(debug=True)
    # app.run(debug=True, host='0.0.0.0', port=80)
