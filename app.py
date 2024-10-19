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

# Home Route
@app.route('/')
def home():
    # Check if the team is already registered
    if 'team_id' not in session:
        return redirect(url_for('register'))  # Redirect to register if team is not set
    return redirect(url_for('ready'))

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        team_name = request.form.get('team_name')
        session['team_id'] = team_name
        session['current_round'] = 0  # Start at round 0
        session['clue'] = None
        return redirect(url_for('ready'))  # Redirect to the ready state
    return render_template('register.html')

# Ready Route
@app.route('/ready')
def ready():
    if 'team_id' not in session:
        return redirect(url_for('register'))  # Ensure the team is registered
    if session.get('current_round', 0) >= total_rounds:
        return redirect(url_for('complete'))  # If rounds > total, go to completion

    return render_template('ready.html')  # Display the ready screen

# Start Game / Get First Clue Route
@app.route('/start_game', methods=['POST'])
def start_game():
    if 'team_id' not in session:
        return redirect(url_for('register'))  # Ensure the team is registered
    
    # Move to the first round
    session['current_round'] += 1
    session['clue'] = clue_stack[session['current_round'] - 1]['clue']
    return redirect(url_for('play_round'))

# Play Round (display clue and take answer)
@app.route('/play_round', methods=['GET', 'POST'])
def play_round():
    if 'team_id' not in session or 'clue' not in session:
        return redirect(url_for('register'))

    if request.method == 'POST':
        answer = request.form.get('answer')
        current_round = session['current_round']
        correct_answer = clue_stack[current_round - 1]['answer']
        
        if answer == correct_answer:
            session['message'] = "Correct! Proceed to the next round."
            if current_round < total_rounds:
                session['current_round'] += 1
                session['clue'] = clue_stack[current_round]['clue']  # Load next clue
            else:
                return redirect(url_for('complete'))  # End game when all rounds complete
        else:
            session['message'] = "Incorrect answer. Try again."
    
    return render_template('play_round.html', clue=session['clue'], message=session.get('message', ''))

# Completion Route
@app.route('/complete')
def complete():
    return render_template('game_complete.html')

# Debug route to clear session for testing purposes
@app.route('/reset')
def reset():
    session.clear()
    return "Session cleared!"

if __name__ == '__main__':
    app.run(debug=True)