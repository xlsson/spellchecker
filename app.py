#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Flask application for SpellChecker
"""

from flask import Flask, render_template, request
from spellchecker_flask import SpellCheckerFlask

app = Flask(__name__)
spellchecker = SpellCheckerFlask()

@app.route("/", methods=["POST", "GET"])
def main():
    """ Find word """
    message = None
    if request.method == "POST":
        message = spellchecker.find_word(request.form["word"])

    return render_template("index.html", message=message)

@app.route("/allwords")
def allwords():
    """ Show all words in wordlist """
    return render_template("allwords.html", allwords=spellchecker.allwords_sorted)

@app.errorhandler(404)
def page_not_found(e):
    """
    Handler for page not found 404
    """
    #pylint: disable=unused-argument
    return "Flask 404 here, but not the page you requested."


@app.errorhandler(500)
def internal_server_error(e):
    """
    Handler for internal server error 500
    """
    #pylint: disable=unused-argument,import-outside-toplevel
    import traceback
    return "<p>Flask 500<pre>" + traceback.format_exc()


if __name__ == "__main__":
    app.run(debug=True)
