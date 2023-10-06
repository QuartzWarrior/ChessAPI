from stockfish import Stockfish
from ujson import dumps
stockfish = Stockfish(path="stockfish_15.1_linux_x64/stockfish-ubuntu-20.04-x86-64", depth=20, parameters={"UCI_Elo": 3532, "Hash": 1024, "Threads": 2})
from flask import Flask, request, jsonify, Response
app = Flask(__name__)
@app.route("/fen")
def fen_move():
    fen = request.args.get('fen').replace("%20"," ")
    if stockfish.is_fen_valid(fen):
        stockfish.set_fen_position(fen)
        bestmove = stockfish.get_best_move_time(int(request.args.get('time')))
        try:
            capture = a.name if (a := stockfish.get_what_is_on_square(bestmove[2:])) else "nothing"
        except:
            capture = "nothing"
        return Response(dumps({"bestmove": bestmove, "piece": stockfish.get_what_is_on_square(bestmove[:2]).name, "capture": capture, "invalid": False}), mimetype='application/json')
    else:
        return Response(dumps({"invalid": True}))
if __name__ == '__main__':app.run(host="0.0.0.0", port=443, ssl_context=("server.crt", "server.key"))


#let xhr = new XMLHttpRequest();
#xhr.open('GET', `https://157.230.230.57:443/fen?fen=${document.getElementsByTagName("vertical-move-list")[0].board.game.getFEN()}`, false)
#xhr.send()
#xhr.responseText
