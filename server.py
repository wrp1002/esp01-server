from flask import Flask, Response, abort
import json

currentID = 0
esps = []

port = 8090
app = Flask(__name__)



class ESP01:
    def __init__(self, id, name, state):
        self.id = str(id)
        self.name = name
        self.state = state

    def Enable(self):
        self.state = "on"

    def Disable(self):
        self.state = "off"

    def IsPowered(self):
        return self.state == "on"

    def ToDict(self):
        return {
            'name': self.name,
            'id': self.id,
            'state': self.state,
            'powered': self.IsPowered(),
        }


def MakeESP(name, state):
    global esps
    global currentID
    esps.append(ESP01(currentID, name, state))
    currentID += 1


@app.route("/")
def get_index():
    global esps
    res = "<style>body{font-size:18px;}</style>"
    res += "<h4>ESP-01s:</h4>"
    res += "<ul>"
    for esp in esps:
        res += "<li>" + "ID:" + esp.id + " Name:" + esp.name + " State:" + esp.state + " Powered:" + str(esp.IsPowered()) +"</li>"
    res += "</ul>"

    res += "<br><br>Go to /get/{id} to view specific information about an esp01"
    res += "<br><br>Go to /set/{id}/{state} to set esp01 state (on or off)"

    return Response(res, 200)

@app.route("/get/<id>")
def get_esp01(id):
    if not id:
        abort(400)

    for esp in esps:
        if esp.id == id:
            return Response(json.dumps(esp.ToDict()))

    return Response("No ESP01 found with that ID", 400)

@app.route("/set/<id>/<state>")
def set_esp01(id, state):
    if not id or not state:
        abort(400)

    if state.lower() not in ["on", "off"]:
        return Response("State must be on or off", 400)

    for esp in esps:
        if esp.id == id:
            esp.state = state
            return Response(json.dumps(esp.ToDict()))

    return Response("No ESP01 found with that ID", 400)





def main():
    MakeESP("Test ESP01", "on")
    MakeESP("Another Test ESP01", "off")

    app.run("0.0.0.0", port, True)







if __name__ == "__main__":
    main()
