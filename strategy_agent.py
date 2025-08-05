import json

class StrategyIntentAgent:
    def __init__(self):
        self.data = {
            "version_description": None,
            "strategy_approach": {
                "strategy_entry": None,
                "model_entry": None,
                "risk_segment": None,
                "search_abort_reasons": []
            },
            "expectation_goal": None,
            "constraint_condition": [],
            "target_sql": None
        }

    def is_complete(self):
        return all([
            self.data["version_description"],
            self.data["strategy_approach"]["strategy_entry"],
            self.data["strategy_approach"]["model_entry"],
            self.data["strategy_approach"]["risk_segment"],
            self.data["strategy_approach"]["search_abort_reasons"],
            self.data["expectation_goal"],
            self.data["constraint_condition"],
            self.data["target_sql"]
        ])

    def prompt_next(self):
        if not self.data["version_description"]:
            return "请提供版本说明。"
        if not self.data["strategy_approach"]["strategy_entry"]:
            return "策略是否准入？（策略准入 / 策略不准入）"
        if not self.data["strategy_approach"]["model_entry"]:
            return "模型是否准入？（模型准入 / 模型不准入）"
        if not self.data["strategy_approach"]["risk_segment"]:
            return "请选择风险分层（R1, R2, R3, R4, nan）"
        if not self.data["strategy_approach"]["search_abort_reasons"]:
            return "请选择搜索中止原因（可多选）"
        if not self.data["expectation_goal"]:
            return "请输入你的预期目标，例如“M4余额增长最大化”。"
        if not self.data["constraint_condition"]:
            return "请输入至少一个约束条件。"
        if not self.data["target_sql"]:
            return "请输入目标客群的SQL。"
        return "输入已完整。"

    def add_constraint(self, metric, operator, threshold):
        self.data["constraint_condition"].append({
            "metric": metric,
            "operator": operator,
            "threshold": threshold
        })

    def generate_json(self):
        return self.data

    def suggest_strategy(self):
        goal = self.data["expectation_goal"]
        if "增长" in goal:
            return "建议：对 A 类人群提升额度 10%。"
        return "建议：请根据策略目标人工审核。"



# strategy_agent.py
from llm_client import LLMClient
from prompt import system_prompt
from strategy_agent import StrategyIntentAgent

client = LLMClient()  # 从 config.toml 读取配置
agent = StrategyIntentAgent()

while not agent.is_complete():
    prompt = agent.prompt_next()
    response = client.chat(system_prompt + "\n" + prompt)
    # 处理用户回复并填入 agent.data 相应字段

# 输出最终配置和策略建议
print(agent.generate_json())
print(agent.suggest_strategy())

# strategy_agent.py
from llm_client import LLMClient
from prompt import system_prompt

def main():
    client = LLMClient()
    agent = StrategyIntentAgent()

    print("🚀 欢迎使用智能策略配置助手")
    print("💬 当前提示词：", system_prompt)

    while not agent.is_complete():
        prompt = agent.prompt_next()
        print("🤖 需要信息：", prompt)

        # 构造 LLM 交互
        user_input = input("用户输入 >>> ")  # 或替换为 LLM 自动生成
        # 示例：简化处理逻辑，只模拟填入字段
        if "版本说明" in prompt:
            agent.data["version_description"] = user_input
        elif "策略是否准入" in prompt:
            agent.data["strategy_approach"]["strategy_entry"] = user_input
        elif "模型是否准入" in prompt:
            agent.data["strategy_approach"]["model_entry"] = user_input
        elif "风险分层" in prompt:
            agent.data["strategy_approach"]["risk_segment"] = user_input
        elif "中止原因" in prompt:
            agent.data["strategy_approach"]["search_abort_reasons"] = user_input.split(",")
        elif "预期目标" in prompt:
            agent.data["expectation_goal"] = user_input
        elif "约束条件" in prompt:
            metric, operator, value = user_input.split()
            agent.add_constraint(metric, operator, value)
        elif "SQL" in prompt:
            agent.data["target_sql"] = user_input

    print("\n✅ 完整策略配置 JSON：")
    print(agent.generate_json())

    print("\n💡 策略建议：")
    print(agent.suggest_strategy())

if __name__ == "__main__":
    main()
