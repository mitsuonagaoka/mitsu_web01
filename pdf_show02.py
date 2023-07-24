import base64

# 文字列をバイト列にエンコードしてBase64エンコード
data = "Hello, world!"
encoded_data = base64.b64encode(data.encode("utf-8")).decode("utf-8")

# Base64エンコードされたデータをデコード
decoded_data = base64.b64decode(encoded_data).decode("utf-8")

print("Encoded:", encoded_data)
print("Decoded:", decoded_data)
