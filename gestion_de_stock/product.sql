CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT, price INT, quantity INT, id_category INT, FOREIGN KEY (id_category) REFERENCES category (id)
);

INSERT INTO
    product (
        name, description, price, quantity, id_category
    )
VALUES (
        'Smartphone', 'Hight-performance mobile device', 800, 50, 1
    ),
    (
        'Jeans', 'Durable denim pants', 50, 150, 2
    ),
    (
        'Cookbook', 'Explore new recipes/technique', 25, 50, 3
    );

SELECT * FROM product;

resultat:
+----+--------------------------+--------------------------------+-------+----------+-------------+
| id | name                     | description                       | price | quantity | id_category |
+----+--------------------------+--------------------------------+-------+----------+-------------+
|  1 | Smartphone               | Hight-performance mobile device   |  800  |       50 |           1 |
|  2 | Jeans                    | Durable denim pants               |  50   |      150 |           2 |
|  3 | Cookbook                 | Explore new recipes andtechnique  |  25   |       50 |           3 |
+----+--------------------------+--------------------------------+-------+----------+-------------+
3 rows in set (0.00 sec)
