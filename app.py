from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Clue stack with their corresponding answers
clue_stack = [
    {"clue": "Clue 1: Look under the old oak tree.", "answer": "Answer1"},
    {"clue": "Clue 2: Check the drawer of the desk.", "answer": "Answer2"},
    {"clue": "Clue 3: The key is behind the painting.", "answer": "Answer3"},
    {"clue": "Clue 4: Find the book with a red cover.", "answer": "Answer4"},
    {"clue": "Clue 5: The next clue is in the kitchen.", "answer": "Answer5"},
    {"clue": "Clue 6: Look for the hidden compartment.", "answer": "Answer6"},
    {"clue": "Clue 7: The clue is near the window.", "answer": "Answer7"},
    {"clue": "Clue 8: Check the last shelf in the library.", "answer": "Answer8"},
    {"clue": "Clue 9: The next hint is in your backpack.", "answer": "Answer9"},
    {"clue": "Clue 10: Look where you keep your shoes.", "answer": "Answer10"}
]

total_teams = 5
total_rounds = 5

# Assigned clues {team_id: [clue_id]}
assigned_clues = {team_id: [] for team_id in range(1, total_teams + 1)}

# Route: Home Page - Registration
@app.route('/')
def home():
    if 'team_id' in session:
        return redirect(url_for('ready'))
    return render_template('register.html')

# Route: Register Team
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        session['team_id'] = random.randint(1, total_teams)
        session['team_name'] = team_name
        session['round'] = 0
        session['clue'] = None
        session['message'] = None
        return redirect(url_for('ready'))
    return render_template('register.html')

# Route: Ready State
@app.route('/ready')
def ready():
    team_name = session.get('team_name')
    if team_name is None:
        return redirect(url_for('home'))
    return render_template('ready.html', team_name=team_name)

# Route: Start Game
@app.route('/start_game', methods=['POST'])
def start_game():
    team_id = session.get('team_id')
    if team_id is None:
        return redirect(url_for('home'))

    session['round'] = 1
    clue_id = random.choice([i for i in range(len(clue_stack)) if i not in assigned_clues[team_id]])
    assigned_clues[team_id].append(clue_id)
    session['clue'] = clue_stack[clue_id]["clue"]
    return redirect(url_for('play_round'))

# Route: Play Rounds
@app.route('/play_round', methods=['GET', 'POST'])
def play_round():
    team_id = session.get('team_id')
    if team_id is None:
        return redirect(url_for('home'))

    current_round = session.get('round')
    if current_round > total_rounds:
        return redirect(url_for('game_complete'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        clue_id = assigned_clues[team_id][-1]
        correct_answer = clue_stack[clue_id]["answer"]

        if answer == correct_answer:
            # Correct answer, move to next round
            current_round += 1
            session['round'] = current_round
            session['message'] = "Correct! Moving to next round."
            if current_round > total_rounds:
                return redirect(url_for('game_complete'))
            clue_id = random.choice([i for i in range(len(clue_stack)) if i not in assigned_clues[team_id]])
            assigned_clues[team_id].append(clue_id)
            session['clue'] = clue_stack[clue_id]["clue"]
            return redirect(url_for('play_round'))
        else:
            # Wrong answer
            session['message'] = "Incorrect answer. Try again."

    return render_template('play_round.html', clue=session.get('clue'), round=current_round, message=session.get('message'))

# Route: Game Complete
@app.route('/game_complete')
def game_complete():
    return render_template('game_complete.html')

# Route: Dashboard for admins to track progress
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', assigned_clues=assigned_clues, clue_stack=clue_stack)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
