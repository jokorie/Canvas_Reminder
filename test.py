from selenium import webdriver
from bs4 import BeautifulSoup
import yaml
import time

options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
# options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

# canvas login page
driver.get("https://google.com")

def button_click(driver, xpath):
    button = driver.find_element('xpath', xpath)
    button.click()

def login(usernameId, username, passwordId, password, submit_buttonId):
    login_button = driver.find_element('xpath', "/html/body/div/div/div[3]/div/div/div/div/div/section/div/div/div/article/div/div/table/tbody/tr[2]/td/a")
    login_button.click()
   
    driver.find_element('xpath', usernameId).send_keys(username)
    driver.find_element('xpath', passwordId).send_keys(password)
    driver.find_element('xpath', submit_buttonId).click()

def duo_two_step(driver):
    count = 0
    time.sleep(2)
    while count < 2:
        try:
            iframe = driver.find_element('xpath', '//*[@id="duo_iframe"]')
            driver.switch_to.frame(iframe)

            duo_button = driver.find_element('xpath', '/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button')
            duo_button.click()
            print("completed")
            time.sleep(10)
            return driver.page_source
        except:
            count += 1
            continue            
    print("Duo Authentification Failed. Quitting")
    quit()

def scrapper(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    assignments = []
    ass_scraper = soup.find_all('div', class_='ig-info')
    for assignment in ass_scraper:
        name = assignment.find_all('a')
        name = name.name

if __name__ == "__main__":
    with open('password.yml', 'r') as file:
        login_details = yaml.safe_load(file)
    page_source = driver.page_source
    scrapper(page_source)




