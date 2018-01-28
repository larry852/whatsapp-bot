from webwhatsapi import WhatsAPIDriver

driver = WhatsAPIDriver(client='chrome')

driver.wait_for_login()
contacts = driver.get_all_chats()
contacts[1].send_message("Test")
