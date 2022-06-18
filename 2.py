from operator import add

from flask import Flask, request

app = Flask(__name__)

sessions = {}
questions = ['Ты хочешь глубже узнать мир IT?',
             'Умеешь пользоваться консолью Windows?',
             'Знаешь хотя бы один язык программирования?',
             'Разговаривал ли ты со змеёй?',
             'Боишся ли ты порабощения человечества машинами?',
             'Сильно ли ты хорош в математике?',
             'У тебя есть опыт в веб-разработке?',
             'Умеешь выходить из VIM?']

changes = [
    {
        "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "n": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
        "y": [1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        "n": [0, 0, 1, 0, 0, 1, 0, 0, 0, 0]
    },
    {
        "y": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        "n": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
        "y": [0, 1, 0, 0, 1, 0, 1, 0, 0, 1],
        "n": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    },
    {
        "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "n": [0, -1, 0, 0, 0, 0, 0, 0, 0, -1]
    },
    {
        "y": [0, 1, 0, 0, 1, 1, 0, 1, 0, 0],
        "n": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    {
        "y": [1, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        "n": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    },
    {
        "y": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "n": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
]

answers = [
    'WEB',
    'Computer vision',
    'Game Dev',
    'Мобильная разработка',
    'Анализ данных',
    'Дизайн интерфейсов',
    'Оптимизация и RL',
    'VK Mini Apps',
    'Back End',
    'Маруся'
]


@app.route("/", methods=["POST"])
def hello_world():
    global sessions
    data = request.get_json()
    session = sessions.get(data["session"]["session_id"], [0] * 10)
    text = data["request"]["command"]

    if data["session"]["message_id"] >= 8:
        answer = answers[session.index(max(session))]
        return {
            "response": {
                "text": answer + ' - то, что вам надо',
                "buttons": [],
                "end_session": True
            },
            "session": {derived_key: data["session"][derived_key] for derived_key in ['session_id', 'user_id', 'message_id']},
            "version": data["version"]
        }
    session = list(map(add, session, changes[data["session"]["message_id"]]["y"]))
    sessions[data["session"]["session_id"]] = session
    print(session)
    text = questions[data["session"]["message_id"]]


    ans = {
        "response": {
            "text": text,
            "buttons": [
                {
                    "title": "Да",
                    "payload": {}
                },
                {
                    "title": "Нет",
                    "payload": {}
                },
            ],
            "end_session": False
        },
        "session": {derived_key: data["session"][derived_key] for derived_key in ['session_id', 'user_id', 'message_id']},
        "version": data["version"]
    }

    return ans
