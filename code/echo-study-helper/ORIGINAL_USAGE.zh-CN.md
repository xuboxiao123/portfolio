# Echo 学习助手（0.2.0）

## 使用方法
1. 在 Chrome 打开 `chrome://extensions`，找到 Echo Lecture Study Helper，点“重新加载”。
2. 回到 EchoVideo 讲座页刷新，打开 Transcript 并点“读取文字稿”。
3. 点“中英字幕”“生成摘要”或某段旁的“问 AI”。插件会把对应提示词和 Transcript 复制到剪贴板，并打开 ChatGPT。
4. 切换到 ChatGPT 标签，按 Ctrl+V 粘贴并发送。ChatGPT 回答显示在 ChatGPT 页面中。

## 费用与限制
此版本不调用 OpenAI API，不需要也不会使用 API Key。请求通过你的 ChatGPT 网页账号发送，会受该账号当前套餐的使用额度/限制约束。每次翻译、摘要或追问都会复制一份讲座文字稿和对应提示词。当前浏览器界面没有稳定的官方预填/提交接口，所以需要你在 ChatGPT 页面手动粘贴并发送；插件也不会自动读取 ChatGPT 回答返回讲座页。

如果 API Key 曾保存在旧版本扩展中，扩展升级时会清除旧的 API 设置。面板仍可拖动，点击时间戳可在有时间信息时跳转。没有时间戳的 Transcript 可以交给 ChatGPT 翻译、总结或提问，但不能同步字幕/按句跳转。
