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

questions_tts = ['Ты хочешь ^глубже^ узнать мир ай ти?',
                 '^Умеешь^ пользоваться консолью в`индоус?',
                 'Знаешь хотя бы ^один^ язык программирования?',
                 '^Разговаривал^ ли ты со змеёй?',
                 '^Боишся^ ли ты порабощения человечества машинами?',
                 'Сильно ли ты хорош в математике?',
                 'У тебя есть опыт в веб разработке?',
                 'Умеешь выходить из ^вим^?']

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

answers_tts = [
    'веб',
    'компьютерное зрение',
    'разработка игр',
    'Мобильная разработка',
    'Анализ данных',
    'Дизайн интерфейсов',
    'Оптимизация',
    'Вк м`ини эпс',
    'бэк энд',
    'Маруся'
]


@app.route("/")
def home():
    return 'по ссылке <pre>https://not-intellectual-cats-marusya.herokuapp.com/1</pre>' \
           ' первое задание, а <pre>https://not-intellectual-cats-marusya.herokuapp.com/2' \
           '</pre> - второе<br/><sub>Мы просто не знали, что садть<br/>а ещё там третье задание выполнено</sub>'


@app.route("/1", methods=["POST"])
def first():
    data = request.get_json()
    if data["request"]["command"] in ["вездекод", "не интеллектуальные коты", "вездеход"]:
        text = "Привет вездекодерам!"
        tts = "Привет ^вездек`одерам^"
    else:
        text = "Не привет"
        tts = "Не привет"
    ans = {
        "response": {
            "text": text,
            "tts": tts,
            "end_session": False
        },
        "session": {derived_key: data["session"][derived_key] for derived_key in
                    ['session_id', 'user_id', 'message_id']},
        "version": data["version"]
    }
    return ans


@app.route("/2", methods=["POST"])
def second():
    global sessions
    data = request.get_json()
    session = sessions.get(data["session"]["session_id"], [0] * 10)
    text = data["request"]["command"]

    if data["session"]["message_id"] >= 8:
        answer = answers[session.index(max(session))]
        tts = answers_tts[session.index(max(session))]
        return {
            "response": {
                "text": answer + ' - то, что вам надо',
                "tts": tts + ' - то, что ^вам^ надо',
                "buttons": [],
                "end_session": True
            },
            "session": {derived_key: data["session"][derived_key] for derived_key in
                        ['session_id', 'user_id', 'message_id']},
            "version": data["version"]
        }

    key = "n"
    if text in ["да", "ага", "именно так"]:
        key = "y"
    session = list(map(add, session, changes[data["session"]["message_id"]]["y"]))
    sessions[data["session"]["session_id"]] = session
    print(session)
    text = questions[data["session"]["message_id"]]
    tts = questions_tts[data["session"]["message_id"]]

    ans = {
        "response": {
            "text": text,
            "tts": tts,
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
        "session": {derived_key: data["session"][derived_key] for derived_key in
                    ['session_id', 'user_id', 'message_id']},
        "version": data["version"]
    }

    return ans
