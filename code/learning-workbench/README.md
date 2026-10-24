# Personal Learning Workbench / 学习工作台

A personal desktop learning application developed iteratively with AI coding assistance. It brings course navigation, editable programming notebooks, local code execution, document/learning tools and persistent notes into one browser interface.

![Code editor and a completed C stack run](../../assets/images/learning-workbench-code-run.jpg)

## Key features / 主要功能

- **Exam planning:** brings exam dates, times, locations, revision scope and permitted materials into one view, alongside source and verification details.
- **Assignment and deadline tracking:** groups submissions and assessments by this week, next week and later; shows Sydney and Beijing times and stores the user's completion confirmations.
- **Knowledge organisation:** connects course and weekly notes with topic cards, searchable mind maps, explanations, examples and related experiments; records self-assessed mastery and mistakes for review.
- **Programming practice:** provides editable code cells, standard input and local execution for Python, Java, C/C++ and PHP, with results and error feedback.
- **Learning software and resources:** connects study activities to VS Code, Arduino IDE, Android Studio and Figma, plus course materials and supporting document tools, depending on installed applications.

Exam and deadline entries retain their course-source context. A personal completion check records progress; official course announcements and submission receipts remain the confirmation source.

## Implementation

- Frontend: plain JavaScript, HTML and CSS; route-based navigation and reusable study views.
- Backend: Python `ThreadingHTTPServer`, JSON endpoints, local job execution and time/output limits.
- Storage: SQLite for notes and prototype records; JSON for learning state and metadata.
- Runtimes: Python plus optional Java, C/C++ via Zig, and PHP toolchains.
- Supporting modules: notebook sessions, learning/mistake records, document tools, mobile companion, floating notes and transcript utilities.

## Start the public demo snapshot

```sh
python -m pip install -r requirements.txt
python configure_demo.py
python server.py 18768
```

Open `http://127.0.0.1:18768/`. The Python example works with Python; the C stack demonstration also needs Zig on PATH. Configure optional toolchains in the generated `config.json`.

This is a local desktop tool. Code cells execute on the host computer, so the server binds to loopback. The public portfolio displays screenshots rather than a remotely hosted code runner.

## Source snapshot

The application modules are included with a small demonstration dataset. Personal study records, student identity, timetable/assessment allocations, course PDFs, licensed resources, transcripts, logs, databases and local runtime binaries are excluded. `canonical_entry.js` is adapted to allow the user's chosen local origin/port. Screenshots show the owner's full local installation; the public snapshot starts with demonstration data.

[Project and screenshots](../../docs/projects/project-learning-workbench.md) · [Portfolio README](../../README.md)
