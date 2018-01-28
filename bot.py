from webwhatsapi import WhatsAPIDriver

driver = WhatsAPIDriver(client='chrome')
driver.wait_for_login()
contacts = driver.get_contacts()
print("Contacts: " + str(len(contacts)))
contacts[11].send_message("Test")
