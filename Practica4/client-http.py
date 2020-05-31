import argparse
import http.client
import json

REMOTE_SERVER_HOST = 'localhost'
REMOTE_SERVER_PATH = '/'

conn = http.client.HTTPConnection(REMOTE_SERVER_HOST, 8081)

print("---------------------------------------")

print("1xx Informational")
print("---------------------------------------")
# 100  Continue
print("100")
string = "very large string of characters"
headers = {
    "Content-Type" : "text/plain",
    "Content-Length" : len(string),
    "Expect" : "100-continue",
    "Connection" : "keep-alive"
}
conn.request("PUT", REMOTE_SERVER_PATH + "large-content", body = string, headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print("---------------------------------------")

# 101 Switching protocols
print("101")
headers = {
    "Connection" : "Upgrade",
    "Upgrade" : "HTTP/3.0"
}

conn.request("GET", REMOTE_SERVER_PATH, headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
print("---------------------------------------")

print("2xx Succsessful")
print("---------------------------------------")

# 201 Created
print("201")
string = "Usuario"
conn.request("PUT", REMOTE_SERVER_PATH + "new-user", body = string.encode())
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
data1 = r1.read()  # This will return entire content.
print("Body:", data1.decode())
print("---------------------------------------")

# 202 Accepted
print("202")
string = "Usuario"
conn.request("PUT", REMOTE_SERVER_PATH + "new-request", body = string.encode())
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
data1 = r1.read()  # This will return entire content.
print("---------------------------------------")



# 204 No Content
print("204")
conn.request("DELETE", REMOTE_SERVER_PATH + "user-delete")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
print("---------------------------------------")

# 205 Reset Content
print("205")
body = {
    'name' : 'Dolores',
    'fist-name' : 'Parra',
    'nationality' : 'Mexican'
}
json_body = json.dumps(body).encode()
header = {
    "Content-type" : "application/json",
    "Content-Length" : len(json_body)
}
conn.request("POST", REMOTE_SERVER_PATH + "new-form", json_body, headers = header)
conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)

print("---------------------------------------")

#206 Partial Content
print("206")
header = {
    "Range" : "0-4"
}

conn.request("GET", REMOTE_SERVER_PATH + "sub-string", headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)

print("---------------------------------------")

print("3xx Redirection")
print("---------------------------------------")
# 300 Multiple Choises
print("300")
conn.request("GET", REMOTE_SERVER_PATH + "multiple-path")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body.decode("utf-8"))
print((res.headers.get("Links","").split(",")))
print("---------------------------------------")


# 301 Moved Permanently
print("301")
conn.request("GET", REMOTE_SERVER_PATH + "moved-path")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read().decode("utf-8")
print("Body:", body)
print("Access to:", res.headers.get("Location", "ERROR"))

print("---------------------------------------")


# 302 Found
print("302")
conn.request("GET", REMOTE_SERVER_PATH + "moved-path-tem")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read().decode("utf-8")
print("Body:", body)
print("Access to:", res.headers.get("Location", "ERROR"))
print("---------------------------------------")

#303 See Other
print("303")
body = {
    "user" : "Dolores",
    "psw" : "some-pass"
}
body_json = json.dumps(body).encode()
header = {
    "Content-type" : "application/json",
    "Content-Length" : len(body_json)
}
conn.request("POST", REMOTE_SERVER_PATH + "see-other", body_json, header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("Access to:", res.headers.get("Location", "ERROR"))
print("---------------------------------------")

# 304 Not Modified
print("304")
header = {
    "If-None-Match" : "1234"
}
conn.request("HEAD", REMOTE_SERVER_PATH + "modified-cons", headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
print(res.headers.get("ETag", "Not modified"))
print("---------------------------------------")
print("4xx Client Error")
print("---------------------------------------")

# 400 Bad Request
print("400")
conn.request("POST", REMOTE_SERVER_PATH + "add-image", body)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 401 Unauthorized
print("401")
header = {
    "Authorization" : "Basic 134"
}
conn.request("GET", REMOTE_SERVER_PATH + "authentication", headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 403 Forbidden
print("403")
conn.request("GET", REMOTE_SERVER_PATH + "authentication")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 404 not found
print("404")
conn.request("GET", REMOTE_SERVER_PATH + "unknown")
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 405 Method not Allowed
print("405")
conn.request("TRACE", REMOTE_SERVER_PATH)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 406 Not Acceptable
body = {
    "image" : "image.gif"
}
body_json = json.dumps(body).encode()
header = {
    "Content-type" : "image/gif",
    "Content-Length" : len(body_json)
}
print("406")
conn.request("POST", REMOTE_SERVER_PATH + "add-image", body_json, headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 409 Conflict
body = "new info"
header = {
    "Content-type" : "text/plain",
    "Content-Length" : len(body)
}
print("409")
conn.request("PUT", REMOTE_SERVER_PATH + "unknown-folder", body, headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 410 Gone
body = "adding info into a deleted folder"
header = {
    "Content-type" : "text/plain",
    "Content-Length" : len(body)
}
print("410")
conn.request("PUT", REMOTE_SERVER_PATH + "deleted-folder", body, headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body = res.read()
print("Body:", body)
print("---------------------------------------")

# 411 Length Required
print("411")
string = "very large string of characters"
headers = {
    "Content-Type" : "text/plain",
    "Expect" : "100-continue",
    "Connection" : "keep-alive",
    "Content-Length" : 0
}
conn.request("PUT", REMOTE_SERVER_PATH + "large-content", body = string, headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
body = r1.read()
print("---------------------------------------")

# 413  Request Entity Too Large
print("413")
string = "very laaaaaaaaaaaaaaaaaaaaaaaaarge string of characters"
headers = {
    "Content-Type" : "text/plain",
    "Content-Length" : len(string),
    "Expect" : "100-continue",
    "Connection" : "keep-alive"
}
conn.request("PUT", REMOTE_SERVER_PATH + "large-content", body = string, headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)

while True:
     chunk = r1.read(200)  # 200 bytes
     if not chunk:
          break
     print(chunk)
print("---------------------------------------")

# 414 Request-URI Too Long
print("414")
string = "very large string of characters"
conn.request("PUT", REMOTE_SERVER_PATH + "very-large-uri-to-the-server", body = string)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
body = r1.read()
print("---------------------------------------")

# 415 Unsupported Media Type
print("415")
string = "<p>User:Dolores</p><p>pass:1234</p>"
headers = {
    "Content-Type" : "text/html",
    "Connection" : "keep-alive",
    "Content-Length" : len(string)
}
conn.request("PUT", REMOTE_SERVER_PATH + "add-user", body = string, headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
print("---------------------------------------")

# 416 Partial Content
print("416")
header = {
    "Range" : "20-60"
}

conn.request("GET", REMOTE_SERVER_PATH + "sub-string", headers = header)
res = conn.getresponse()
print("Response:", res.status, res.reason)
print(res.headers)
body_res = res.read()
print("Body:", body_res)
print("---------------------------------------")
print("5xx Server Error")
print("---------------------------------------")
# 501 Not Implemented
print("501")
headers = {
    "Proxy-Authorization": "basic aGVsbG86d29ybGQ="
}
conn.request("CONNECT", REMOTE_SERVER_PATH + "add-user", headers = headers)
r1 = conn.getresponse()
print("\nResponse", r1.status, r1.reason)
print(r1.headers)
body_res = r1.read()
print("Body:", body_res)




