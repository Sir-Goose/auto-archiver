import os
import sys
from flask import Flask, render_template, request, session, redirect, url_for



app = Flask(__name__)

@app.route('/', methods=['GET'])
def archive():
    query = request.args.get('query')
    return render_template('home.html')


if __name__ == '__main__':
    default_port = 5431

    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port.")
            port = default_port
    else:
        port = default_port

    app.run(host="0.0.0.0", port=port)
