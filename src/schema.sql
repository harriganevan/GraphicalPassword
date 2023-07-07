DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS images;

--add their password image ids
CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  fname TEXT NOT NULL,
  lname TEXT NOT NULL,
  pw INTEGER NOT NULL,
  attempts INTEGER NOT NULL,
  locked INTEGER NOT NULL,
  images INTEGER NOT NULL
);

CREATE TABLE images (
  id INTEGER NOT NULL,
  src TEXT NOT NULL
);

--test values
-- INSERT INTO user (username, fname, lname, pw, attempts, locked, images) VALUES 
-- ("harriganevan@gmail.com", "evan", "harrigan", 10111213, 4, 0, 101112132122232425);

--insert images
INSERT INTO images (id, src) VALUES 
(10, "../static/imgs/cat.png"),
(11, "../static/imgs/fox.png"),
(12, "../static/imgs/frog.png"),
(13, "../static/imgs/giraffe.png"),
(14, "../static/imgs/horse.png"),
(15, "../static/imgs/lion.png"),
(16, "../static/imgs/monkey.png"),
(17, "../static/imgs/penguin.png"),
(18, "../static/imgs/rabbit.png"),
(19, "../static/imgs/apple.png"),
(20, "../static/imgs/cheese.png"),
(21, "../static/imgs/dragon.png"),
(22, "../static/imgs/hamburger.png"),
(23, "../static/imgs/ice-cream.png"),
(24, "../static/imgs/mask.png"),
(25, "../static/imgs/planet.png"),
(26, "../static/imgs/scissors.png"),
(27, "../static/imgs/pinata.png"),
(28, "../static/imgs/cactus.png"),
(29, "../static/imgs/trumpet.png"),
(30, "../static/imgs/sweet.png"),
(31, "../static/imgs/diamond.png"),
(32, "../static/imgs/health.png"),
(33, "../static/imgs/sun.png"),
(34, "../static/imgs/joystick.png"),
(35, "../static/imgs/gingerbread-man.png"),
(36, "../static/imgs/ufo.png");