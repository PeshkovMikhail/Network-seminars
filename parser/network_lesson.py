import time
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import argparse
import pandas

class HabrParser:
    def __init__(self) -> None:
        self.driver = webdriver.Chrome()

    def auth(self, email: str, password: str):
        self.driver.get("https://account.habr.com/login/?consumer=default")
        self.driver.implicitly_wait(3)
        try:
            self.driver.find_element(By.NAME, "email").send_keys(email)
            self.driver.find_element(By.NAME, "password").send_keys(password)

            captcha = self.driver.find_element(By.ID, "captcha-s-field")
            if captcha.is_displayed():
                print("Please solve captcha")
                time.sleep(20)
            
            self.driver.find_element(By.NAME, "go").click()
            self.driver.implicitly_wait(5)

            print(self.driver.find_element(By.CLASS_NAME, "welcome__title").text)
        except Exception as e:
            print(f'something is wrong: {e}')
        time.sleep(30)

    def get_articles(self, page: int = 1) -> list:
        if args.page < 1:
            raise ValueError("page number must be >= 1")

        self.driver.get(f"https://habr.com/ru/all/page{page}/")
        return [i.text for i in self.driver.find_elements(By.CLASS_NAME, "tm-article-snippet__title")]
    
    def save_articles(self, path: str, page: int = 1):
        articles = self.get_articles(page)
        df = pandas.DataFrame(articles)
        df.to_csv(path, encoding='utf-8-sig', index=False, header=False)

def parse_auth_data(path: str):
    f = open(path)
    data = json.load(f)
    return data["email"], data['password']

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Habrahabr parser")
    parser.add_argument("--auth", action="store_true")
    parser.add_argument("--auth_data_path", type=str, default="auth_data.json")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--save_path", type=str, default="articles.csv")
    args = parser.parse_args()

    habrParser = HabrParser()
    if args.auth:
        email, password = parse_auth_data(args.auth_data_path)
        habrParser.auth(email, password)
    else:
        habrParser.save_articles(args.save_path, args.page)
    