import requests


url = 'http://localhost:8000/users/create-object/'
file_path = "F:\\university\\C++ abdul bari\\14.pdf"
with open(file_path, 'rb') as f:
    files = {'file': f}
    response = requests.post(url, files=files)

print('Status Code:', response.status_code)
print('Response JSON:', response.json())

# data = {
#     'object_name':'14.pdf',
#     'url_file': 'F:\\university\\C++ abdul bari\\14.pdf',
#     'size': '100',
#     'owner': '2',
#     'accessible_users': ['2']  # توجه کنید که اگر چندین کاربر مجاز باشد، باید از لیست استفاده کنید.
# }
