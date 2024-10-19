from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Total clues and number of teams
total_clues = 10
total_teams = 5
total_rounds = 5

# Clue stack (global, so every session shares this data)
clue_stack = [
    "Clue 1: Look under the old oak tree.",
    "Clue 2: Check the drawer of the desk.",
    "Clue 3: The key is behind the painting.",
    "Clue 4: Find the book with a red cover.",
    "Clue 5: The next clue is in the kitchen.",
    "Clue 6: Look for the hidden compartment.",
    "Clue 7: The clue is near the window.",
    "Clue 8: Check the last shelf in the library.",
    "Clue 9: The next hint is in your backpack.",
    "Clue 10: Look where you keep your shoes."
]

# Store assigned clues for each team and each round
assigned_clues = {team_id: [] for team_id in range(1, total_teams + 1)}

@app.route('/')
def home():
    team_id = session.get('team_id')
    round_num = len(assigned_clues.get(team_id, [])) + 1

    # If all rounds are done, show completion message
    if round_num > total_rounds:
        return render_template('home.html', message="Congratulations! You've completed all the rounds.")

    clue = session.get('clue')  # Get the current clue from session
    return render_template('home.html', clue=clue, team_id=team_id, round_num=round_num)

@app.route('/register_team', methods=['POST'])
def register_team():
    team_id = int(request.form.get('team_id'))
    session['team_id'] = team_id
    session['clue'] = None
    return redirect(url_for('home'))

@app.route('/get_clue', methods=['POST'])
def get_clue():
    team_id = session.get('team_id')

    if team_id is None:
        return redirect(url_for('home'))

    round_num = len(assigned_clues[team_id]) + 1

    if round_num > total_rounds:
        return redirect(url_for('home'))  # All rounds completed

    available_clues = [i for i in range(len(clue_stack)) if all(i not in assigned_clues[t] for t in range(1, total_teams + 1))]

    if available_clues:
        clue_id = random.choice(available_clues)  # Randomly select a clue
        assigned_clues[team_id].append(clue_id)
        session['clue'] = clue_stack[clue_id]  # Store the clue in session
    else:
        session['clue'] = "No clues left for this round."  # Debugging statement for no clues
    
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('team_id', None)
    session.pop('clue', None)
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', assigned_clues=assigned_clues, clue_stack=clue_stack)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
