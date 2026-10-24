# React Event Management System / React 活动管理

![Event list with search and date sorting](../../assets/images/react-events-interface.jpg)

Original student frontend: React components and Hooks, a reusable event form and an Axios REST client.

- Browse and search event records.
- Sort events by date.
- Create and edit event details through a form.
- Delete events after confirmation.
- Show loading, success and request-error feedback.

## Editing interface / 编辑界面

![Update Event form](../../assets/images/react-events-edit.jpg)

[Full project notes](../../docs/projects/project-event-manager.md) · [App component](src/App.jsx) · [REST API client](src/services/api.js)

## Run the frontend

```sh
npm ci
npm run dev
```

Requires Node.js and a compatible events API. The original client targets `http://localhost:8181/events`; update the API client for your environment. Event records use `id`, `name`, `description`, `startdate` and `enddate`.

[Recovered Express/MySQL companion API](../event-api-reference) is stored separately as course reference material. It is not claimed as independently authored backend work. Screenshots show the owner-provided interface; they do not establish a fresh end-to-end test of the archive.

[← Source index](../README.md) · [Portfolio README](../../README.md)
