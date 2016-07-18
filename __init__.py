#/usr/bin/env python
# -*- coding: utf-8 -*-
import flask, core

# Debug
# Set this to 'False' in a production environment.
debug = True

# Initialize Flask App
app = flask.Flask(__name__)

# Index route: renders the landing/home page from templates.
@app.route("/")
def index():
    return flask.render_template("index.html", isform=False)

# Enterprise route: this will be expanded upon in the future.
@app.route("/enterprise")
def enterprise():
    return flask.render_template("enterprise.html")

# Index route: renders output from API when input is posted.
@app.route("/", methods=['POST'])
def verify_doc_post():
    html_name = "render.html"

    url = flask.request.form['search']
    if url == "":
        return flask.render_template("index.html", isform=False)
    else:
        api_response = core.core().process_data(url)

    if api_response['error']:
        return flask.render_template(html_name, message=api_response['message'], iserror=True, isform=True)
    else:
        return flask.render_template(html_name, url=url, domain=core.core().get_domain(url), message=api_response['message'], user=api_response['data']['username'], title=api_response['data']['title'], timestamp=api_response['data']['timestamp_utc'], isuserverified=api_response['data']['user_verified'], iserror=False, isform=True)

#Link route: gathers the URL information from the given URI, rather than the form in index.
@app.route("/link", methods=['GET'])
def verify_button(link=False):
    link = flask.request.args.get('link')
    if not link:
        return flask.render_template("index.html", isform=False)
    else:
        api_response = core.core().process_data(link)

    if api_response['error']:
        return flask.render_template("render.html", message=api_response['message'], iserror=True, isform=True)
    else:
        return flask.render_template("render.html", url=link, domain=core.core().get_domain(link), message=api_response['message'], user=api_response['data']['username'], title=api_response['data']['title'], timestamp=api_response['data']['timestamp_utc'], isuserverified=api_response['data']['user_verified'], iserror=False, isform=True)

# Run app
if __name__ == '__main__':
    if debug:
        app.run(debug=True)
    else:
        app.run()