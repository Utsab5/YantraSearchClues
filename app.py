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

# Assigned clues {team_id: {round_num: clue_id}}
assigned_clues = {team_id: [] for team_id in range(1, total_teams + 1)}
current_round = 0

# Flag to toggle re-registration permission
restrict_reregistration = True

@app.route('/')
def home():
    team_id = session.get('team_id')
    if team_id is None:
        return redirect(url_for('register'))

    clue = session.get('clue')  # Get the current clue from session
    message = session.get('message', None)  # Feedback message

    # Initialize current_round based on how many clues have been assigned to this team
    current_round = len(assigned_clues[team_id])

    # If no clue is assigned, set the current round correctly before clue retrieval
    if not clue:
        current_round = len(assigned_clues[team_id])

    return render_template('home.html', clue=clue, team_id=team_id, current_round=current_round, message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if restrict_reregistration and 'team_id' in session:
            return redirect(url_for('home'))  # Prevent re-registration if restriction is on

        team_id = int(request.form.get('team_id'))
        session['team_id'] = team_id
        session['clue'] = None
        session['message'] = None  # Clear any old message
        return redirect(url_for('home'))
    
    return render_template('register.html')

@app.route('/get_clue', methods=['POST'])
def get_clue():
    team_id = session.get('team_id')

    if team_id is None:
        return redirect(url_for('home'))

    current_round = len(assigned_clues[team_id]) + 1

    if current_round > total_rounds:
        return redirect(url_for('home'))

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

    session['message'] = None  # Clear message when getting a new clue
    return redirect(url_for('home'))

# Add the submit_answer route to handle answer submission
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    team_id = session.get('team_id')
    if team_id is None:
        return redirect(url_for('home'))  # Team must be registered

    current_round = len(assigned_clues[team_id])

    # If current round exceeds total rounds, redirect to home
    if current_round > total_rounds:
        return redirect(url_for('home'))

    answer = request.form.get('answer')
    correct_answer = clue_stack[assigned_clues[team_id][-1]]['answer']  # Get last clue's correct answer

    if answer == correct_answer:
        # Proceed to next round if the answer is correct
        return redirect(url_for('get_clue'))  # Redirect to get next clue
    else:
        # Show message if the answer is wrong
        return render_template('home.html', team_id=team_id, clue=session.get('clue'), current_round=current_round, message="Incorrect answer. Try again.")


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
