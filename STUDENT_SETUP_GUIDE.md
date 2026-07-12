Setup Guide — Vulnerability Discovery Exercise

This guide tells you exactly how to run each codebase and how to verify
your fixes. Always run the code first, note the baseline output, then
hunt for vulnerabilities. After fixing, run again to confirm you did not
break normal behaviour.


Level 1 — level1_student_portal.py

Requirements: nothing to install — pure Python standard library.

Run:

python level1_student_portal.py

Expected baseline output (write this down before changing anything):

Student Grade Portal — sample students: Aarav, Priya, Rohan

Enter student name: Aarav
Grade: (88,)

After applying every fix, typing "Aarav" should still return Grade: (88,).
If it crashes or returns nothing, your fix broke something — review it.


Level 2 — level2_file_vault.py

Requirements: nothing to install — pure Python standard library.

Run:

python level2_file_vault.py

This runs a demo automatically — no input needed.

Expected baseline output (write this down before changing anything):

Campus File Vault

Login with correct password: True
Downloaded file contents: Sample report card contents.
Vault Alert: demo_student downloaded report_card.txt
Restored session: {'username': 'demo_student', 'logged_in': True}

All four lines must still appear after your fixes. If any line changes or
disappears, a fix was too aggressive.

Tip: to reset demo data, delete vault.db and the vault_files/
folder, then run again.


Level 3 — level3_marketplace_api.py

This is a web server — it stays running while you test it.
You need two terminals open at the same time.

Install dependencies (once only)

pip install flask pyjwt requests

Terminal 1 — start the server (keep this open)

python level3_marketplace_api.py

You should see:

* Running on http://127.0.0.1:5000

Leave this terminal open. Press Ctrl+C here to stop the server.

Terminal 2 — run your tests here


Testing Level 3: two approaches

Approach A — test_level3.py (recommended, works on all systems)

This is the easiest method. It tests all major vulnerabilities automatically
and tells you clearly what is broken and what is fixed.

Run:

python test_level3.py

Understanding the output:

SymbolMeaning[VULN]Vulnerability confirmed present — needs fixing[PASS]Vulnerability not detected — either already fixed or not present[INFO]Informational — check manually (see note in output)

Example output before any fixes:

=======================================================
  TEST 1 — Broken Access Control
=======================================================
  [INFO]  Fetching order 1 (our order)...
  [INFO]  Fetching order 2 (someone ELSE's order)...
  [VULN]  Order 2 returned: [2, 2, 'Chemistry Textbook', 380.0]
  [VULN]  Any user can read any other user's order — no ownership check!

The fix-and-verify cycle:

Step 1 → Run test_level3.py → note which tests show [VULN]
Step 2 → Apply fix to that line of code (based on your agent's suggestion)
Step 3 → Run test_level3.py again → [VULN] should become [PASS]
Step 4 → Run the server and confirm it still starts without errors

Important: A [PASS] means the test did not detect the vulnerability.
It does not guarantee the code is perfectly secure. Think of it as a
minimum bar, not a perfect score.

Resetting between tests: Some tests modify the database (e.g. mass
assignment changes is_admin, coupon redemption marks a coupon used).
To reset to a clean state, stop the server, delete marketplace.db,
and start the server again — it recreates fresh sample data automatically.


Approach B — manual commands (if you prefer not to use the test script)

Choose the section for your operating system.


Mac / Linux (Terminal — bash or zsh)

bash# ── TEST 1: IDOR — can you read someone else's order? ─────────────
curl http://127.0.0.1:5000/order/1
curl http://127.0.0.1:5000/order/2
# If you see order 2's data without any login, IDOR is present.

# ── TEST 2: Mass Assignment — can you set is_admin yourself? ───────
curl -X POST http://127.0.0.1:5000/profile/update \
  -H "Content-Type: application/json" \
  -d '{"id":2,"is_admin":1}'
# If it returns {"status":"updated"}, mass assignment is present.

# ── TEST 3: SSRF — can you make the server fetch any URL? ──────────
curl -X POST http://127.0.0.1:5000/preview-link \
  -H "Content-Type: application/json" \
  -d '{"image_url":"https://example.com"}'
# If you get HTML back, the server fetched the URL — SSRF is present.

# ── TEST 4: Race Condition — run both lines at the same time ───────
curl -X POST http://127.0.0.1:5000/redeem-coupon \
  -H "Content-Type: application/json" \
  -d '{"code":"WELCOME10"}' &
curl -X POST http://127.0.0.1:5000/redeem-coupon \
  -H "Content-Type: application/json" \
  -d '{"code":"WELCOME10"}' &
# If BOTH return {"status":"coupon redeemed"}, race condition is present.
# (Restart server and delete marketplace.db to reset the coupon.)

# ── TEST 5: Info leak — does the error response expose secrets? ─────
curl http://127.0.0.1:5000/debug-info
# If you see "encryption_key" in the response, info leak is present.

# ── TEST 6: Open Redirect — does ?next= accept any URL? ────────────
curl -i "http://127.0.0.1:5000/logout?next=https://evil-example.com"
# Look at the "Location:" header in the response.
# If it shows https://evil-example.com, open redirect is present.


Windows — PowerShell (Invoke-WebRequest)

powershell# ── TEST 1: IDOR ────────────────────────────────────────────────────
Invoke-WebRequest -Uri "http://127.0.0.1:5000/order/1" | Select-Object -Expand Content
Invoke-WebRequest -Uri "http://127.0.0.1:5000/order/2" | Select-Object -Expand Content

# ── TEST 2: Mass Assignment ─────────────────────────────────────────
Invoke-WebRequest -Uri "http://127.0.0.1:5000/profile/update" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"id":2,"is_admin":1}' | Select-Object -Expand Content

# ── TEST 3: SSRF ────────────────────────────────────────────────────
Invoke-WebRequest -Uri "http://127.0.0.1:5000/preview-link" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"image_url":"https://example.com"}' | Select-Object -Expand Content

# ── TEST 4: Race Condition (PowerShell parallel jobs) ───────────────
$job1 = Start-Job { Invoke-WebRequest -Uri "http://127.0.0.1:5000/redeem-coupon" -Method POST -ContentType "application/json" -Body '{"code":"WELCOME10"}' | Select-Object -Expand Content }
$job2 = Start-Job { Invoke-WebRequest -Uri "http://127.0.0.1:5000/redeem-coupon" -Method POST -ContentType "application/json" -Body '{"code":"WELCOME10"}' | Select-Object -Expand Content }
Receive-Job $job1 -Wait; Receive-Job $job2 -Wait

# ── TEST 5: Info Leak ───────────────────────────────────────────────
Invoke-WebRequest -Uri "http://127.0.0.1:5000/debug-info" | Select-Object -Expand Content

# ── TEST 6: Open Redirect (check Location header) ───────────────────
$r = Invoke-WebRequest -Uri "http://127.0.0.1:5000/logout?next=https://evil-example.com" `
  -MaximumRedirection 0 -ErrorAction SilentlyContinue
$r.Headers["Location"]


Windows — curl.exe (Command Prompt or Git Bash)


Use curl.exe (not just curl) — in PowerShell, curl is an alias for
Invoke-WebRequest, which is different. curl.exe calls the real curl.



bat:: TEST 1: IDOR
curl.exe http://127.0.0.1:5000/order/1
curl.exe http://127.0.0.1:5000/order/2

:: TEST 2: Mass Assignment
curl.exe -X POST http://127.0.0.1:5000/profile/update -H "Content-Type: application/json" -d "{\"id\":2,\"is_admin\":1}"

:: TEST 3: SSRF
curl.exe -X POST http://127.0.0.1:5000/preview-link -H "Content-Type: application/json" -d "{\"image_url\":\"https://example.com\"}"

:: TEST 5: Info Leak
curl.exe http://127.0.0.1:5000/debug-info

:: TEST 6: Open Redirect (look for Location: in the output)
curl.exe -i "http://127.0.0.1:5000/logout?next=https://evil-example.com"


Python requests — cross-platform, no curl needed

Save this as manual_test.py and run it in Terminal 2.
Works identically on Windows, Mac, and Linux.

pythonimport requests

BASE = "http://127.0.0.1:5000"

print("\n── TEST 1: IDOR ──────────────────────────────")
print("Order 1:", requests.get(f"{BASE}/order/1").json())
print("Order 2:", requests.get(f"{BASE}/order/2").json())
print("If both show data, IDOR is present.\n")

print("── TEST 2: Mass Assignment ───────────────────")
r = requests.post(f"{BASE}/profile/update", json={"id": 2, "is_admin": 1})
print("Response:", r.json())
print("If status=updated, server accepted is_admin — mass assignment present.\n")

print("── TEST 3: SSRF ──────────────────────────────")
r = requests.post(f"{BASE}/preview-link", json={"image_url": "https://example.com"})
print(f"Response length: {len(r.content)} bytes")
print("If >100 bytes of HTML returned, SSRF is present.\n")

print("── TEST 5: Info Leak ─────────────────────────")
r = requests.get(f"{BASE}/debug-info")
print("Response:", r.json())
print("If 'encryption_key' in response, info leak present.\n")

print("── TEST 6: Open Redirect ─────────────────────")
r = requests.get(
    f"{BASE}/logout?next=https://evil-example.com",
    allow_redirects=False
)
print("Location header:", r.headers.get("Location"))
print("If evil-example.com appears, open redirect is present.\n")


General tips


After every fix, restart the server (Ctrl+C → python level3_marketplace_api.py) and run tests fresh.
Delete marketplace.db whenever you want clean sample data.
If a test still shows [VULN] after your fix, re-read the fix the agent suggested — make sure you applied it to the right function and saved the file.
It is fine if a test shows [INFO] — those require manual inspection and are explained in the test output itself.
