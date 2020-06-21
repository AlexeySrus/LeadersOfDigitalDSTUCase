from flask import Flask, jsonify, request, abort
from argparse import ArgumentParser
import re
import numpy as np
from flask_cors import CORS

from utils.scopus_utils import ScopusScienceTopicSearch
from utils.web_parsers.scopus_topics_parser import ScopusScienceTopicRelevance
from utils.web_parsers.scopus_person_parser import ScopusPersonInformation
from utils.web_parsers.scopus_person_parser import useful_person_for_subjects
from utils.hh_database_toolkit import HHDatabase

app = Flask(__name__)
CORS(app)

scopus_topics_estimator = ScopusScienceTopicSearch()
scopus_papers_count_estimator = ScopusScienceTopicRelevance()
scopus_person_subjects_estimator = ScopusPersonInformation()
hh_database = HHDatabase(threshold=0.4)

avg_rostov_salary = 44000

degree_map = {
    'нет': 0,
    'кандидат наук': 1,
    'доктор наук': 2,
}


@app.route('/api/test', methods=['POST'])
def test_server_inference():
    request_data = request.get_json()
    print('Data is:', request_data)

    return jsonify(
        {
            'test': 'test'
        }
    )


@app.route('/api/compute', methods=['POST'])
def server_inference():
    """
    Compute metric of curriculum Relevance
    Input json in follow format:
    {
        'program_name': str,
        'competencies: [list of strings],
        'maker': str with Full name if program maker,
        'maker_science_degree': str, choose from `нет`, `кандидат наук`, `доктор наук`
        'university': str, choose from `SFEDU`, `DSTU` (experimental feature)
    }
    Returns:
        Json in follow format:
        {
            'scientific_activity': float rate of science activity
                on scopus platform by program name
            'curriculum_relevance_score': float result relevance score
            'avg_region_salary_increase': float index means that how many times
                the median salary is higher than the
                average salary in the region
            'status': node for frontend
        }
    """
    try:
        request_data = request.get_json()

        scopus_topics = scopus_topics_estimator(
            request_data['program_name'],
            ru=True
        )

        publications_count = scopus_papers_count_estimator(scopus_topics)

        useful_person = False
        if 'maker' in request_data.keys() and \
                'university' in request_data.keys():
            main_maker_topics = scopus_person_subjects_estimator(
                request_data['maker'],
                request_data['university']
            )

            useful_person = useful_person_for_subjects(
                main_maker_topics[1],
                scopus_topics
            )

        if 'maker_science_degree' in request_data.keys():
            degree_score = degree_map[request_data['maker_science_degree']] / 2
        else:
            degree_score = 0

        job_quality = 0
        if 'competencies' in request_data.keys():
            offers = hh_database(request_data['competencies'].split(';'))
            avg_region_salary_increase = 0

            if len(offers) > 0:
                salary_median = np.median(
                    np.array(
                        [offer['avg_salary'] for offer in offers]
                    )
                )
                offers_count = np.array(
                    [offer['offers_count'] for offer in offers]
                ).mean()

                avg_region_salary_increase = salary_median / avg_rostov_salary

                job_quality = avg_region_salary_increase + \
                              5 * offers_count / hh_database.max_offers_count

        curriculum_score = (
               publications_count / 400 + useful_person + job_quality + degree_score
        ) / 4
    except Exception as e:
        print(e)
        abort(401)

    return jsonify(
        {
            'scientific_activity': float("{:.2f}".format(publications_count / 900)),
            'curriculum_relevance_score': float("{:.2f}".format(curriculum_score)),
            'avg_region_salary_increase': float("{:.2f}".format(avg_region_salary_increase))
        }
    )


def args_parse():
    parser = ArgumentParser(description='Server')
    parser.add_argument('--ip', required=False, type=str, default='0.0.0.0')
    parser.add_argument('--port', required=False, type=int, default=5000)
    return parser.parse_args()


def main():
    args = args_parse()
    app.run(host=args.ip, debug=False, port=args.port)


if __name__ == '__main__':
    main()
