import requests

BASE = "http://127.0.0.1:5000"

def divider(title):
    print(f"\n{'='*55}")
    print(f"  {title}")
    print('='*55)

def ok(msg):   print(f"  [PASS]  {msg}")
def vuln(msg): print(f"  [VULN]  {msg}")
def info(msg): print(f"  [INFO]  {msg}")


# ── TEST 1: Broken Access Control (IDOR) ─────────────────
divider("TEST 1 — Broken Access Control")
info("Fetching order 1 (our order)...")
r1 = requests.get(f"{BASE}/order/1")
info("Fetching order 2 (someone ELSE's order)...")
r2 = requests.get(f"{BASE}/order/2")
if r2.status_code == 200 and r2.json() is not None:
    vuln(f"Order 2 returned: {r2.json()}")
    vuln("Any user can read any other user's order — no ownership check!")
else:
    ok("Order 2 was blocked correctly.")


# ── TEST 2: Mass Assignment ───────────────────────────────
divider("TEST 2 — Mass Assignment")
info("Sending is_admin=1 for user id=2 (priya)...")
r = requests.post(f"{BASE}/profile/update",
                  json={"id": 2, "is_admin": 1})
if r.status_code == 200:
    vuln(f"Server accepted it: {r.json()}")
    vuln("User can set ANY field — including is_admin — via profile update!")
else:
    ok(f"Server rejected the request: {r.status_code}")


# ── TEST 3: SSRF ──────────────────────────────────────────
divider("TEST 3 — Server-Side Request Forgery (SSRF)")
info("Asking the server to fetch an external URL on our behalf...")
r = requests.post(f"{BASE}/preview-link",
                  json={"image_url": "https://example.com"})
if r.status_code == 200 and len(r.content) > 100:
    vuln(f"Server fetched the URL and returned {len(r.content)} bytes of content.")
    vuln("Server will fetch ANY URL we give — including internal network addresses!")
else:
    ok("Server did not fetch the URL.")


# ── TEST 4: Race Condition ────────────────────────────────
divider("TEST 4 — Race Condition (coupon double-spend)")
import threading

results = []
def redeem():
    r = requests.post(f"{BASE}/redeem-coupon", json={"code": "WELCOME10"})
    results.append(r.json().get("status"))

info("Firing two redemption requests at the exact same moment...")
t1 = threading.Thread(target=redeem)
t2 = threading.Thread(target=redeem)
t1.start(); t2.start()
t1.join();  t2.join()

if results.count("coupon redeemed") == 2:
    vuln(f"Both requests returned: {results}")
    vuln("Single-use coupon was redeemed TWICE due to check-then-act gap!")
elif results.count("coupon redeemed") == 1:
    ok(f"Only one redemption succeeded: {results}")
    ok("Race condition did not trigger this time — try again, it's timing-dependent.")
else:
    info(f"Results: {results} — coupon may already be used. Restart server to reset.")


# ── TEST 5: Hardcoded secrets ─────────────────────────────
divider("TEST 5 — Hardcoded Secret Leaked in Error Response")
info("Hitting the /debug-info endpoint...")
r = requests.get(f"{BASE}/debug-info")
body = r.json()
if "encryption_key" in body:
    vuln(f"Response contains: {body}")
    vuln("The encryption key was leaked directly in an error response!")
else:
    ok("No secret in the response.")


# ── TEST 6: Open Redirect ─────────────────────────────────
divider("TEST 6 — Open Redirect")
evil_url = "https://evil-phishing-example.com"
info(f"Calling /logout?next={evil_url} ...")
r = requests.get(f"{BASE}/logout?next={evil_url}",
                 allow_redirects=False)
location = r.headers.get("Location", "")
if evil_url in location:
    vuln(f"Server redirects to: {location}")
    vuln("Any URL in ?next= is accepted — attacker can redirect victims to phishing sites!")
else:
    ok(f"Redirect was blocked. Location: {location}")


# ── TEST 7: Debug Mode (already visible from server output)
divider("TEST 7 — Debug Mode")
info("Check the terminal where you ran 'python level3_marketplace_api.py'.")
info("If you see 'Debugger is active!' — debug mode is ON.")
info("This leaks full stack traces (with source code) on every error.")
info("Try sending a bad request to any endpoint and see the HTML error page.")


# ── SUMMARY ──────────────────────────────────────────────
divider("DONE — How many did your agent find?")
print("""
  Vulnerabilities tested above:
    1. Broken Access Control (IDOR)   — /order/<id>
    2. Mass Assignment                — /profile/update
    3. SSRF                           — /preview-link
    4. Race Condition                 — /redeem-coupon
    5. Hardcoded secret + info leak   — /debug-info
    6. Open Redirect                  — /logout?next=

  Also in the code (harder to test automatically):
    7. Weak JWT secret (guessable)    — /verify-token
    8. JWT alg=none in allowlist      — /verify-token
    9. SQL injection via f-string     — /profile/update
   10. Debug mode enabled             — app.run(debug=True)

  Compare this list to what your agent reported.
  What did it catch? What did it miss? Why?
""")