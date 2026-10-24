[← Portfolio](../../README.md)

# Personal Learning Workbench / 个人学习平台

![Learning overview and course navigation](../../assets/images/learning-workbench-overview.jpg)

A personal learning platform that connects course organisation, programming practice and local learning tools. Built iteratively with AI coding assistance, with product choices driven by day-to-day study and repeated refinement.

**Stack:** JavaScript · HTML/CSS · Python HTTP server · SQLite · JSON · local language toolchains.

## Key features / 主要功能

- **Exam planning:** brings exam dates, times, locations, revision scope and permitted materials into one view, alongside source and verification details.
- **Assignment and deadline tracking:** groups submissions and assessments by this week, next week and later; shows Sydney and Beijing times and stores the user's completion confirmations.
- **Knowledge organisation:** connects course and weekly notes with topic cards, searchable mind maps, explanations, examples and related experiments; records self-assessed mastery and mistakes for review.
- **Programming practice:** provides editable code cells, standard input and local execution for Python, Java, C/C++ and PHP, with results and error feedback.
- **Learning software and resources:** connects study activities to VS Code, Arduino IDE, Android Studio and Figma, plus course materials and supporting document tools, depending on installed applications.

Exam and deadline entries retain their course-source context. A personal completion check records progress; official course announcements and submission receipts remain the confirmation source.

## Editable code and real execution / 代码编辑与实际运行

![Editable C notebook with completed output](../../assets/images/learning-workbench-code-run.jpg)

The screenshot records a successful local run of the standalone stack demonstration: output **8, 5, 2**, exit code **0**. The workbench provides code cells, standard input, execution controls and result panels. This check verifies that example, not every runtime or feature.

## Implementation and scope

- Course and subject navigation, learning cards and reusable views.
- Editable notebooks with local Python, Java, C/C++ and PHP integrations, subject to installed toolchains.
- Python JSON endpoints, queued execution jobs, time/output limits and error reporting.
- SQLite notes and prototype records, JSON learning state and backup/restore tools.
- Document/mistake tools, mobile companion and floating notes are included as supporting modules; a full regression test of these modules is not claimed.

[Browse the public source snapshot](../../code/learning-workbench) · [Download source](../../downloads/learning-workbench-source.zip)

The application runs locally. This public project presentation and screenshots can be viewed without starting it. The exported source uses demonstration data and excludes personal records, course PDFs, transcripts, databases and local machine configuration.
