USE db;

CREATE TABLE IF NOT EXISTS client (
    id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    city VARCHAR(100),
    balance FLOAT NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    signup TIMESTAMP,
    total_spend FLOAT,
    PRIMARY KEY(id)
);

INSERT INTO client(id, name, email, city, balance, account_type, signup, total_spend)
VALUES ('C001', 'Marie Dupont', 'marie.dupont@email.fr', 'Paris', 15420.50, 'Premium', '2021-03-15 00:00:00', 8750.00);

INSERT INTO client(id, name, balance, account_type) VALUES ('C002', 'Jean Martin', 3200.00, 'Standard');
INSERT INTO client(id, name, balance, account_type) VALUES ('C003', 'Sophie Bernard', 28900.00, 'VIP');
INSERT INTO client(id, name, balance, account_type) VALUES ('C004', 'Lucas Petit', 750.00, 'Standard');

CREATE TABLE IF NOT EXISTS product (
    id VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO product(id, name, price, stock) VALUES ('P001', 'Ordinateur portable Pro', 899.00, 45);
INSERT INTO product(id, name, price, stock) VALUES ('P002', 'Souris ergonomique', 49.90, 45);
INSERT INTO product(id, name, price, stock) VALUES ('P003', 'Bureau réglable', 350.00, 18);
INSERT INTO product(id, name, price, stock) VALUES ('P004', 'Casque audio sans fil', 129.00, 67);
INSERT INTO product(id, name, price, stock) VALUES ('P005', 'Écran 27 pouces 4K', 549.00, 30);