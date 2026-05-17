"""
Test API-AUTH-01: GET /auth/me — Perfil del usuario autenticado
"""
import json
import urllib.request
import urllib.error

BASE = 'http://127.0.0.1:8000'

def request(path, method='GET', data=None, headers=None):
    """Helper para hacer requests HTTP"""
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

print("=" * 60)
print("TEST API-AUTH-01: GET /auth/me — Perfil usuario autenticado")
print("=" * 60)

# Test 1: GET /auth/me sin token
print("\n[Test 1] GET /auth/me sin token (debe fallar con 401)...")
status, data = request('/auth/me', method='GET')
print(f"Status: {status}")
print(f"Respuesta: {json.dumps(data, indent=2)}")

if status != 401:
    print(f"❌ FALLO: Esperaba 401, obtuve {status}")
    exit(1)

print("✅ Sin token retorna 401 Unauthorized")

# Test 2: GET /auth/me con token inválido
print("\n[Test 2] GET /auth/me con token inválido (debe fallar con 401)...")
status, data = request('/auth/me', method='GET', 
                       headers={'Authorization': 'Bearer token_invalido_xyz'})
print(f"Status: {status}")
print(f"Respuesta: {json.dumps(data, indent=2)}")

if status != 401:
    print(f"❌ FALLO: Esperaba 401, obtuve {status}")
    exit(1)

print("✅ Token inválido retorna 401 Unauthorized")

# Test 3: Login para obtener token válido
print("\n[Test 3] Login para obtener token válido...")
status, data = request('/auth/login', method='POST',
                       data={'usuario':'test_admin_api','contrasena':'Test1234'})
print(f"Status: {status}")

if status != 200:
    print(f"❌ FALLO: No se pudo hacer login: {data}")
    exit(1)

token = data.get('access_token')
print(f"✅ Token obtenido: {token[:30]}...")

# Test 4: GET /auth/me con token válido
print("\n[Test 4] GET /auth/me con token válido (debe retornar datos)...")
status, data = request('/auth/me', method='GET',
                       headers={'Authorization': f'Bearer {token}'})
print(f"Status: {status}")
print(f"Respuesta: {json.dumps(data, indent=2)}")

if status != 200:
    print(f"❌ FALLO: Esperaba 200, obtuve {status}")
    exit(1)

# Validar estructura { "data": { ... } }
if 'data' not in data:
    print("❌ FALLO: Respuesta no tiene estructura { 'data': { ... } }")
    exit(1)

me_data = data['data']
print(f"\nDatos del usuario autenticado:")
print(f"  ID: {me_data.get('id_usuario')}")
print(f"  Usuario: {me_data.get('usuario')}")
print(f"  Rol: {me_data.get('rol')}")
print(f"  ID Médico: {me_data.get('id_medico_fk')}")

# Validar campos requeridos
required_fields = {'id_usuario', 'usuario', 'rol'}
missing_fields = required_fields - set(me_data.keys())
if missing_fields:
    print(f"❌ FALLO: Faltan campos: {missing_fields}")
    exit(1)

# Validar valores
if not isinstance(me_data['id_usuario'], int):
    print("❌ FALLO: id_usuario debe ser int")
    exit(1)

if me_data['usuario'] != 'test_admin_api':
    print(f"❌ FALLO: usuario debe ser 'test_admin_api', obtuve '{me_data['usuario']}'")
    exit(1)

if me_data['rol'] != 'Administrativo':
    print(f"❌ FALLO: rol debe ser 'Administrativo', obtuve '{me_data['rol']}'")
    exit(1)

print("\n✅ GET /auth/me retorna estructura correcta con datos del usuario")

# Test 5: Validar que el token contiene el payload correcto
print("\n[Test 5] Verificar que el token contiene el payload de autenticación...")
import base64
parts = token.split('.')
if len(parts) != 3:
    print("⚠️  Token no es un JWT válido (no tiene 3 partes)")
else:
    # Agregar padding si es necesario
    payload_part = parts[1]
    padding = 4 - len(payload_part) % 4
    if padding != 4:
        payload_part += '=' * padding
    
    try:
        payload_decoded = base64.urlsafe_b64decode(payload_part)
        payload_json = json.loads(payload_decoded)
        print(f"Payload del JWT: {json.dumps(payload_json, indent=2)}")
        
        # Verificar que contiene los campos esperados
        if 'id_usuario' in payload_json and 'usuario' in payload_json and 'rol' in payload_json:
            print("✅ JWT contiene campos requeridos para /auth/me")
        else:
            print("⚠️  JWT no contiene todos los campos esperados")
    except Exception as e:
        print(f"⚠️  No se pudo decodificar payload: {e}")

print("\n" + "=" * 60)
print("✅ TODOS LOS TESTS DE API-AUTH-01 COMPLETADOS")
print("=" * 60)
