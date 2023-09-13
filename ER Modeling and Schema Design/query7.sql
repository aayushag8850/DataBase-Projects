SELECT COUNT(DISTINCT Category.Category_Name)
FROM Category
INNER JOIN Items ON Category.ItemID = Items.ItemID
WHERE Items.Currently > 100
AND Items.Number_of_Bids > 0;
