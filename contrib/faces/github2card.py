#!/usr/bin/env python
# github2card.py (Feb 2017) by Jan-Piet Mens
# Usage: github2card username
#
# Read the Github profile of `username' and obtain user's
# name and avatar_url to create a CARD JSON payload to
# be published retained to owntracks/username/device/info
#
# You probably want to do this:
#
# github2card.py jjolie  > card.json
# mosquitto_pub -t owntracks/jane/phone/info -r -f card.json
#
# Note: the two commands cannot be piplelined (mosquitto_pub -l)
# because of a bug in mosquitto_pub: https://bugs.eclipse.org/bugs/show_bug.cgi?id=478917
# If you have a newer version it should work fine.

import requests
import base64
import json
import sys

def user_profile(username):
    url = "https://api.github.com/users/" + username
    r = requests.get(url)
    if r.status_code != 200:
        print "User not found; response:", r
        sys.exit(1)

    profile = json.loads(r.content)
    name = profile.get('name')
    avatar_url = profile.get('avatar_url', None)

    if name is None:
        print "User has no name; stopping"
        sys.exit(1)

    if avatar_url is None:
        print "No avatar for this user"
        sys.exit(1)

    # sizing an avatar works only for "real" avatars; not
    # for the github-generated thingies (identicons)
    avatar_url = avatar_url + '&size=40'

    r = requests.get(avatar_url)
    if r.status_code != 200:
        print "Cannot retrieve avatar for this user:", r
        sys.exit(1)

    f = open(username + ".png", "wb")
    f.write(r.content)
    f.close()

    card = {
        '_type': 'card',
        'name' : name,
        'face' : base64.b64encode(r.content)
    }

    print json.dumps(card)


if __name__ == '__main__':
    (username) = sys.argv[1]
    user_profile(username)