from flask import Flask, render_template
from steamapi import core, user

app = Flask("Steamer")
core.APIConnection(api_key="YOURKEYHERE")

@app.route('/user/<name>')
def hello(name=None):
  try:
    try:
      steam_user = user.SteamUser(userid=int(name))
    except ValueError: # Not an ID, but a vanity URL.
      steam_user = user.SteamUser(userurl=name)
    name = steam_user.name
    content = "Your real name is {0}. You have {1} friends and {2} games.".format(steam_user.real_name,
                                                                                  len(steam_user.friends),
                                                                                  len(steam_user.games))
    img = steam_user.avatar
    return render_template('hello.html', name=name, content=content, img=img)
  except Exception as ex:
    # We might not have permission to the user's friends list or games, so just carry on with a blank message.
    return render_template('hello.html', name=name)
  
if __name__ == '__main__':
  app.run()
