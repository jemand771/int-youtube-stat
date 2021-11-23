import multiprocessing
import time

from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import app as main_app


multiprocessing.set_start_method("fork")


class TestWebInterface(LiveServerTestCase):

    def create_app(self):
        app = main_app.app
        app.config["LIVESERVER_PORT"] = 0
        app.config["LIVESERVER_TIMEOUT"] = 10
        return app

    def setUp(self) -> None:
        chrome_options = Options()
        # TODO re-enable
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(1920, 1080)
        self.driver.implicitly_wait(5)

    def tearDown(self) -> None:
        self.driver.close()

    def test_foo(self):
        self.driver.get(self.get_server_url())
        time.sleep(10)
