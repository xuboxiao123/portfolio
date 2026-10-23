-- Reconstructed example schema from Events.js queries; not an original submission.
-- 根据查询语句补写的最小示例，不是找回的原始数据库文件。
CREATE TABLE IF NOT EXISTS events (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  startdate DATE NOT NULL,
  enddate DATE NOT NULL
);
