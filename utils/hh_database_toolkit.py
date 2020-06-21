import json
import numpy as np
from utils.text_similarity import TextSimilarityEstimator
from tqdm import tqdm


class HHDatabase(object):
    def __init__(self,
                 database_path: str = 'data/hh_eng_database.json',
                 threshold: float = 0.5):
        with open(database_path, 'r') as jf:
            self.db = json.load(jf)

        self.max_offers_count = 0
        for field in self.db.keys():
            l = len(self.db[field]['salaries'])
            if l > self.max_offers_count:
                self.max_offers_count = l

        self.text_similarity_estimator = TextSimilarityEstimator()
        self.threshold = threshold

    def __call__(self, competencies: list) -> list:
        """
        Get similarity vacancy list
        Args:
            competencies: list of competencies in russian

        Returns:
            Similarity vacancy list
        """
        matched_fields = []
        eng_competencies = [
            self.text_similarity_estimator.translate(comp)
            for comp in competencies
        ]

        for field in list(self.db.keys()):
            scores = []
            for competence in eng_competencies:
                sequence = self.db[field]['requirements']
                if len(sequence) > 15:
                    sequence = sequence[:15]
                for req in sequence:
                    score = self.text_similarity_estimator(
                        competence, req
                    )
                    scores.append(score)

            avg_score = np.array(scores).mean()
            # print(avg_score)
            if avg_score > self.threshold:
                matched_fields.append(field)

        return [
            {
                'name': field,
                'offers_count': len(self.db[field]['salaries']),
                'avg_salary': np.array(self.db[field]['salaries']).mean()
            }
            for field in matched_fields
        ]
