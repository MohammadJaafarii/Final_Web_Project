import requests

url = 'http://localhost:8000/users/create-object/'
files = {
    'icon': open('C:\\Users\\ok\\PycharmProjects\\final web\\Final_Web_Project\\FileStorage\\FileStorage\\img\\PDF.png', 'rb')
}
data = {
    'object_name':'14.pdf',
    'url_file': 'F:\\university\\C++ abdul bari\\14.pdf',
    'size': '100',
    'owner': '1',
    'accessible_users': ['1']  # توجه کنید که اگر چندین کاربر مجاز باشد، باید از لیست استفاده کنید.
}

response = requests.post(url, files=files, data=data)
print(response.json())
