import yaml
from googletrans import Translator


class ScopusScienceTopicSearch(object):
    """Mapping russian courses names to scopus classes"""
    def __init__(self, topics_map_path: str = 'sources/scopus_science_map.yml'):
        """
        Class constructor
        Args:
            topics_map_path: path to scopus_science_map
        """
        with open(topics_map_path, 'r') as f:
            self.topics_map = yaml.safe_load(f)

        self.preprocess_topics_map = {
            main_topic: [
                subtopic.lower()
                for subtopic in self.topics_map[main_topic]
            ]
            for main_topic in self.topics_map
        }

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

    def __call__(self, input_topic: str, ru: bool = False) -> list:
        """
        Call method
        Args:
            input_topic: input topic description in english
            ru: topic in russian

        Returns:
            List of strings with probability science themes from scopus list
            with follow format: `main topic,subtopic`
        """
        if ru:
            tags = self.translate(input_topic).lower().split(' ')
        else:
            tags = input_topic.lower().split(' ')

        result_topics = []

        for main_topic in self.topics_map.keys():
            for tag in tags:
                found_in_subtopics = False

                for k, subtopic in enumerate(
                        self.preprocess_topics_map[main_topic]):
                    if tag in subtopic:
                        found_in_subtopics = True
                        result_topics.append(
                            main_topic + ',' + self.topics_map[main_topic][k]
                        )

                # if not found_in_subtopics:
                #     if tag in str(main_topic).lower():
                #         for subtopic in self.topics_map[main_topic]:
                #             result_topics.append(
                #                 main_topic + ',' + subtopic
                #             )

        return result_topics
