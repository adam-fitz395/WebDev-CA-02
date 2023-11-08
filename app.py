from crypt import methods
from flask import Flask, render_template, request, session  # from module import Class.

import os
import hfpy_utils
import swim_utils

app = Flask(__name__)

app.secret_key = os.urandom(12)


@app.get("/base")
def base():
    sample_title = "Swimmer Select"
    return render_template("base.html", title=sample_title)


@app.post("/chart")
def display_chart():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    thisswimmer = session.get("swimmer")
    event = request.form["event"]
    event = str(event).replace(" ", "")

    thisFile = None

    for file in files:
        if thisswimmer in file and event in file:
            thisFile = file
            break
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data(thisFile)

    converts.reverse()
    the_times.reverse()

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


@app.get("/")
@app.get("/getswimmers")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.post("/displayevents")
def get_swimmer_events():
    events = set()

    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")

    swimmer = request.form["swimmer"]
    session["swimmer"] = swimmer

    for file in files:
        if swimmer + "-" in file:
            swimmer_data = swim_utils.get_swimmers_data(file)
            events.add(f"{swimmer_data[2]} - {swimmer_data[3]}")

    return render_template("event.html", title="Select an event", data=sorted(events))


if __name__ == "__main__":
    app.run(debug=True)  # Starts a local (test) webserver, and waits... forever.
