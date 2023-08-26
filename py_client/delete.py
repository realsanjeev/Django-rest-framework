import requests

book_id = input("Enter id of book needed to delete: ")

try:
    book_id = int(book_id)
except:
    print(f"Book id {book_id} id not valid")
    book_id = None


endpoint = f"http://localhost:8000/v1/api/{book_id}/delete/"
try:
    get_response = requests.delete(endpoint)
    print(get_response.content)
    print(get_response.status_code)
except:
    print("Error while communication with endpoint")
