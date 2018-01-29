from webwhatsapi import WhatsAPIDriver
import utils

driver = None
contacts = None


def init():
    global driver
    global contacts
    driver = WhatsAPIDriver(client='chrome')
    return driver.get_qr()


def login():
    driver.wait_for_login()
    return True


def get_contacts():
    driver.wait_for_connect()
    contacts = driver.get_contacts()
    if utils.query_yes_no('Total contacts: ' + str(len(contacts)) + '. Continue?'):
        return contacts


def send_message(message):
    for contact in contacts:
        name = contact.get_safe_name()
        message.format(name)
        try:
            chat = contact.get_chat()
        except Exception:
            chat = None
        print(name)
        print(message)
        print(chat)
        # chat.send_message(message)
