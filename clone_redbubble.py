import io
import json
import time

import requests
from PIL import Image, ImageDraw, ImageFont

import random
import selenium
import shutil

from lxml import html
from lxml.html import clean

from seleniumrequests import Firefox
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementNotInteractableException, ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from pathlib import Path
from urllib.parse import urljoin, urlparse

USERNAME = ""
PASSWORD = ""
DOWNLOAD_DIR = Path('./') / "redbubble"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

class RedBubble:
    def __init__(self):
        self.options = Options()
        self.options.set_preference("intl.accept_languages", 'en-us')
        self.options.set_preference('useAutomationExtension', False)
        self.options.set_preference('dom.webdriver.enabled', False)

        self.driver = Firefox(options=self.options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get("https://amiunique.org/fp")
        time.sleep(5)
        self.driver.get("https://antcpt.com/score_detector/")
        time.sleep(5)

    def get_to(self, url):
        if self.driver.current_url != url:
            self.driver.get(url)

    def download_image(self, file_name, image_url):
        if "x1000" in image_url:
            big_image_url = image_url.replace("1000x1000", "2000x2000")
            big_image_url = big_image_url.replace("750x1000", "1500x2000")
            big_image_url = big_image_url.replace("1000", "2000")
            big_image_url = big_image_url.replace("750", "1500")
            if self.download_image(file_name, big_image_url):
                print(f"Gotten bigger image for {file_name} @ {big_image_url}")
                return True
        try:
            res = self.driver.request('GET', image_url)
        except requests.exceptions.ConnectionError:
            time.sleep(60)
            res = self.driver.request('GET', image_url)

        if 200 <= res.status_code < 300:
            im = Image.open(io.BytesIO(res.content))

            width, height = im.size

            # Add watermark
            if max(width, height) >= 2000:
                font = ImageFont.truetype('Arial.ttf', 72)
            else:
                font = ImageFont.truetype('Arial.ttf', 36)

            draw = ImageDraw.Draw(im)
            text = "DuckHunt.me"

            fill_color = (128, 0, 0)

            textwidth, textheight = draw.textsize(text, font)

            margin = 30
            x = width - textwidth - margin
            y = height - textheight - margin
            try:
                draw.text((x, y), text, font=font, fill=fill_color)
            except TypeError:
                draw.text((x, y), text, font=font, fill=128)

            # Write to file
            im.save(file_name)

            return True
        else:
            print(f"Download of {file_name} (@{image_url}) FAILED.")
            return False

    def clean_html(self, html_string):
        tree = html.fromstring(html_string)

        cleaner = html.clean.Cleaner()
        cleaner.safe_attrs_only = True
        cleaner.safe_attrs = frozenset(['id'])
        cleaned = cleaner.clean_html(tree)
        return html.tostring(cleaned, encoding='unicode')

    def dismiss_cookie_popup(self):
        self.dismiss_member_prompt()
        try:
            self.driver.find_element_by_class_name("Toastify__toast-body").find_element_by_tag_name("button").click()
            return True
        except (NoSuchElementException, ElementClickInterceptedException):
            return False

    def dismiss_member_prompt(self):
        try:
            self.driver.find_element_by_class_name("sailthru-overlay-close").click()
            return True
        except NoSuchElementException:
            return False

    def login(self):
        self.driver.get("https://www.redbubble.com/en/auth/login")

        username = self.driver.find_element_by_xpath('//*[@id="ReduxFormInput1"]')
        username.send_keys(USERNAME)

        password = self.driver.find_element_by_xpath('//*[@id="ReduxFormInput2"]')
        password.send_keys(PASSWORD)

        connect = self.driver.find_element_by_xpath('/html/body/div[1]/div[7]/div[2]/div[2]/div/form/span/button')

        prev_url = self.driver.current_url
        connect.click()
        time.sleep(5)

        while prev_url == self.driver.current_url:
            print("Please solve captcha")
            time.sleep(1)

    def change_locale(self):
        self.get_to("https://www.redbubble.com/settings/show")

        locale_dropdown = Select(self.driver.find_element_by_xpath('//*[@id="settings_locale"]'))
        locale_dropdown.select_by_visible_text("English")

        country_code_dropdown = Select(self.driver.find_element_by_xpath('//*[@id="settings_country_code"]'))
        country_code_dropdown.select_by_value("US")

        currency_dropdown = Select(self.driver.find_element_by_xpath('//*[@id="settings_currency_iso"]'))
        currency_dropdown.select_by_value("USD")

        try:
            button = self.driver.find_element_by_xpath('/html/body/div/form/div[4]/input')
        except NoSuchElementException:
            button = self.driver.find_element_by_xpath('/html/body/div[1]/div[6]/div[2]/form/div[4]/button')

        button.click()

    def get_works_urls(self):
        self.get_to("https://www.redbubble.com/en/portfolio/manage_works")
        self.dismiss_cookie_popup()
        works = []

        links = self.driver.find_elements_by_class_name('works_work-menu-option')
        for a in links:
            if a.tag_name != 'a':
                continue

            href = a.get_attribute('href')
            if href.startswith("https://www.redbubble.com/people/duckhuntdiscord/works"):
                works.append(href)

        random.shuffle(works)
        return works

    def get_work_products_urls(self, work_url):
        self.get_to(work_url)
        products_urls = []

        links = self.driver.find_elements_by_class_name('carousel_item-link')
        for a in links:
            if a.tag_name != 'a':
                continue

            href = a.get_attribute('href')
            if href.startswith("https://www.redbubble.com/i/"):
                products_urls.append(href)

        random.shuffle(products_urls)
        return products_urls

    def get_work_info(self, work_url):
        self.get_to(work_url)

        return {
            "name": self.driver.find_element_by_class_name('work-information_title').text,
            "url": urljoin(work_url, urlparse(work_url).path)
        }

    def _get_colorswatch(self):
        try:
            colors_button = self.driver.find_element_by_css_selector("[class^='ColorPickerActivator__colorPickerActivator--']")
        except NoSuchElementException:
            colors_button = None

        if colors_button:
            colors_button.click()

        try:
            colors_swatch = self.driver.find_elements_by_css_selector("[class^='DesktopColorControls__swatch--']")
        except NoSuchElementException:
            colors_swatch = [None]

        if len(colors_swatch) == 0:
            colors_swatch = [None]

        return colors_swatch

    def _get_print_locations(self):
        print_locations = self.driver.find_elements_by_name("printLocation")

        if not print_locations:
            print_locations = [None]

        return print_locations

    def _get_sizes(self):
        sizes = self.driver.find_elements_by_name("size")

        if not sizes:
            sizes = [None]

        return sizes

    def download_product_information(self, product_url, work_info):
        self.get_to(product_url)
        self.dismiss_cookie_popup()

        varients = []

        product_name = self.driver.find_element_by_tag_name('h1').text
        print(f"Downloading {product_name}...")

        download_to = DOWNLOAD_DIR / work_info["name"] / product_name
        download_to.mkdir(exist_ok=True, parents=True)

        if (download_to / "download.json").exists():
            print("Skipping : already downloaded")
            return

        colors = len(self._get_colorswatch())
        print(f"Found {colors} colors_swatch.")
        for color_n in range(colors):
            color_element = self._get_colorswatch()[color_n]

            if color_element is None:
                color_product_name = None
            else:
                color_product_name = color_element.get_attribute('title')
                color_element.click()
                self.dismiss_cookie_popup()

            print_locations_count = len(self._get_print_locations())
            print(f"Found {print_locations_count} print locations.")

            for print_location_n in range(print_locations_count):
                print_location_element = self._get_print_locations()[print_location_n]
                if print_location_element is None:
                    print_location_text = None
                else:
                    label = print_location_element.find_element_by_xpath('..')
                    print_location_text = label.text
                    label.click()
                    self.dismiss_cookie_popup()

                sizes = self._get_sizes()
                sizes_names = []
                for size_element in sizes:
                    if size_element is None:
                        continue
                    else:
                        label = size_element.find_element_by_xpath('..')
                        size_name = label.text
                        sizes_names.append(size_name)

                time.sleep(1)  # Time for images to load
                images = self.driver.find_elements_by_tag_name('img')

                images_downloaded = 0
                images_files = []

                for img in images:
                    src = img.get_attribute('src')
                    klass = img.get_attribute('class')
                    if src.startswith("https://ih1.redbubble.net/image") and "GalleryImage__img--" in klass:
                        main = "PreviewGallery__rightColumn--" in img.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('class')

                        img_folder = download_to / f"{color_product_name} - {print_location_text}"
                        img_folder.mkdir(parents=True, exist_ok=True)
                        image_name = img_folder / f"{images_downloaded}.jpg"
                        dld = self.download_image(file_name=image_name, image_url=src)
                        if dld:
                            images_downloaded += 1
                            images_files.append({"link": str(image_name), "main": main})

                price = ''
                config_div = self.driver.find_element_by_tag_name('h1').find_element_by_xpath('..')
                prices_maybe = config_div.find_elements_by_tag_name('span')

                for price_maybe in prices_maybe:
                    try:
                        price = price_maybe.find_element_by_tag_name('span').text
                        break
                    except NoSuchElementException:
                        continue

                varient = {
                    "color_product_name": color_product_name,
                    "print_location_text": print_location_text,
                    "sizes_names": sizes_names,
                    "images_count": images_downloaded,
                    "images": images_files,
                    "price": price,
                    "url": self.driver.current_url,
                }

                print(varient)

                varients.append(varient)
        try:
            features = self.driver.find_element_by_xpath("//*[contains(text(), 'Features')]")\
                                  .find_element_by_xpath('..')\
                                  .find_element_by_tag_name('ul')\
                                  .get_attribute('outerHTML')
        except NoSuchElementException:
            features = self.driver.find_element_by_xpath("//*[contains(text(), 'Features')]") \
                .find_element_by_xpath('..') \
                .find_element_by_xpath('..') \
                .find_element_by_tag_name('ul') \
                .get_attribute('outerHTML')

        with open(download_to / "download.json", "w") as f:
            json.dump({
                "varients": varients,
                "features_html": self.clean_html(features),
                "work": work_info,
            }, f, sort_keys=True)

    def main(self):
        self.login()
        self.change_locale()
        works_urls = self.get_works_urls()
        print(f"Discovered {len(works_urls)} works")
        for work_url in works_urls:
            work_info = self.get_work_info(work_url)
            # if (DOWNLOAD_DIR / work_info["name"]).exists():
            #     print(f"Skipping {work_info['name']} because it was already downloaded.")
            #     continue
            product_urls = self.get_work_products_urls(work_url)
            for product_url in product_urls:
                ok = False
                while not ok:
                    try:
                        self.download_product_information(product_url, work_info)
                        ok = True
                    except (StaleElementReferenceException, ElementNotInteractableException, NoSuchElementException) as e:
                        print(f"That failed {e}, retrying...")

        self.driver.quit()


rb = RedBubble()
rb.main()


