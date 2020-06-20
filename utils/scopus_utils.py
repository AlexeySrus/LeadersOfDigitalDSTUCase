import yaml


class ScopusScienceTopicSearch(object):
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

    def __call__(self, input_topic: str):
        """
        Call method
        Args:
            input_topic: input topic description in english

        Returns:
            List of strings with probability science themes from scopus list
            with follow format: `main topic,subtopic`
        """
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

                if not found_in_subtopics:
                    if tag in str(main_topic).lower():
                        for subtopic in self.topics_map[main_topic]:
                            result_topics.append(
                                main_topic + ',' + subtopic
                            )

        return result_topics
