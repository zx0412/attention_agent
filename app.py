from flask import Flask, request, jsonify
from strategy_agent import StrategyIntentAgent

app = Flask(__name__)
agent = StrategyIntentAgent()

@app.route("/input", methods=["POST"])
def input_handler():
    data = request.json
    for k, v in data.items():
        if k in agent.data:
            agent.data[k] = v
        elif k in agent.data["strategy_approach"]:
            agent.data["strategy_approach"][k] = v
    return jsonify({"next_prompt": agent.prompt_next()})

@app.route("/submit_constraint", methods=["POST"])
def submit_constraint():
    body = request.json
    agent.add_constraint(body["metric"], body["operator"], body["threshold"])
    return jsonify({"next_prompt": agent.prompt_next()})

@app.route("/generate", methods=["GET"])
def generate():
    if agent.is_complete():
        return jsonify({
            "json_config": agent.generate_json(),
            "strategy_suggestion": agent.suggest_strategy()
        })
    else:
        return jsonify({
            "error": "信息不完整",
            "next_prompt": agent.prompt_next()
        }), 400

if __name__ == "__main__":
    app.run(port=8888)
