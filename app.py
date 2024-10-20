from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Clue stack with answers
clue_stack = [
    {"clue": "Clue 1: Look under the old oak tree.", "answer": "oak"},
    {"clue": "Clue 2: Check the drawer of the desk.", "answer": "desk"},
    {"clue": "Clue 3: The key is behind the painting.", "answer": "painting"},
    {"clue": "Clue 4: Find the book with a red cover.", "answer": "book"},
    {"clue": "Clue 5: The next clue is in the kitchen.", "answer": "kitchen"},
    {"clue": "Clue 6: Look for the hidden compartment.", "answer": "compartment"},
    {"clue": "Clue 7: The clue is near the window.", "answer": "window"},
    {"clue": "Clue 8: Check the last shelf in the library.", "answer": "shelf"},
    {"clue": "Clue 9: The next hint is in your backpack.", "answer": "backpack"},
    {"clue": "Clue 10: Look where you keep your shoes.", "answer": "shoes"}
]

total_teams = 5
total_rounds = 5

# Assigned clues {team_id: {round_num: clue_id}}
assigned_clues = {team_id: [] for team_id in range(1, total_teams + 1)}

@app.route('/')
def home():
    team_id = session.get('team_id')
    if team_id is None:
        return redirect(url_for('register'))

    current_round = len(assigned_clues[team_id]) + 1

    # If all rounds are completed
    if current_round > total_rounds:
        return render_template('home.html', message="You've completed all the rounds.")

    clue = session.get('clue')  # Get the current clue from session

    return render_template('home.html', clue=clue, team_id=team_id, current_round=current_round)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if restrict_reregistration and 'team_id' in session:
            return redirect(url_for('home'))  # Prevent re-registration if restriction is on

        team_id = int(request.form.get('team_id'))
        session['team_id'] = team_id
        session['clue'] = None
        return redirect(url_for('home'))
    
    return render_template('register.html')

# Function to verify if the answer is correct
def CorrectAns(submitted_answer, clue_id):
    correct_answer = clue_stack[clue_id]["answer"]
    return submitted_answer.strip().lower() == correct_answer.lower()

@app.route('/get_clue', methods=['POST'])
def get_clue():
    team_id = session.get('team_id')

    if team_id is None:
        return redirect(url_for('home'))

    current_round = len(assigned_clues[team_id]) + 1

    if current_round > total_rounds:
        return redirect(url_for('home'))

    # Get the submitted answer (if provided)
    submitted_answer = request.form.get('answer')

    # Get the current clue ID
    if len(assigned_clues[team_id]) > 0:
        current_clue_id = assigned_clues[team_id][-1]
    else:
        current_clue_id = None

    # If there's a current clue, validate the answer
    if current_clue_id is not None and submitted_answer:
        if not CorrectAns(submitted_answer, current_clue_id):
            session['clue'] = clue_stack[current_clue_id]["clue"]
            return render_template('home.html', clue=session['clue'], team_id=team_id, current_round=current_round, message="Wrong answer! Try again.")

    # Get clues already assigned in this round to other teams
    clues_taken_this_round = [assigned_clues[t][current_round - 1] for t in assigned_clues if len(assigned_clues[t]) >= current_round]
    
    # Get clues already assigned to this team in previous rounds
    clues_taken_by_team = assigned_clues[team_id]

    # Available clues for this team in this round
    available_clues = [i for i in range(len(clue_stack)) if i not in clues_taken_this_round and i not in clues_taken_by_team]

    if available_clues:
        clue_id = random.choice(available_clues)  # Randomly select an available clue
        assigned_clues[team_id].append(clue_id)
        session['clue'] = clue_stack[clue_id]["clue"]  # Store the clue in session
    else:
        session['clue'] = "No clues available."  # If somehow no clues left (unlikely)

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', assigned_clues=assigned_clues, clue_stack=clue_stack, restrict_reregistration=restrict_reregistration)

@app.route('/toggle_registration', methods=['POST'])
def toggle_registration():
    global restrict_reregistration
    restrict_reregistration = not restrict_reregistration  # Toggle the registration restriction
    return redirect(url_for('dashboard'))

@app.route('/reset_event', methods=['POST'])
def reset_event():
    global assigned_clues
    assigned_clues = {team_id: [] for team_id in range(1, total_teams + 1)}  # Reset all clues
    session.clear()  # Clear all sessions to allow new registrations
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
