from django.test import Client
c = Client()
print('Sending GET /course/add/')
r = c.get('/course/add/', HTTP_HOST='127.0.0.1')
print('GET status:', r.status_code)
print('Sending POST /course/add/')
r2 = c.post('/course/add/', {'name': 'UIT Test', 'code': 'UIT101'}, follow=True, HTTP_HOST='127.0.0.1')
print('POST status:', r2.status_code)
print('Redirect chain:', r2.redirect_chain)
# print a snippet of the response body to help debug
try:
    text = r2.content.decode('utf-8')
except Exception:
    text = str(r2.content)
print('Response snippet:\n', text[:1000])
