import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from googletrans import Translator


class ScopusPersonInformation(object):
    def __init__(self):
        firefox_options = Options()
        firefox_options.add_argument('--headless')
        firefox_options.add_argument('--start-maximized')
        self.driver = webdriver.Firefox(
            firefox_options=firefox_options,
            executable_path='data/geckodriver'
        )
        self.translator = Translator()

    def translate(self, russian_string: str) -> str:
        """
        Translate russian sentence to english
        Args:
            russian_string: string with sentence in russian

        Returns:
            string with sentence in english
        """
        return self.translator.translate(text=russian_string, src='ru').text

    def __call__(self,
                 person_name: str,
                 university: str,
                 top_k: int = 3,
                 ru: bool = False) -> tuple:
        """
        Get count of publication of input topics
        Args:
            person_name: name in Last Name F.S. format
            university: name of university
            top_k: returned subjects count
            ru: name in russian

        Returns:
            Tuple of (h-index, list of target main topics)
        """
        input_name = person_name if not ru else self.translate(person_name)

        last_name, first_name = input_name.split(' ')

        subject_area_list = []
        h_index = 0

        self.driver.get(
            'https://www.scopus.com/freelookup/form/author.uri'
        )

        # Click last name field
        try:
            button = self.driver.find_element_by_xpath(
                '/html/body/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/form/div[1]/div/div[1]/div[1]/div/span[1]/label'
            )
            button.click()
        except Exception as e:
            print(e)

        # time.sleep(1)
        # Input last name
        try:
            topic_enter = self.driver.find_element_by_xpath(
                '//*[@id=\"lastname\"]'
            )
            topic_enter.send_keys(last_name)
        except Exception as e:
            print(e)

        # Click first name field
        try:
            button = self.driver.find_element_by_xpath(
                '/html/body/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/form/div[1]/div/div[1]/div[2]/div/span[1]/label'
            )
            button.click()
        except Exception as e:
            print(e)

        # time.sleep(1)
        # Input first name
        try:
            topic_enter = self.driver.find_element_by_xpath(
                '//*[@id=\"firstname\"]'
            )
            topic_enter.send_keys(first_name.upper())
        except Exception as e:
            print(e)

        # Click university name field
        try:
            button = self.driver.find_element_by_xpath(
                '/html/body/div/div/div[1]/div[2]/div/div[3]/div/div[2]/div[2]/form/div[1]/div/div[2]/div[1]/div/span[1]/label'
            )
            button.click()
        except Exception as e:
            print(e)

        # time.sleep(1)
        # Input university name
        try:
            topic_enter = self.driver.find_element_by_xpath(
                '//*[@id=\"institute\"]'
            )
            topic_enter.send_keys(university)
        except Exception as e:
            print(e)

        # time.sleep(1)

        # Click search button
        try:
            button = self.driver.find_element_by_xpath(
                '//*[@id=\"authorSubmitBtn\"]'
            )
            button.click()
        except Exception as e:
            print(e)

        # Select person from table
        try:
            button = self.driver.find_element_by_xpath(
                '/html/body/div[1]/div/div[1]/div[1]/div/div[3]/form/div[3]/div[2]/div[1]/div/div[2]/div/table/tbody/tr[1]/td[1]/a'
            )
            button.click()
        except Exception as e:
            print(e)

        time.sleep(1)

        # Extract subject area list
        try:
            for i in range(top_k):
                subject = self.driver.find_element_by_css_selector(
                    '#subjectAreaBadges > span:nth-child({})'.format(i + 1)
                )
                subject_area_list.append(subject.text)

        except Exception as e:
            print(e)

        # Select person from table
        try:
            h_index_selector = self.driver.find_element_by_xpath(
                '/html/body/div/div[1]/div[1]/div[2]/div[1]/div[3]/form/div[3]/div[3]/section[1]/div[1]/div[2]/div/section[3]/div[2]/div/span'
            )
            h_index = int(h_index_selector.text)
        except Exception as e:
            print(e)

        return h_index, subject_area_list


def useful_person_for_subjects(
        person_main_topics: list,
        scopus_topics: list,
        k_relevant: int = 1) -> bool:
    """
    Get possibility status use person for subject
    Args:
        person_main_topics:
        scopus_topics: topics list in ScopusScienceTopicSearch class format
        k_relevant: count of reviewed topics

    Returns:
        Status
    """
    if len(scopus_topics) == 0 or len(person_main_topics) == 0:
        return False

    for topic in scopus_topics[:k_relevant]:
        if topic.split(',')[0] in person_main_topics:
            return True

    return False


if __name__ == '__main__':
    spi = ScopusPersonInformation()

    print(spi('Чепурненко А.С.', 'DSTU', ru=True))
