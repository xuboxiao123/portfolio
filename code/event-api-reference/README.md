# Events REST API — course companion / 活动管理配套 API

Recovered from ExpressEventsAPI(1).zip in the user's coursework downloads. This is a course-companion backend reference; the archive does not establish authorship, so it is **not presented as an independently authored backend by Boxiao Xu**. / 课程资料中的配套后端，作者未能从压缩包确认，不作为本人独立开发成果。

The existing [React frontend](../react-events/) calls http://localhost:8181/events, matching this API's port and routes. Express, CORS and mysql2 provide list, lookup, create, update and delete endpoints. No original SQL dump was found in this archive; schema.example.sql is newly reconstructed from the SQL queries and is labelled accordingly.

## Run locally / 本地运行

```powershell
npm ci
$env:DB_HOST="localhost"
$env:DB_USER="your_user"
$env:DB_PASSWORD="your_password"
$env:DB_NAME="events_db"
node app.js
```

Import schema.example.sql into an empty local database first. Keep real database credentials outside source files. The publication copy replaces the historical database settings with environment variables; other API source is preserved. JavaScript syntax was checked; a live MySQL integration is not claimed in this audit. / 先准备本地数据库；本次做语法检查，未声称已完成数据库联调。

The code is a historical coursework companion and does not include authentication. Use it locally for review. Original package metadata is preserved; no authorship or ownership is reassigned.
