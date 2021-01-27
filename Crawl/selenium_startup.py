from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
#無頭模式
# options = webdriver.ChromeOptions()
# options.add_argument("headless")
# desired_capabilities = options.to_capabilities()
# browser = webdriver.Chrome(desired_capabilities = desired_capabilities )

browser = webdriver.Chrome()
#WebDriverWait(browser,3, 0.1).until(ec.presence_of_element_located((By.CLASS_NAME,"flightPageProgressTrackCompleted")))
#soup = BeautifulSoup(browser.page_source,'html.parser')