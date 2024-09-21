import argparse
from chromedriver_py import binary_path
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
logging.basicConfig(level=logging.INFO)

class MondayShareLinkDisableAutomation():

    def __init__(self, email, password, boardId, viewId):
        super().__init__()
        self.email = email
        self.password = password
        self.boardId = boardId
        self.viewId = viewId

    def start_disable_flow(self):
        print("HIIIII")
        # Set up Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--disable-dev-shm-usage")
        # chrome_options.add_argument("--disable-gpu")


        # # Path to the ChromeDriver executable
        svc = ChromeService(executable_path=binary_path)
        driver = webdriver.Chrome(service=svc, options=chrome_options)
        logging.info("start selenium")

        try:
            # Navigate to monday.com login page
            driver.get(f"https://cisco617620.monday.com/boards/{self.boardId}/views/{self.viewId}")  
            wait = WebDriverWait(driver, 240)        
            login_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-monday-container"]/div/div[2]/div/div[2]/div/button')))
            login_button.click()
            logging.info(login_button)
            logging.info("Able to perform selenium actions")

            #Email /Username field
            username_field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-parent"]/div/div[3]/label/input')))
            username_field.send_keys(self.email)  
            next_button =  driver.find_element(By.XPATH, '//*[@id="login-parent"]/div/div[3]/button')
            next_button.click()

            #Show other options
            show_other_options = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pwl-prompt-root"]/div/div/div/div[3]/button')))
            show_other_options.click()

            #Password field
            other_options_password =  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="pwl-prompt-root"]/div/div/div/div[3]/div/div[2]/a')))
            other_options_password.click()
            password_field =  wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-parent"]/div/div[3]/form/label/input')))
            password_field.send_keys(self.password)

            log_in_button =   wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="login-parent"]/div/div[3]/form/button')))
            log_in_button.click()
            logging.info("Successfully able to login using selenium")


            stop_button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Stop')]")))
            stop_button.click() 
            logging.info("Successfully clicked stop")
            time.sleep(30)
            
        except TimeoutException as exception:
            logging.error(f"Timed out waiting for element to appear {exception}")
        except NoSuchElementException as exception:
            logging.error(f"Element not found exception {exception}.")
        except Exception as exception:
            logging.error(f"Exception {exception}.")

        finally:
            driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Selenium tests for Monday Shareable Links.')
    parser.add_argument('email', type=str, help='The email address used to login.')
    parser.add_argument('password', type=str, help='The password to login.')
    parser.add_argument('boardId', type=str, help='Board ID of the view to be disabled.')
    parser.add_argument('viewId', type=str, help='View ID of the board to be disabled')

    args = parser.parse_args()
    # test = MondayShareLinkDisableAutomation('args.email', 'args.password', 'args.boardId', 'args.viewId' )
    test = MondayShareLinkDisableAutomation(args.email, args.password, args.boardId, args.viewId )
    test.start_disable_flow()