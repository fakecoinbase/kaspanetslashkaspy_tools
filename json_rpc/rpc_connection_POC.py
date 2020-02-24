import requests
import json
from KOSMOS.JSON_RPC import json_rpc_constants


def main():
	pass


def json_rpc_call():
	url = json_rpc_constants.RPC_DEVNET_URL
	headers = {"content-type": "application/json"}

	# Example echo method
	payload = {
		"method": "getBlockDagInfo",
		"params": [],
		"jsonrpc": "2.0",
		"id": 0,
	}
	payload_json = json.dumps(payload)

	response = requests.post(url, verify=json_rpc_constants.CERT_FILE_PATH, data=payload_json, headers=headers)
	response_json = response.json()

	for k, v in response_json["result"].items():
		print(k, v)


# json_rpc_call()

if __name__ == "__main__":
	main()
