# Setup Guide — Vulnerability Discovery Exercise

This guide tells you how to run each codebase, **before** you ask your AI agent
to analyze it. Always run the code first and note what it outputs — once you
(or your agent) apply a fix, run it again. If the same normal output still
appears, your fix didn't break anything. If it changed or crashed, you fixed
too aggressively and need to adjust.

---

## Level 1 — `level1_student_portal.py`

**Requirements:** none — pure Python, nothing to install.

**How to run:**
```
python level1_student_portal.py
```

**What you'll see (this is normal — note it down):**
```
Student Grade Portal — sample students: Aarav, Priya, Rohan

Enter student name: Aarav
Grade: (88,)
```
Type one of the sample names (`Aarav`, `Priya`, or `Rohan`) when prompted.

---

## Level 2 — `level2_file_vault.py`

**Requirements:** none — pure Python, nothing to install.

**How to run:**
```
python level2_file_vault.py
```
This one doesn't ask for input — it runs a short demo automatically.

**What you'll see (this is normal — note it down):**
```
Campus File Vault

Login with correct password: True
Downloaded file contents: Sample report card contents.
Vault Alert: demo_student downloaded report_card.txt
Restored session: {'username': 'demo_student', 'logged_in': True}
```

**Tip:** if you want to reset the demo data, delete `vault.db` and the
`vault_files/` folder before running again.

---

## Level 3 — `level3_marketplace_api.py`

This one is different — it's a small web server, not a script that runs once
and stops. You'll need two things open at the same time: the server, and a
way to send it requests.

**Requirements:**
```
pip install flask pyjwt requests
```

**Step 1 — start the server (leave this terminal running):**
```
python level3_marketplace_api.py
```
You should see something like:
```
* Running on http://127.0.0.1:5000
```
Leave this terminal open. Press `Ctrl+C` here whenever you want to stop the
server.

**Step 2 — open a SECOND terminal (or your browser) to send it requests.**

The easiest way to test an endpoint from a browser is to just visit a URL
directly, for `GET` endpoints:
```
http://127.0.0.1:5000/order/1
```
**Expected normal output:**
```json
[1, 1, "Physics Textbook", 450.0]
```

For endpoints that need more than a simple visit (the `POST` ones), use
`curl` in your second terminal. Here's one safe example to confirm the
server is working correctly:
```
curl -X POST http://127.0.0.1:5000/preview-link -H "Content-Type: application/json" -d "{\"image_url\":\"https://example.com\"}"
```
This should return the raw HTML of `example.com` — proving the endpoint
works as intended.

**Tip:** if you want to reset the demo data, stop the server, delete
`marketplace.db`, then start the server again.

---

## General advice for this exercise

1. **Run the code first, before involving your agent.** Know what "working
   correctly" looks like.
2. **Read the code yourself for a few minutes** before handing it to the
   agent — you'll understand its findings much better.
3. **After applying any suggested fix, re-run the program** and compare the
   output to your notes from step 1. A correct fix closes the security hole
   *without* changing normal behavior.
4. **If something stops working after a fix,** that's a useful signal too —
   ask your agent why, and whether there's a way to fix the vulnerability
   without breaking the feature.
