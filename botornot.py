#find out who is a bot, and who is not

from tweetsql.model import User
from tweetsql.database import db_session
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Firefox()
driver.get("http://truthy.indiana.edu/botornot/")
elem = driver.find_element_by_class_name("form-control")

all_users = db_session.query(User).all()
button = driver.find_element_by_id('btnGetTimeline')

for user in all_users:
	screen_name = user.screen_name.encode('ascii', 'ignore')
	elem.send_keys(screen_name)
	button.click()
	# try:
	# 	print 'waiting'
	# 	element = WebDriverWait(driver, 30).until(
	# 		EC.presence_of_element_located((By.ID, 'span-power-readout'))
	# 	)
	# finally:
	# 	driver.quit()
	# driver.implicitly_wait(10)
	time.sleep(10)
	print 'waiting some more? why...who knows?'
	try:
		perc = driver.find_element_by_id('span-power-readout')
		stringScore = perc.text.encode('ascii', 'ignore')
		numScore = int(stringScore[:-1])
		user.botscore = numScore
		db_session.commit()
		print 'got a bot score of %d for %s' % (numScore, screen_name)
	except:
		print 'poo poo'
	
	#what to do with this perc?



