SELECT ItemID
FROM (
    SELECT ItemID, MAX(Currently)
    FROM Items
);
