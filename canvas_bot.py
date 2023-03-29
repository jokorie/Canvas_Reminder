from selenium import webdriver  # use to interact with ava content on dynamic webpages
from bs4 import BeautifulSoup # use to scrape information off static webpage
import pandas as pd # use to store data into ordered csv file
import yaml # use to pull password information from secure location
import time # use to tell computer to wait in order for some webpages to load

# initializing options for the wedriver browser
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)

# open canvas login front page
driver.get("https://canvas.mit.edu/courses/19452/assignments")

def button_click(driver, xpath):
    """Clicks button as specified through the xpath address uing the specified driver

    Args:
        driver: webdriver element
        xpath: xpath to button
    """    
    button = driver.find_element('xpath', xpath)
    button.click()

def login(usernameId, username, passwordId, password, submit_buttonId):
    """Inputs the username, password into their respective fields and hits submit button
    
    Args:
        usernameId (xpath): location of username field
        username (string): username
        passwordId (xpath): location of password field
        password (string): password
        submit_buttonId (xpath): submit button field
    """    
    login_button = driver.find_element('xpath', "/html/body/div/div/div[3]/div/div/div/div/div/section/div/div/div/article/div/div/table/tbody/tr[2]/td/a")
    login_button.click()
   
    driver.find_element('xpath', usernameId).send_keys(username)
    driver.find_element('xpath', passwordId).send_keys(password)
    driver.find_element('xpath', submit_buttonId).click()

def duo_two_step(driver):
    """Logs in via duo two step authentification **requires duo verication on phone** and returns the html canvas page content

    Args:
        driver (driver): webdriver object

    Returns:
        html content: _description_
    """    
    attempts = 0 # attempts to login to duo
    time.sleep(2) # allows webpage time to load desired content
    while attempts < 2:
        try:
            iframe = driver.find_element('xpath', '//*[@id="duo_iframe"]') # the duo push notification button is located within an ifram
            driver.switch_to.frame(iframe) # to press button we must switch our driver into iframe
            duo_button = driver.find_element('xpath', '/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button')
            duo_button.click()

            time.sleep(10) # time to let canvas page load
            driver.switch_to.default_content() # switch driver out of ifram
            return driver.page_source # return content of the page for the beutiful soup library to parse
        except:
            time.sleep(25) # cooldown till second duo authentification attempt
            attempts += 1
            continue            
    print("Duo Authentification Failed. Quitting")
    quit()

def scrapper(page_source):
    """take canvas html page content and scrapes asssignments and their due dates

    Args:
        page_source (html content): html content of asisgnments page

    Returns:
        list(tuple): list where each element is a tuple representing the assignment and its due date
    """    
    soup = BeautifulSoup(page_source, 'html.parser') # parses html content making it operable for python script
    assignments = []
    ass_scraper = soup.find_all('div', class_='ig-info') # finds the divider regions which holds the assignment content
    for assignment in ass_scraper:
        try:
            name = assignment.find('a').get_text().strip()
            due_date = assignment.find('div', class_='ig-details__item assignment-date-due').find('span').get_text().strip()
            assignments.append((name, due_date))
        except:
            print('Error with content')
    return assignments


if __name__ == "__main__":
    start_time = time.time() # start timer for operation
    with open('password.yml', 'r') as file: # loads password info for canvas login
        login_details = yaml.safe_load(file)

    myKerb = login_details['canvas_user']['kerb']
    myPassword = login_details['canvas_user']['password']

    # xpaths for username, password, submit_button fields
    username_path = '/html/body/div[2]/form[2]/fieldset/label[1]/input'
    password_path = '/html/body/div[2]/form[2]/fieldset/label[2]/input[1]'
    button_path = '/html/body/div[2]/form[2]/fieldset/label[2]/input[2]'

    login(username_path, myKerb, password_path, myPassword, button_path)

    page_source = duo_two_step(driver)
    ass_info = scrapper(page_source)
    names, dates = tuple(map(list, zip(*ass_info))) # name = list of all assignment names etc..

    canvas_info = pd.DataFrame() #make our spreadsheet with a pandas data frame!
    canvas_info['name'] = names
    canvas_info['due_date'] = dates

    canvas_info.to_csv('canvas_info.csv', index=False) # save df into csv file
    
    driver.close() # close the webpage

    print('script completed')
    print("--- %s seconds ---" % (time.time() - start_time))



