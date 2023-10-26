#!/usr/bin/python3
""" States and State """

from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/states/<id>', strict_slashes=False)
@app.route('/states', strict_slashes=False)
def states_and_state(id=None):
    """ States and State content """
    # sort states by name from a to z
    slist = sorted(storage.all(
        State).values(), key=lambda x: x.name)
    if id is None:
        return render_template("9-states.html", sorted_states_list=slist,
                               states=True)
    else:
        # sort cities by name from a to z
        for s in slist:
            if s.id == id:
                s.cities.sort(key=lambda x: x.name)
                return render_template("9-states.html", state=s)
    return render_template("9-states.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
