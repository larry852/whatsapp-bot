from PIL import Image
from webwhatsapi import WhatsAPIDriver
import utils

driver = None


def init():
    global driver
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


def send_message(contacts):
    for contact in contacts:
        name = contact.get_safe_name()
        message = "Hola " + name
        try:
            chat = contact.get_chat()
        except Exception:
            chat = None
        print(message)
        print(chat)
        # chat.send_message(message)


if __name__ == "__main__":
    contacts = None
    qr = init()
    viewer = Image.open(qr)
    viewer.show()
    if login():
        while contacts is None:
            contacts = get_contacts()
        send_message(contacts)
