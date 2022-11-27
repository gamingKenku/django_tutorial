from selenium import webdriver
from django.test import LiveServerTestCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from datetime import date
import time
import random


class BookshopTests(LiveServerTestCase):

    def test_adding_book(self):
        try:
            driver = webdriver.Chrome()
            driver.get('http://127.0.0.1:8000/add/')

            book_title = driver.find_element(By.NAME, 'title')
            book_price = driver.find_element(By.NAME, 'price')
            book_release_date = driver.find_element(By.NAME, 'release_date')
            book_author = driver.find_element(By.NAME, 'author')

            submit = driver.find_element(By.NAME, 'submit')

            book_title.send_keys('test_title')
            book_price.send_keys(float(random.randint(1, 200)))
            now = date.today().strftime('%d-%m-%Y')
            book_release_date.send_keys(now)
            book_author.send_keys('test_author')

            submit.send_keys(Keys.RETURN)

            assert driver.current_url == 'http://127.0.0.1:8000/'

            driver.close()
            print("test1 successful")
        finally:
            print('test1 done')

    def test_login(self):
        try:
            driver = webdriver.Chrome()
            driver.get('http://127.0.0.1:8000/users/login/')

            user_login = driver.find_element(By.ID, "id_username")
            user_password = driver.find_element(By.ID, "id_password")

            submit = driver.find_element(By.ID, "id_submit")

            user_login.send_keys('Selenium_test_login')
            user_password.send_keys('s_e_le_ni_um1942')

            submit.send_keys(Keys.RETURN)

            assert driver.current_url == 'http://127.0.0.1:8000/'

            print("test2 successful")
        finally:
            print('test2 done')
