from flask import Flask, render_template, jsonify, request
import json
from routes.projects import projects
from routes.recommendations import recommend
from routes.events import events
from routes.skills import skills
from routes.certifications import certifications


app = Flask(__name__)

projects_file = "templates/json/cards_data.json"
recommendations_file = "templates/json/recommendations.json"
skills_file = "templates/json/skills.json"


def load_json(file): 
    with open(file, "r") as f: return json.load(f)

@app.route('/')
def index():
    return render_template(
        'index.html',
        projects=load_json(projects_file),
        recommendations=load_json(recommendations_file),
        skills_data=load_json(skills_file),
        certifications=load_json("templates/json/certifications.json")  # ⬅️ Add this
    )


@app.route('/filter_projects', methods=['POST'])
def filter_projects():
    category = request.json['category']
    projects_data = load_json(projects_file)
    filtered = [p for p in projects_data if category in p['labels']]
    return jsonify(filtered)

# Register blueprints
app.register_blueprint(projects)
app.register_blueprint(recommend)
app.register_blueprint(events)
app.register_blueprint(skills)
app.register_blueprint(certifications)

if __name__ == '__main__':
    app.run(debug=True)
