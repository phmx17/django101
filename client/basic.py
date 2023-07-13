import requests

endpoint = 'http://127.0.0.1:8000/books/api'

# response = requests.get(endpoint)
# books = response.json()
# for idx, book in enumerate(books['books'], start=1):
#     print(f"title {idx}: {book['title']} ")

response = requests.post(endpoint, json={'title': 'Bourne Identity'})
# the server returns the payload by default
print(response.json())
