""" main.py is the top level script.

Return "Hello World" at the root URL.
"""

from flask import Flask
from flask import render_template
from steamapi import * # All submodules.

app = Flask(__name__.split('.')[0])

@app.route('/user/<name>')
def hello(name=None):
    try:
        core.APIConnection(api_key="YOURKEYHERE", settings={'precache': False})
        if core.APIConnection()._api_key == "YOURKEYHERE" or
           core.APIConnection()._api_key == "":
            return "Uh-oh, you forgot to set the API key!", 503
        try:
            steam_user = user.SteamUser(userid=int(name))
        except ValueError: # Not an ID, but a vanity URL.
            steam_user = user.SteamUser(userurl=name)
        name = steam_user.name
        content = "Your real name is {0}. You have {1} friends and {2} games.".format(steam_user.real_name,
                                                                                      len(steam_user.friends),
                                                                                      len(steam_user.games))
        img = steam_user.avatar
    except Exception as ex:
        # We might not have permission to the user's friends list or games, so just carry on with a blank message.
        content = None
        img = None
    return render_template('hello.html', name=name, content=content, img=img)
  
if __name__ == "__main__":
    app.run()