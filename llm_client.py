import openai
import toml

class LLMClient:
    def __init__(self, config_path="config.toml"):
        config = toml.load(config_path)["llm"]

        self.model = config.get("model")
        self.max_tokens = config.get("max_tokens", 2048)
        self.temperature = config.get("temperature", 0.7)

        openai.api_base = config.get("base_url")
        openai.api_key = config.get("api_key")
        if config.get("api_type"):
            openai.api_type = config.get("api_type")
        if config.get("api_version"):
            openai.api_version = config.get("api_version")

    def chat(self, system_prompt, user_prompt):
        response = openai.ChatCompletion.create(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        return response.choices[0].message.content.strip()
