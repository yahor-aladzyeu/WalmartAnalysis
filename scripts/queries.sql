-- 1. Retrieve full data (sample rows)
SELECT * FROM walmart_data LIMIT 10;

-- 2. Average purchase value for each city
SELECT City_Category, AVG(Purchase) AS Avg_Purchase
FROM walmart_data
GROUP BY City_Category;

-- 3. Total purchases for each city by gender
SELECT City_Category, Gender, SUM(Purchase) AS Total_Purchase
FROM walmart_data
GROUP BY City_Category, Gender;

-- 4. Most popular product category for each city
SELECT City_Category, Product_Category, COUNT(*) AS Product_Count
FROM walmart_data
GROUP BY City_Category, Product_Category
ORDER BY City_Category, Product_Count DESC;

-- 5. Average purchase value by age and marital status
SELECT Age, Marital_Status, AVG(Purchase) AS Avg_Purchase
FROM walmart_data
GROUP BY Age, Marital_Status;

-- 6. Average purchase value for each product category
SELECT Product_Category, AVG(Purchase) AS Avg_Purchase
FROM walmart_data
GROUP BY Product_Category;

-- 7. Analysis of purchases based on length of stay in the city
SELECT Stay_In_Current_City_Years, AVG(Purchase) AS Avg_Purchase
FROM walmart_data
GROUP BY Stay_In_Current_City_Years;

-- 8. Highest and lowest purchases by occupation
SELECT Occupation, MAX(Purchase) AS Max_Purchase, MIN(Purchase) AS Min_Purchase
FROM walmart_data
GROUP BY Occupation;

-- 9. Number of purchases by product category and age
SELECT Product_Category, Age, COUNT(*) AS Purchase_Count
FROM walmart_data
GROUP BY Product_Category, Age;
