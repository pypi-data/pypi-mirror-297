
# SLLM 構築中 (under construction...)

import openai

class SLLM:
	def __init__(self, model="gpt-3.5-turbo"):
		# モデル名やAPIキーをセットアップ
		self.model = model
		self.api_key = "your_openai_api_key"  # 必要に応じてAPIキーを設定
		openai.api_key = self.api_key

	def __call__(self, prompt):
		# LLMへの問いかけを行うメソッド
		response = openai.ChatCompletion.create(
			model=self.model,
			messages=[
				{"role": "system", "content": "You are a helpful assistant."},
				{"role": "user", "content": prompt}
			]
		)
		return response.choices[0].message['content']

# SLLMのインスタンスを作成して利用
if __name__ == "__main__":
	llm = SLLM()

	# 質問例
	question = "ずばり簡潔に、タコの足は何本？"
	answer = llm(question)
	print(answer)
