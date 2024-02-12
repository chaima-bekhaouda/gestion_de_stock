CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)
);

INSERT INTO category (name) VALUES
('Informatiques'),
('Habits'),
('Livres');

SELECT * FROM category;

resultat:
+----+---------------+
| id | name          |
+----+---------------+
|  1 | Informatiques |
|  2 | Habits        |
|  3 | Livres        |
+----+---------------+
3 rows in set (0.00 sec)
