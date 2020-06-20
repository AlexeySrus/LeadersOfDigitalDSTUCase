from flask import Flask, jsonify, request
from argparse import ArgumentParser

from utils.scopus_utils import ScopusScienceTopicSearch
from utils.web_parsers.scopus_topics_parser import ScopusScienceTopicRelevance

app = Flask(__name__)

scopus_topics_estimator = ScopusScienceTopicSearch()
scopus_papers_count_estimator = ScopusScienceTopicRelevance()


@app.route('/api/compute', methods=['POST'])
def server_inference():
    """
    Compute metric of curriculum Relevance
    Input json in follow format:
    {
        'program_name': str,
        'competencies: [list of strings],
        'maker': str with Full name if program maker,
        'university': str, choose from `SFEDU`, `DSTU` (experimental feature)
    }
    Returns:
        Json in follow format:
        {
            'scientific_activity': rate of science activity
                on scopus platform by program name
        }
    """
    request_data = request.get_json()

    scopus_topics = scopus_topics_estimator(
        request_data['program_name'],
        ru=True
    )

    publications_count = scopus_papers_count_estimator(scopus_topics)

    return jsonify(
        {
            'scientific_activity': publications_count / 500
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
