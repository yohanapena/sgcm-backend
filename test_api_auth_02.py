"""
Test API-AUTH-02: GET /auth/usuarios/{id} — Obtener usuario por ID
"""
import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:8000'


def request(path, method='GET', data=None, headers=None):
    url = BASE + path
    data_bytes = None
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
    hdrs = {'Content-Type': 'application/json'}
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data_bytes, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read().decode('utf-8')
            return res.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        try:
            payload = json.loads(body)
        except Exception:
            payload = body
        return e.code, payload


print("TEST API-AUTH-02: GET /auth/usuarios/{id}")

# Login to obtain token
status, data = request('/auth/login', method='POST', data={'usuario':'test_admin_api','contrasena':'Test1234'})
print('Login status:', status)
if status != 200:
    print('❌ Cannot obtain token:', data)
    raise SystemExit(1)

token = data.get('access_token')
print('Token obtained')

# Get list of users to find test_admin_api id
status, data = request('/auth/usuarios', method='GET', headers={'Authorization': f'Bearer {token}'})
print('List users status:', status)
if status != 200:
    print('❌ Cannot list users:', data)
    raise SystemExit(1)

users = data
user_id = None
for u in users:
    if u.get('usuario') == 'test_admin_api':
        user_id = u.get('id_usuario')
        break

if not user_id:
    print('❌ test_admin_api not found in users list')
    raise SystemExit(1)

print('Found test_admin_api id =', user_id)

# Test: GET existing user
print('\n[Test] GET existing user')
status, data = request(f'/auth/usuarios/{user_id}', method='GET', headers={'Authorization': f'Bearer {token}'})
print('Status:', status)
print('Response:', json.dumps(data, indent=2))
if status != 200:
    print('❌ Expected 200 for existing user')
    raise SystemExit(1)

# Validate response structure { data: UsuarioResponse }
if 'data' not in data:
    print('❌ Response missing data wrapper')
    raise SystemExit(1)

me = data['data']
required = {'id_usuario','usuario','rol','estado'}
miss = required - set(me.keys())
if miss:
    print('❌ Missing fields in response:', miss)
    raise SystemExit(1)

print('✅ Existing user returned with required fields')

# Test: GET nonexistent user (use a high id unlikely to exist)
non_id = 999999
print('\n[Test] GET nonexistent user id', non_id)
status, data = request(f'/auth/usuarios/{non_id}', method='GET', headers={'Authorization': f'Bearer {token}'})
print('Status:', status)
print('Response:', json.dumps(data, indent=2))
if status != 404:
    print('❌ Expected 404 for nonexistent user')
    raise SystemExit(1)

print('✅ Nonexistent user returns 404')

print('\nALL API-AUTH-02 TESTS PASSED')
