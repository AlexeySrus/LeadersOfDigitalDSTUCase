import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


class ScopusScienceTopicRelevance(object):
    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--start-maximized')
        self.driver = webdriver.Firefox(
            firefox_options=firefox_options,
            executable_path='data/geckodriver'
        )

    def __call__(self, input_topics: list) -> int:
        """

        Args:
            input_topics: input topics from ScopusScienceTopicSearch class

        Returns:
            Count of publications by this topic in previous year
        """
        count = 0

        for topic in input_topics:
            self.driver.get(
                'https://www.scopus.com/sources.uri'
            )

            try:
                button = self.driver.find_element_by_xpath(
                    '//*[@id=\"search_source_label\"]'
                )
                button.click()
            except Exception as e:
                print(e)

            time.sleep(1)

            try:
                topic_enter = self.driver.find_element_by_xpath(
                    '//*[@id=\"search-term\"]'
                )
                topic_enter.send_keys(topic.split(',')[1])

            except Exception as e:
                print(e)

            time.sleep(1)

            try:
                button = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[1]/div[2]/div/div[3]/form/section[1]/div[1]/div/div[2]/div[3]/div/ul/li[2]/ul/li/label'
                )
                button.click()
            except Exception as e:
                print(e)

            time.sleep(1)

            try:
                button = self.driver.find_element_by_xpath(
                    '/html/body/div[1]/div/div[1]/div[2]/div/div[3]/form/section[1]/div[1]/div/div[2]/div[3]/div/div/div/input'
                )
                button.click()
            except Exception as e:
                print(e)

            time.sleep(1)

            try:
                item = self.driver.find_element_by_xpath(
                    '//*[@id=\"resultCount\"]'
                )
                value = item.text
                count += int(value.split(' ')[0])
            except Exception as e:
                print(e)

        return count


if __name__ == '__main__':
    t = ScopusScienceTopicRelevance()
    query = [
        'Arts and Humanities,Language and Linguistics',
        'Social Sciences,Linguistics and Language'
    ]

    print('Total publications count: {}'.format(t(query)))
