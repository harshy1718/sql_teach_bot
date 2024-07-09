import os
from flask import Flask, request, render_template, jsonify, redirect, url_for
import openai

# Set the absolute path to the templates folder
template_dir = os.path.abspath('./templates')
app = Flask(__name__, template_folder=template_dir)

OPENAI_API_KEY = 'add-your-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/questionnaire')
def questionnaire():
    # Display the questionnaire form
    return render_template('questionnaire.html')

@app.route('/ask', methods=['POST'])
def ask():
    profession = request.form['profession']
    experience_level = request.form['experience_level']
    other_knowledge = request.form['other_knowledge']
    goal = request.form['goal']
    specifications = request.form['specifications']
    application = request.form['application']
    time_commitment = request.form['time_commitment']
    plan_duration = request.form['plan_duration']

    # Redirect to the plan page with all the parameters
    return redirect(url_for('plan',
                            profession=profession,
                            experience_level=experience_level,
                            other_knowledge=other_knowledge,
                            goal=goal,
                            specifications=specifications,
                            application=application,
                            time_commitment=time_commitment,
                            plan_duration=plan_duration))

@app.route('/plan', methods=['GET'])
def plan():
    # Retrieve the data passed to this route
    profession = request.args.get('profession')
    experience_level = request.args.get('experience_level')
    other_knowledge = request.args.get('other_knowledge')
    goal = request.args.get('goal')
    specifications = request.args.get('specifications')
    application = request.args.get('application')
    time_commitment = request.args.get('time_commitment')
    plan_duration = request.args.get('plan_duration')

    # Construct the prompt for the OpenAI API
    prompt = f"""Hi, I am a {profession} and want to create a study plan for learning SQL. 
    My experience level is {experience_level} and I have {other_knowledge} prior knowledge.
    My goal is {goal}. I am interested in the {specifications} feature of SQL specifically.
    I want to apply it in {application} domain and can devote {time_commitment} each week. 
    Please create an elaborate study plan for {plan_duration} weeks."""

    # Extract the text from the response
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    openai.api_key = OPENAI_API_KEY
    gpt_assistant_prompt = "You are a teacher and very good at teaching basics of SQL"
    message = [{"role": "assistant",
                "content": gpt_assistant_prompt
                },
               {"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model="gpt-4",
        messages=message
    )
    chat_response = response.choices[0].message.content
    return render_template('plan.html', answer=chat_response)

if __name__ == '__main__':
    app.run(debug=True)
