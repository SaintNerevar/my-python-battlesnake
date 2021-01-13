import os
import random

import cherrypy

"""
This is a simple Battlesnake server written in Python.
For instructions see https://github.com/BattlesnakeOfficial/starter-snake-python/README.md
"""


class Battlesnake(object):
    @cherrypy.expose
    @cherrypy.tools.json_out()
    def index(self):
        # This function is called when you register your Battlesnake on play.battlesnake.com
        # It controls your Battlesnake appearance and author permissions.
        # TIP: If you open your Battlesnake URL in browser you should see this data
        return {
            "apiversion": "1",
            "author": "",  # TODO: Your Battlesnake Username
            "color": "#888888",  # TODO: Personalize
            "head": "default",  # TODO: Personalize
            "tail": "default",  # TODO: Personalize
        }

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def start(self):
        # This function is called everytime your snake is entered into a game.
        # cherrypy.request.json contains information about the game that's about to be played.
        data = cherrypy.request.json

        print("START")
        return "ok"

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # This function is called on every turn of a game. It's how your snake decides where to move.
        # Valid moves are "up", "down", "left", or "right".
        data = cherrypy.request.json

        head = (data["you"]["head"]["x"], data["you"]["head"]["y"])
        up = (head[0], head[1]+1)
        down = (head[0], head[1]-1)
        left = (head[0]-1, head[1])
        right = (head[0]+1, head[1])

        board_height = data["board"]["height"]
        board_width = data["board"]["width"]

        body = [(part["x"], part["y"]) for part in data["you"]["body"]]
        
        eligible_moves = []
        directions = [up, down, left, right]


        # Check for wall collision
        for index, (x, y) in enumerate(directions):
            if (x < 0 or x >= board_width):
                continue
            if (y < 0 or y >= board_height):
                continue
            eligible_moves.append(index)

        # Check for self collision
        for index in list(eligible_moves):
            if directions[index] in body:
                eligible_moves.remove(index)

        # Choose a random direction to move in among eligible choices
        possible_moves = ["up", "down", "left", "right"]
        move = possible_moves[random.choice(eligible_moves)]

        print(f"MOVE: {move}")
        return {"move": move}

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def end(self):
        # This function is called when a game your snake was in ends.
        # It's purely for informational purposes, you don't have to make any decisions here.
        data = cherrypy.request.json

        print("END")
        return "ok"


if __name__ == "__main__":
    server = Battlesnake()
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update(
        {"server.socket_port": int(os.environ.get("PORT", "8080")),}
    )
    print("Starting Battlesnake Server...")
    cherrypy.quickstart(server)
