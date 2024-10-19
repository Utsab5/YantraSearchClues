from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session management

# Clue stack
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

@app.route('/')
def home():
    clue_id = session.get('clue_id')  # Get the current clue ID from session
    return render_template('home.html', clue_id=clue_id)

@app.route('/get_clue', methods=['POST'])
def get_clue():
    if 'clue_id' not in session:  # Check if the user has not received a clue
        if clue_stack:  # Ensure there are clues available
            clue_id = random.choice(range(len(clue_stack)))  # Randomly select a clue
            session['clue_id'] = clue_id
            session['clue'] = clue_stack[clue_id]  # Store the clue in session
            clue_stack.pop(clue_id)  # Remove the clue from the stack
        else:
            return redirect(url_for('home'))  # No clues left, redirect to home
    return redirect(url_for('home'))

@app.route('/reset', methods=['POST'])
def reset():
    session.pop('clue_id', None)  # Remove the clue ID from session
    session.pop('clue', None)      # Remove the clue from session
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Allow access from any IP
