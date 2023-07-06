from flask import Flask, render_template, request
from pymongo import MongoClient


#from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)

uri = "mongodb+srv://jjames71396:qUFaF5pYhmjxAxPD@cluster0.ldooqi5.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

client.db.command("dropDatabase")

db = client['game_database']
collection = db['game_states']


# Game parameters
pile_sizes = [0, 0, 0]
min_pickup = 1
max_pickup = 3
players = {}


document = {"name": "game_state",'started': False,'p1': '','p2': '','turn': 1,'pile_sizes': pile_sizes, 'min_pickup': min_pickup, 'max_pickup': max_pickup}
inserted_document = collection.update_one({'name':'game_state'},{'$set': document})

@app.route('/')
def index():
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    # Retrieve the game state from the database
    print(game_state)
    turn = None
    cur_player = None
    p = players
    if game_state["p1"] == '':
        game_state = None
        p = None
    elif game_state["p2"] == '':
        game_state = None
        p = None
    elif not game_state['started']:
        game_state = None
    else:
        pile_sizes = game_state['pile_sizes']
        if game_state['turn'] == 1:
            cur_player = game_state['p1']
        else:
            cur_player = game_state['p2']
            
        
    # Render the template with the game state and player names
    return render_template('index.html', game_state=game_state, players=p, current_player=cur_player)

@app.route('/players', methods=['POST'])
def players():
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    if game_state['p1'] == '':
        player1 = request.form['player1']
        player2 = None
    elif game_state['p2'] == '':
        player1 = None
        player2 = request.form['player2']
    
    if player1 is not None and player1 != '':
        document = {'p1': player1}
        inserted_document = collection.update_one(query,{'$set': document})
    elif player2 is not None and player2 != '':
        document = {'p2': player2}
        inserted_document = collection.update_one(query,{'$set': document})
    # Redirect back to the index page
    return index()

@app.route('/pick', methods=['POST'])
def pick():
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    pile_number = int(request.form['pile_number']) - 1
    num_stones = int(request.form['num_stones'])
    if pile_number < 0:
        pile_number = 0
    elif pile_number > 2:
        pile_number = 2
    # Update the game state
    pile_sizes[pile_number] -= num_stones
    players[game_state['turn']] += num_stones

    # Switch players
    if game_state['turn'] == 1:
        document = {'turn': 2}
        inserted_document = collection.update_one(query,{'$set': document})
    else:
        document = {'turn': 1}
        inserted_document = collection.update_one(query,{'$set': document})
    # Save the updated game state to the database
    collection.update_one(query, {'$set': {'pile_sizes': pile_sizes}})

    # Redirect back to the index page
    return index()


@app.route('/start', methods=['POST'])
def start():
    global pile_sizes, current_player, players, min_pickup, max_pickup
    query = {"name": "game_state"} 
    game_state = collection.find_one(query)
    # Retrieve the game parameters from the form
    pile_sizes = [int(request.form['pile1']), int(request.form['pile2']), int(request.form['pile3'])]
    min_pickup = int(request.form['min_pickup'])
    max_pickup = int(request.form['max_pickup'])
    players = {
        1: 0,
        2: 0
    }

    # Save the initial game state to the database
    collection.update_one(query, {'$set': {'pile_sizes': pile_sizes, 'min_pickup': min_pickup, 'max_pickup': max_pickup, 'started': True}})
    print(pile_sizes)
    # Redirect back to the index page
    return index()


if __name__ == '__main__':
    app.run(debug=True)