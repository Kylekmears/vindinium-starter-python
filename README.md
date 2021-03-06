Note on changes I've made: Running client.py will create a command line interactive mode in which Vindinium can be played.  Moves, game states, wins and losses are tracked.  Students and bot enthusiasts can then use supervised learning methods to train a bot to play like them.

![Alt text](https://github.com/Kylekmears/vindinium-starter-python/blob/master/vindiniumInterface.png "Interface Example")

Works on python3.  Untested on python2.

Install deps:

    pip install -r requirements.txt

Run with:

    python client.py <key> <[training|arena]> <number-of-games-to-play> [server-url]

Examples:

    python client.py mySecretKey arena 10
    python client.py mySecretKey training 10 http://localhost:9000
