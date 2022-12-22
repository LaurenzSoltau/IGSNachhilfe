INSERT INTO user (username, email, password)
VALUES
  ('test', 'test.test@gmail.com', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
  ('other', 'test2.test2@gmail.com', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');

INSERT INTO post (offerer, email, title, body, subject, grade_from, grade_to, created)
VALUES
  (1, 'test.test@gmail.com', 'test title', 'test' || x'0a' || 'body', 'deutsch,englisch,mathe', 5, 7, '2022-01-01 00:00:00');