#from lib2to3.pgen2 import driver
from optparse import OptionError
from ssl import Options
from zipapp import create_archive
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re as re
import time
import pandas as pd



#PATH = "C:\\Users\\Fabio\\Documents\\Software\\webdriver\\msedgedriver.exe"
USERNAME = "your email"
PASSWORD = "your password"
print(PATH)
print(USERNAME)
print(PASSWORD)

driver = webdriver.Edge(executable_path = "C:\\Users\\Fabio\\Documents\\Software\\webdriver\\msedgedriver.exe") # replace for your path to webdriver
driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)
#driver.close

driver.maximize_window()


email=driver.find_element_by_id("username")
email.send_keys(USERNAME)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
time.sleep(1)
password.send_keys(Keys.RETURN)
time.sleep(1)



jobs_link = driver.find_element(by=By.LINK_TEXT, value='Empleos')
jobs_link.click()
time.sleep(1)


driver.get('https://www.linkedin.com/jobs/search/?currentJobId=2965051237&f_AL=true&f_TPR=r2592000&f_WT=2&geoId=91000006&keywords=analyst%22&location=Alemania%2C%20Austria%20y%20Suiza&sortBy=DD')


search_keyword = driver.find_element(by=By.XPATH, value ="//input[starts-with(@id,'jobs-search-box-keyword')]")
search_keyword.clear()
search_keyword.send_keys('"data analyst"')
time.sleep(1)

search_location = driver.find_element(by=By.XPATH, value ="//input[starts-with(@id,'jobs-search-box-location')]")
search_location.clear()
search_location.send_keys("Reino Unido")
time.sleep(1)
search_location.send_keys(Keys.ENTER)
time.sleep(1)





"""This function finds all the offers through all the pages result of the search and filter"""

# find the total amount of results (if the results are above 24-more than one page-, we will scroll trhough all available pages)
total_results = driver.find_element(by=By.CLASS_NAME, value="display-flex.t-12.t-black--light.t-normal")
total_results_int = int(total_results.text.split(' ',1)[0].replace(",",""))
print(total_results_int)

time.sleep(2)
# get results for the first page
current_page = driver.current_url
results = driver.find_elements(by=By.CLASS_NAME, value="jobs-search-results__list-item.occludable-update.p0.relative.ember-view")
# for each job add, submits application if no questions asked

for result in results:
    hover = ActionChains(driver).move_to_element(result)
    hover.perform()
    time.sleep(0.5)
    titles = result.find_elements(by=By.CLASS_NAME, value='disabled.ember-view.job-card-container__link.job-card-list__title')
    for title in titles:
        title.click()
        time.sleep(1)
        try:
            in_apply = driver.find_element_by_css_selector(".jobs-apply-button--top-card button")
            in_apply.click()
        except NoSuchElementException:
            #print('You already applied to this job, go to next...')
            pass
        time.sleep(1)
        
        
        # try to submit if submit application is available...
        try:
            submit = driver.find_element_by_xpath("//button[@aria-label='Enviar solicitud']/span[@class='artdeco-button__text']")
            submit.click()
            time.sleep(3)
            close_dialog = driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
            close_dialog.send_keys(Keys.ENTER)
            time.sleep(1)
        
        # ... if not available, discard application and go to next
        except NoSuchElementException:
            print('Not direct application, going to next...')
            try:
                discard = driver.find_element_by_xpath("//button[@data-test-modal-close-btn]")
                discard.send_keys(Keys.RETURN)
                time.sleep(1)
                discard_confirm = driver.find_element_by_xpath("//button[@data-test-dialog-primary-btn]")
                discard_confirm.send_keys(Keys.RETURN)
                time.sleep(1)
            except NoSuchElementException:
                pass

        time.sleep(2)

time.sleep(5)

driver.close

