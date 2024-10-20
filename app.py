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

# Flag to toggle re-registration permission
restrict_reregistration = True

AnsGiven = 'C'##Correct

@app.route('/')
def home():

    global AnsGiven

    if AnsGiven != 'W':
        team_id = session.get('team_id')
        if team_id is None:
            return redirect(url_for('register'))

        current_round = len(assigned_clues[team_id]) + 1

        # If all rounds are completed
        if current_round > total_rounds:
            return render_template('home.html', message="You've completed all the rounds.")

        clue = session.get('clue')  # Get the current clue from session

        if not clue:
            current_round = len(assigned_clues[team_id])  # Show the correct round before clue retrieval

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

@app.route('/get_clue', methods=['POST'])
def get_clue():

    global AnsGiven
    team_id = session.get('team_id')

    if team_id is None:
        return redirect(url_for('home'))

    current_round = len(assigned_clues[team_id]) + 1

    if current_round > total_rounds:
        return redirect(url_for('home'))

    # Check the answer provided by the team
    Team_ans = request.form.get('answer')
    print(f"ANSWER GIVEN BY TEAM++++++++++++==================={Team_ans}")


    # The last clue assigned in the current round
    clue_id = assigned_clues[team_id][-1]  
    Correct_ans = clue_stack[clue_id]['answer']
    print(f"CORRECT ANS IS++++++++++++==================={Correct_ans}")

    # Compare the answers (case-insensitive)
    if Team_ans.lower() != Correct_ans.lower():
        print("WWWOORRNNGG ANSWER !!!!!!!!!!!!!!!!!!!!!!!!!!!")
        AnsGiven = 'W'
        return redirect(url_for('home'))  # Reload the page to notify the wrong answer

    # If the answer is correct
    print("CORRECT ANSWER! Moving to the next clue.")
    AnsGiven = 'C'  # Mark the answer as correct



    # Get clues already assigned in this round to other teams
    clues_taken_this_round = [assigned_clues[t][current_round - 1] for t in assigned_clues if len(assigned_clues[t]) >= current_round]
    
    # Get clues already assigned to this team in previous rounds
    clues_taken_by_team = assigned_clues[team_id]

    # Available clues for this team in this round
    available_clues = [i for i in range(len(clue_stack)) if i not in clues_taken_this_round and i not in clues_taken_by_team]

    if available_clues:
        clue_id = random.choice(available_clues)  # Randomly select an available clue
        assigned_clues[team_id].append(clue_id)
        session['clue'] = clue_stack[clue_id]  # Store the clue in session
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