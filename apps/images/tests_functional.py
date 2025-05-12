from django.contrib.staticfiles.testing import LiveServerTestCase
from django.urls import reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

class ImageFunctionalTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()

    def test_login_upload_and_list_image(self):
        # Login
        self.browser.get(self.live_server_url + reverse('accounts:login'))
        self.browser.find_element(By.NAME, 'username').send_keys('edson.uenf@gmail.com')
        self.browser.find_element(By.NAME, 'password').send_keys('fractal')
        self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(1)
        assert 'Dashboard' in self.browser.page_source or 'dashboard' in self.browser.current_url.lower()

        # Upload de imagem
        self.browser.get(self.live_server_url + reverse('images:upload_image'))
        self.browser.find_element(By.NAME, 'title').send_keys('Imagem Funcional Selenium')
        # Usa a primeira imagem encontrada na pasta fornecida
        image_path = r'C:\Users\edson\Documentos\msaude\04_Edson_ABRIL_25\Fotos_ABRIL_25_tratadas\Aline Horta - 06-12-24-8297.jpg'
        assert os.path.exists(image_path), f"Arquivo de imagem não encontrado: {image_path}"
        self.browser.find_element(By.NAME, 'images').send_keys(image_path)
        self.browser.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(2)

        # Verifica se aparece na listagem
        self.browser.get(self.live_server_url + reverse('images:image_list'))
        time.sleep(1)
        assert 'Imagem Funcional Selenium' in self.browser.page_source
