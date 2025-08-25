from flask import Flask, request, jsonify, render_template
from crew import AgentsCrew 
import os
import threading
import uuid 

app = Flask(__name__)
app.secret_key = os.urandom(24)

task_results = {}

def run_crew_task(task_id, inputs):
    print(f"Iniciando tarefa do Crew (ID: {task_id}) com os inputs: {inputs}")
    
    try:
        my_crew = AgentsCrew()
        result = my_crew.kickoff(inputs=inputs)
        task_results[task_id] = {"status": "completed", "result": result}
        print(f"Tarefa (ID: {task_id}) finalizada com sucesso.")
    except Exception as e:
        print(f"Erro ao executar a tarefa (ID: {task_id}): {e}")
        task_results[task_id] = {"status": "error", "message": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_crew', methods=['POST'])
def run_career_crew():
    data = request.get_json()
    new_topic = data.get('topic')

    if not new_topic:
        return jsonify({"error": "O tópico é obrigatório"}), 400

    task_id = str(uuid.uuid4())
    task_results[task_id] = {"status": "pending"} 

    inputs = {'topic': new_topic}

    thread = threading.Thread(target=run_crew_task, args=(task_id, inputs))
    thread.start()

    return jsonify({
        "message": "Sua solicitação foi recebida! Nila já está trabalhando na sua resposta.",
        "task_id": task_id
    }), 202 

@app.route('/get_result/<task_id>', methods=['GET'])
def get_result(task_id):
    result = task_results.get(task_id, {"status": "not_found"})
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)