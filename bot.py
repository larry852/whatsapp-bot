from webwhatsapi import WhatsAPIDriver

driver = None
contacts = None
again = None


def init():
    global driver
    global contacts
    global again
    try:
        driver.close()
    except Exception:
        pass
    driver = WhatsAPIDriver(client='chrome')
    return driver.get_qr()


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
            name = contact.get_safe_name()
            message_user = message.format(name.split(' ')[0]) if name and name[0].isalpha() else message.format('amigo/a')
            try:
                chat = contact.get_chat()
                chat.send_message(message_user)
            except Exception:
                driver.send_message_by_name_contact(name, message_user)
        except Exception:
            print("Error sending message")
            driver.close()
            return contact
    driver.close()
