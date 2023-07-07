import json
import os
from flask import Flask, render_template, request, redirect, session
from survivor import Survivor
from data_handler import all_survivors, add_new_survivor

app = Flask(__name__)
app.secret_key = 'secret_key_placeholder'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    # Retrieve MCQ answers data
    answers = []
    for i in range(len(questions)):
        if i == 2:  # Question with a single answer
            answer = int(request.form.get('answer' + str(i + 1)))
            answers.append(answer)
        else:  # Questions with multiple answers
            answer_options = request.form.getlist('answer' + str(i + 1))
            answer_values = [int(option) for option in answer_options]
            answers.append(answer_values)
    
    # Retrieve action items data
    action_items_data = request.form.get('actionItemsData').strip().split('\n')
    action_items = {}
    current_stakeholder = None
    for line in action_items_data:
        current_stakeholder = line.split(':')[0].strip()
        current_action = line.split(':')[1].strip()
        if current_stakeholder not in action_items:
            action_items[current_stakeholder] = [current_action]
        else:
            action_items[current_stakeholder].append(current_action)
    
    # Retrieve important questions data
    important_questions = []
    for option in request.form.getlist('importantQuestions'):
        important_questions.append(int(option[len('option'):]))
        
    # Retrieve harm case description, feelings, impact
    description = request.form.get('description')
    feelings = request.form.get('feelings')
    impact = request.form.get('impact')
    
    # Create a new survivor with the collected data
    new_survivor = Survivor(answers, action_items, important_questions, description, feelings, impact)
    
    # Find recommended action items and divide into same stakeholder and different stakeholder
    rec_items_from_same_stakeholder, rec_items_from_different_stakeholder = new_survivor.divide_recommended_action_items(all_survivors)

    rec_items = new_survivor.get_recommended_action_items(all_survivors)
    
    # Store the recommended action items in the session
    session['recommended_items'] = {
        'from_same_stakeholder': rec_items,
        'from_different_stakeholder': rec_items_from_different_stakeholder
    }

    # Save the new survivor's data to the system
    add_new_survivor(new_survivor)
    
    return redirect('/recommendations')

@app.route('/recommendations')
def show_recommendations():
    # Retrieve the recommended action items from the session
    recommended_items = session['recommended_items']
    
    # Get the new survivor's action plan, assuming the new survivor is the last one in the list
    new_survivor = all_survivors[-1]
    
    return render_template('recommendations.html', recommended_items=recommended_items, new_survivor=new_survivor)

@app.route('/update_action_plan', methods=['POST'])
def update_action_plan():
    updated_action_plan = request.json.get('action_plan')
    new_survivor = all_survivors[-1]
    new_survivor.update_action_plan(updated_action_plan)
    
    with open('survivors_data.json', 'w') as f:
        json.dump([s.__dict__ for s in all_survivors], f, indent=4)
    return 'Action plan updated successfully!'

@app.route('/action_plan')
def show_action_plan():
    # Get the new survivor's action plan
    new_survivor = all_survivors[-1]

    return render_template('action_plan.html', new_survivor=new_survivor)

# Define the questions list
questions = [
    {
        'question': 'Please select all the options below that best describe the type(s) of harm you experienced:',
        'options': ['Offensive name-calling', 'Purposeful embarrassment', 'Stalking', 'Physical threats', 'Harassment over a sustained period of time', 'Sexual harassment']
    },
    {
        'question': 'Please select all the options below that apply to where the harm occurred:',
        'options': ['In person', 'In private online chat', 'In public online chat']
    },
    {
        'question': 'Please select the option below that best reflects the number of individuals you believe have caused harm to you:',
        'options': ['One', 'Multiple']
    },
    {
        'question': 'Please select all the options below that apply to your relationship with the individuals who caused the harm:',
        'options': ['Strangers', 'Friends', 'Acquaintances']
    },
]

if __name__ == '__main__':
    app.run(port=8080)
