import uuid

class TokenizationService:
    def __init__(self):
        self.token_map = {}

    def tokenize(self, data):
        token = str(uuid.uuid4())
        self.token_map[token] = data
        return token

    def detokenize(self, token):
        return self.token_map.get(token)

if __name__ == "__main__":
    token_service = TokenizationService()
    token = token_service.tokenize("4111111111111111")
    print(f"Token: {token}")
    original_data = token_service.detokenize(token)
    print(f"Original Data: {original_data}")
