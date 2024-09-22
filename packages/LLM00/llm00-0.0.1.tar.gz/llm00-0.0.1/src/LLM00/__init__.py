
# シンプルなLLMインターフェース [LLM00]

import os
import sys
import json
import fies
import requests
from sout import sout

# OpenAIのAPIキー格納候補
api_keyfile_cand_ls = [
	"C:/develop/keys/OpenAI_API_key_for_LLM00.txt",
]

# OpenAIのAPIキー取得
def get_api_key():
	for filepath in api_keyfile_cand_ls:
		if os.path.exists(filepath):
			return fies[filepath, "text"]
	raise Exception("[LLM00 error] The API key file is missing (not found in any of the specified locations).")

# OpenAIのLLMを呼び出し
def call_openAI_api(query):
	# ヘッダの指定
	headers = {
		"Authorization": "Bearer %s"%get_api_key(),	# OpenAIのAPIキー取得
		"Content-Type": "application/json",
	}
	# request bodyの指定
	req_body = json.dumps({
		"model": "gpt-4o",
		"messages": [{"role": "user", "content": query}]
	})
	# 呼び出し
	raw_resp = requests.post("https://api.openai.com/v1/chat/completions", data = req_body, headers = headers)
	# レスポンスから必要部分を取り出して返す
	resp = raw_resp.json()
	# エラーの確認
	if "choices" not in resp: raise Exception("[LLM00 error] An API error has occurred.")
	# AIのレスポンステキストを取り出す
	resp_text = resp["choices"][0]["message"]["content"]
	return resp_text

# ツールの中核をなすクラス
class LLM00_Class:
	# 初期化処理
	def __init__(self):
		pass
	# 簡易呼び出し
	def __call__(self,
		query,	# AIへの問いかけ
	):
		# 型チェック
		if type(query) != type(""): raise Exception("[LLM00 error] The query type is invalid. Only string types are allowed in the current version.")
		# OpenAIのLLMを呼び出し
		resp =  call_openAI_api(query)
		# AIからの返答を返す
		return resp

# モジュールオブジェクトと「LLM00クラスのオブジェクト」を同一視
sys.modules[__name__] = LLM00_Class()
