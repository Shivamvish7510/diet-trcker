-- Step 1: Create the Database
CREATE DATABASE IF NOT EXISTS DietTracker3;

-- Step 2: Use the Database
USE DietTracker3;

-- Step 3: Create the Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    daily_calorie_goal INT NOT NULL,
    role VARCHAR(50) DEFAULT 'user'
);

-- Step 4: Create the Foods Table
CREATE TABLE IF NOT EXISTS Foods (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    calories_per_100g INT NOT NULL,
    protein_per_100g FLOAT NOT NULL,
    fat_per_100g FLOAT NOT NULL,
    carbs_per_100g FLOAT NOT NULL
);

-- Step 5: Create the Food_Log Table
CREATE TABLE IF NOT EXISTS Food_Log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_id INT NOT NULL,
    quantity FLOAT NOT NULL,
    log_date DATE NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (food_id) REFERENCES Foods(food_id)
);

-- Step 6: Create the Diet_Plan Table
CREATE TABLE IF NOT EXISTS Diet_Plan (
    plan_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL,
    breakfast VARCHAR(255),
    lunch VARCHAR(255),
    dinner VARCHAR(255),
    snacks VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    UNIQUE KEY unique_user_date (user_id, date)
);

-- Insert Admin and Regular Users
INSERT INTO Users (name, email, password, daily_calorie_goal, role) VALUES
('Admin User', 'admin@example.com', 'admin123', 2500, 'admin'),
('John Doe', 'john@example.com', 'john123', 2000, 'user'),
('Jane Smith', 'jane@example.com', 'jane123', 1800, 'user'),
('Mike Johnson', 'mike@example.com', 'mike123', 2200, 'user');

-- Insert Common Foods with Nutritional Information
INSERT INTO Foods (name, calories_per_100g, protein_per_100g, fat_per_100g, carbs_per_100g) VALUES
-- Fruits
('Apple', 52, 0.3, 0.2, 14),
('Banana', 89, 1.1, 0.3, 23),
('Orange', 47, 0.9, 0.1, 12),
('Strawberries', 32, 0.7, 0.3, 8),
('Blueberries', 57, 0.7, 0.3, 14),

-- Vegetables
('Broccoli', 34, 2.8, 0.4, 7),
('Carrot', 41, 0.9, 0.2, 10),
('Spinach', 23, 2.9, 0.4, 3.6),
('Sweet Potato', 86, 1.6, 0.1, 20),

-- Proteins
('Chicken Breast', 165, 31, 3.6, 0),
('Salmon', 208, 20, 13, 0),
('Eggs', 143, 13, 10, 1.1),
('Tofu', 76, 8, 4.8, 1.9),
('Lean Beef', 250, 26, 15, 0),

-- Grains
('Brown Rice', 111, 2.6, 0.9, 23),
('Quinoa', 120, 4.4, 1.9, 21),
('Whole Wheat Bread', 247, 13, 3.2, 41),
('Oats', 389, 17, 7, 66),

-- Dairy
('Milk (Whole)', 61, 3.2, 3.3, 4.8),
('Greek Yogurt', 59, 10, 0.4, 3.6),
('Cheddar Cheese', 403, 25, 33, 1.3),

-- Nuts and Seeds
('Almonds', 579, 21, 50, 22),
('Peanuts', 567, 26, 49, 16),
('Walnuts', 654, 15, 65, 14),
('Chia Seeds', 486, 17, 31, 42);

-- Insert Sample Food Logs
INSERT INTO Food_Log (user_id, food_id, quantity, log_date) VALUES
(2, 1, 150, CURDATE()),  -- John ate 150g apple today
(2, 10, 200, CURDATE()), -- John ate 200g chicken today
(2, 16, 100, CURDATE()), -- John ate 100g brown rice today
(3, 2, 120, CURDATE()),  -- Jane ate 120g banana today
(3, 11, 150, CURDATE()), -- Jane ate 150g salmon today
(3, 17, 80, CURDATE()),  -- Jane ate 80g quinoa today
(4, 3, 200, CURDATE()),  -- Mike ate 200g orange today
(4, 12, 100, CURDATE()), -- Mike ate 100g eggs today
(4, 18, 120, CURDATE()); -- Mike ate 120g whole wheat bread today

-- Insert Sample Diet Plans
INSERT INTO Diet_Plan (user_id, date, breakfast, lunch, dinner, snacks) VALUES
(2, CURDATE(), 
 'Oatmeal with blueberries and almonds', 
 'Grilled chicken with brown rice and broccoli', 
 'Baked salmon with quinoa and spinach', 
 'Greek yogurt with chia seeds'),

(3, CURDATE(), 
 'Whole wheat toast with peanut butter and banana', 
 'Quinoa salad with tofu and vegetables', 
 'Lean beef with sweet potato mash', 
 'Apple slices with almond butter'),

(4, CURDATE(), 
 'Scrambled eggs with whole wheat toast', 
 'Chicken wrap with whole wheat tortilla', 
 'Grilled fish with brown rice and carrots', 
 'Handful of mixed nuts');

-- View all data
SELECT * FROM Users;
SELECT * FROM Foods;
SELECT * FROM Food_Log;
SELECT * FROM Diet_Plan;

-- View user food logs with details
SELECT u.name, f.name AS food, fl.quantity, fl.log_date, 
       (f.calories_per_100g * fl.quantity / 100) AS total_calories
FROM Food_Log fl
JOIN Users u ON fl.user_id = u.user_id
JOIN Foods f ON fl.food_id = f.food_id;

-- View user diet plans
SELECT u.name, dp.date, dp.breakfast, dp.lunch, dp.dinner, dp.snacks
FROM Diet_Plan dp
JOIN Users u ON dp.user_id = u.user_id;


INSERT INTO Food_Log (user_id, food_id, quantity, log_date)
VALUES 
(1, 5, 150, '2023-11-15'),  -- User 1 ate 150g of food_id 5 (Blueberries)
(1, 10, 200, '2023-11-15'), -- User 1 ate 200g of food_id 10 (Chicken Breast)
(1, 16, 100, '2023-11-15'); -- User 1 ate 100g of food_id 16 (Brown Rice)

INSERT INTO Diet_Plan (user_id, date, breakfast, lunch, dinner, snacks)
VALUES 
(1, '2023-11-20', 
 'Oatmeal with berries', 
 'Grilled chicken with quinoa', 
 'Salmon with roasted vegetables', 
 'Greek yogurt with almonds');
 
 select * from users;
show tables;
select * from water_intake;


SELECT 
    SUM(f.calories_per_100g * fl.quantity / 100) AS total_calories
FROM 
    Food_Log fl
JOIN 
    Foods f ON fl.food_id = f.food_id
WHERE 
    fl.user_id = 3  -- Replace with the desired user ID
    AND fl.log_date = '2025-04-03';  -- Replace with the desired date
