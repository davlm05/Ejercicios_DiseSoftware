CREATE TABLE tour (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(255) NOT NULL,
    price DOUBLE NOT NULL,
    guide_name VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    max_capacity INT DEFAULT 10,
    available BOOLEAN DEFAULT TRUE
);
