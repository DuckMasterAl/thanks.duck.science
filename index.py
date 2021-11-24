import os, sys, quart, tokens
from quart import Quart, render_template, redirect, request, make_response
from quart_motor import Motor
app = Quart(__name__)

app.config["MONGO_URI"] = tokens.mongo
mongo = Motor(app)
app.url_map.strict_slashes = False

@app.before_request
async def path_redirects():
    path = request.path
    if path != '/' and path.endswith('/'):# trailing slash
        path = path[:-1]
    if path.endswith('.html'):# removes .html from requests
        path = path[:-5]
    if path == '/index':# /index -> /
        path = '/'
    if path != request.path:# redirect if something has changed
        return redirect(path)

if sys.platform != 'linux':# Add no cache headers if running locally
    async def cache_headers(r):
        r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        r.headers["Pragma"] = "no-cache"
        r.headers["Expires"] = "0"
        return r
    app.after_request(cache_headers)

@app.route('/thanks/<string:code>')
async def message(code):
    db = await mongo.db.messages.find_one({"_id": str(code)})
    if db is None:
        return await render_template('404.html')
    return await render_template('card.html', name=db['name'], message=db['message'].split("\n"))

@app.route('/license')
@app.route('/license.txt')
async def license():
    return await app.send_static_file("license.txt")

@app.route('/robots')
@app.route('/robots.txt')
async def robots():
    return await app.send_static_file("robots.txt")

@app.errorhandler(404)
async def page_not_found(e):
    return await make_response(await render_template("404.html"), 404)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1125, debug=False if sys.platform == 'linux' else True)
