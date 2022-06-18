from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello_world():
    data = request.get_json()
    if data["request"]["command"] in ["вездекод", "не интеллектуальные коты", "вездеход"]:
        text = "Привет вездекодерам!"
    else:
        text = "Не привет"
    ans = {
        "response": {
            "text": text,
            "end_session": False
        },
        "session": {derived_key: data["session"][derived_key] for derived_key in ['session_id', 'user_id', 'message_id']},
        "version": data["version"]
    }
    return ans
