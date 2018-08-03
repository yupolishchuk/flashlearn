DROP TABLE IF EXISTS flashcard;

CREATE TABLE flashcard (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    question VARCHAR(255) NOT NULL,
    answer VARCHAR(255) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);