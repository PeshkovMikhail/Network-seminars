import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import argparse
import pandas

parser = argparse.ArgumentParser(description="4PDA parser")
parser.add_argument("--page", type=int, default=1)
parser.add_argument("--username", type=str, default="null")
parser.add_argument("--password", type=str, default="null")
args = parser.parse_args()

driver = webdriver.Chrome()

def auth(username: str, password: str):
    driver.get("https://account.habr.com/login/?consumer=default")
    driver.implicitly_wait(3)
    try:
        driver.find_element(By.NAME, "email").send_keys(args.username)
        driver.find_element(By.NAME, "password").send_keys(args.password)
        driver.find_element(By.NAME, "go").click()
    except Exception as e:
        print(f'something is wrong: {e}')
    time.sleep(30)

def get_articles(page: int) -> list:
    if args.page < 1:
        raise ValueError("page number must be >= 1")

    driver.get(f"https://habr.com/ru/all/page{args.page}/")
    return [i.text for i in driver.find_elements(By.CLASS_NAME, "tm-article-snippet__title")]

    

if args.username != "null" and args.password != "null":
    auth(args.username, args.password)
else:
    articles = get_articles(args.page)
    df = pandas.DataFrame(articles)
    df.to_csv("articles.csv", encoding='utf-8-sig', index=False, header=False)
    