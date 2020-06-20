from flask import Flask, jsonify, request
from argparse import ArgumentParser


app = Flask(__name__)





def args_parse():
    parser = ArgumentParser(description='Server')
    parser.add_argument('--ip', required=False, type=str, default='0.0.0.0')
    parser.add_argument('--port', required=False, type=int, default=5000)
    parser.add_argument('--path-to-names-list', required=True, type=str)
    return parser.parse_args()


def main():
    args = args_parse()
    app.run(host=args.ip, debug=False, port=args.port)


if __name__ == '__main__':
    main()
