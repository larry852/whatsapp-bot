from webwhatsapi import WhatsAPIDriver
import shutil

driver = None
contacts = None


def init():
    global driver
    global contacts
    try:
        driver.close()
    except Exception:
        pass
    driver = WhatsAPIDriver(client='chrome')
    qr_tmp = driver.get_qr()
    qr = 'static/qr/{}'.format(qr_tmp.split('/')[-1])
    shutil.move(qr_tmp, qr)
    return qr


def login():
    driver.wait_for_login()
    return True


def get_contacts():
    driver.wait_for_connect()
    contacts = driver.get_contacts()
    return contacts


def send_message(message):
    for contact in contacts:
        try:
            contact.send_message(message)
        except Exception:
            driver.send_message_to_id(contact.id, message)
        # try:
        # name = contact.get_safe_name()
        # message_user = message.format(name.split(' ')[0]) if name and name[0].isalpha() else message.format('amigo/a')
        # except Exception:
        #     print("Error sending message")
        #     driver.close()
        #     return contact
    driver.close()
