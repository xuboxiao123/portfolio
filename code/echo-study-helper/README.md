# Echo Lecture Study Helper / Echo 讲座学习助手

An AI-assisted personal browser-extension prototype, version 0.2.0, for studying EchoVideo lecture transcripts. / 使用 AI 辅助开发的个人学习插件原型，版本 0.2.0。

## Features / 功能

- Reads transcript text already visible in an EchoVideo page. / 读取页面已有讲稿。
- Prepares translation, summary and question prompts. / 整理中英翻译、摘要和追问提示词。
- Copies the prompt to the clipboard and opens ChatGPT. The user manually pastes and sends it. / 复制后打开 ChatGPT，由用户粘贴发送。
- Supports a draggable panel and seeking when timestamps are available. / 可拖动面板；有时间戳时支持跳转。

## Install locally / 本地安装

1. Download this directory, or extract the source archive linked from the portfolio.
2. Open Chrome's extensions page, enable Developer mode and choose **Load unpacked**.
3. Select this directory; open an EchoVideo lecture and its transcript, then use the helper panel.

下载目录后在 Chrome 扩展页启用开发者模式，选择“加载已解压的扩展程序”。本次发布未替用户安装插件。

## Scope and privacy / 范围与数据

This version uses no OpenAI API key and makes no direct OpenAI API calls. ChatGPT responses stay in ChatGPT; the extension does not read them back into the lecture page. The user chooses which transcript text to send. The archive includes only extension code, no lecture transcripts, recordings, account cookies or stored settings. Permissions: storage and clipboardWrite; EchoVideo host matches are declared in manifest.json.

当前版本不调用 OpenAI API，也不读取 ChatGPT 回答。只归档插件源码，未包含讲义、录像、账号或缓存。页面适配及时间戳解析依赖 EchoVideo 的实际界面，历史版本的端到端兼容性未在此次上传时重新验证。

Source / 来源: E:/Codex/2026-09-25/unsw-ai-echovideo-assistant. Original Chinese usage notes are preserved in ORIGINAL_USAGE.zh-CN.md.
