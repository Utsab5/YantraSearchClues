from flask import Flask, request, render_template_string
from collections import deque

app = Flask(__name__)

# Initialize a stack of clues (added 10 clues)
clues_stack = deque([
    "Clue 1: Search near the big tree.",
    "Clue 2: Look under the bench by the fountain.",
    "Clue 3: Check behind the library's main door.",
    "Clue 4: Find the hidden message on the wall.",
    "Clue 5: Explore the area by the old clock tower.",
    "Clue 6: Look under the third step of the main stairs.",
    "Clue 7: Behind the bulletin board in the main hall.",
    "Clue 8: Near the bike racks at the campus entrance.",
    "Clue 9: Check inside the small garden shed.",
    "Clue 10: Investigate the painting near the cafeteria."
])

# Optional: Track users (example using IP) to ensure they only get one clue
users_received_clue = {}

@app.route('/get-clue', methods=['GET'])
def get_clue():
    # Get the user's IP address
    user_ip = request.remote_addr

    # Check if the user has already received a clue
    if user_ip in users_received_clue:
        previous_clue = users_received_clue[user_ip]
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
                        h1 { color: #ff6347; }
                        p { font-size: 20px; color: #333; }
                        .warning { color: red; font-weight: bold; }
                    </style>
                </head>
                <body>
                    <h1>You have already received a clue!</h1>
                    <p>Your clue was: <b>{{ clue }}</b></p>
                    <p class="warning">Warning: You cannot receive a new clue!</p>
                </body>
            </html>
        ''', clue=previous_clue)
    
    # If clues are still available
    if clues_stack:
        # Pop a clue from the stack and store it for this user
        clue = clues_stack.popleft()
        users_received_clue[user_ip] = clue
        
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
                        h1 { color: #4CAF50; }
                        p { font-size: 20px; color: #333; }
                    </style>
                </head>
                <body>
                    <h1>Your Clue</h1>
                    <p>Your clue is: <b>{{ clue }}</b></p>
                </body>
            </html>
        ''', clue=clue)
    else:
        # If no clues are left
        return render_template_string('''
            <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; background-color: #f4f4f9; text-align: center; padding: 50px; }
                        h1 { color: #ff6347; }
                        p { font-size: 20px; color: #333; }
                    </style>
                </head>
                <body>
                    <h1>No More Clues</h1>
                    <p>Sorry, all clues have been distributed!</p>
                </body>
            </html>
        ''')

# Optional: Endpoint to reset clues for testing or admin purposes
@app.route('/reset-clues', methods=['POST'])
def reset_clues():
    global clues_stack, users_received_clue
    clues_stack = deque([
        "Clue 1: Search near the big tree.",
        "Clue 2: Look under the bench by the fountain.",
        "Clue 3: Check behind the library's main door.",
        "Clue 4: Find the hidden message on the wall.",
        "Clue 5: Explore the area by the old clock tower.",
        "Clue 6: Look under the third step of the main stairs.",
        "Clue 7: Behind the bulletin board in the main hall.",
        "Clue 8: Near the bike racks at the campus entrance.",
        "Clue 9: Check inside the small garden shed.",
        "Clue 10: Investigate the painting near the cafeteria."
    ])
    users_received_clue.clear()
    return "Clues and users have been reset!"

if __name__ == '__main__':
    app.run(debug=True)
