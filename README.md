VulnScan Challenge
Find the bug before the hacker does — a 3-level AI-assisted security exercise

Three deliberately vulnerable Python codebases. One AI coding agent. Your job: write a prompt that finds every security vulnerability hiding inside.
---
For students — quick start
Step 1: Give this repo a ⭐ Star (top-right button) — your instructor needs it, and it helps other students find this!
Step 2: Fork this repo (Fork button, top-right) so you have your own copy to work on.
Step 3: Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/security-analysis-of-vulnerable-code
cd security-analysis-of-vulnerable-code
```
Step 4: Read `student-guide/SETUP.md` to understand how to run each exercise.
Step 5: Pick a level and start hunting!
---
The exercise
You have a vulnerable Python codebase. You have an AI coding agent (Claude, Antigravity, GitHub Copilot, etc.). Your goal: write a prompt that gets the agent to find every security vulnerability in the file.
The real challenge isn't running the agent — it's writing a prompt good enough to surface all the bugs, including the ones that don't look like bugs until you think about how they could be exploited.
Level	File	Difficulty	Vulnerabilities	What makes it hard?
1 — Basic	`exercises/level1/level1_student_portal.py`	⭐	4	Classic, well-known patterns
2 — Medium	`exercises/level2/level2_file_vault.py`	⭐⭐	6	Includes unsafe data handling formats
3 — Hard	`exercises/level3/level3_marketplace_api.py`	⭐⭐⭐	10	Logic flaws that don't "look" wrong
---
What you'll need
Levels 1 and 2 — no installation needed, pure Python:
```bash
python exercises/level1/level1_student_portal.py
python exercises/level2/level2_file_vault.py
```
Level 3 — Flask web server:
```bash
pip install -r exercises/level3/requirements.txt
python exercises/level3/level3_marketplace_api.py
```
See `student-guide/SETUP.md` for full run instructions and what "normal" output looks like before you start hunting.
---
Submit your findings
Once you complete a level, open an Issue on this repository (not your fork) using the "Level Complete" template. Tell us:
Which level you completed
How many vulnerabilities you found
Your best prompt (the one that surfaced the most)
The most surprising vulnerability you found
Every submission adds to the community knowledge base.
---
Prompting tips
Your AI agent is only as good as the prompt you give it. A few things to try:
Be specific about your role: "You are a senior security engineer" gets better results than "find bugs"
Ask for line numbers: the agent will anchor its findings to specific locations in the code
Ask for exploit scenarios: "show how an attacker would exploit this" forces the agent to reason beyond just naming the bug
For Level 3: a simple "find all vulnerabilities" prompt will miss at least half of them — you'll need to think about what kind of reasoning helps surface logic flaws
---
Contributing
Found a new vulnerability we missed? Built a better prompt? See CONTRIBUTING.md.
---
