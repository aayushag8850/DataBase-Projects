drop table if exists Items;
drop table if exists Seller;
drop table if exists Bidder;
drop table if exists Bids;
drop table if exists Category;

create table Seller(
UserID STRING NOT NULL,
Country STRING,
Rating int,
Location STRING,
PRIMARY KEY(UserID)
); 

create table Bidder(
UserID STRING NOT NULL,
Country STRING,
Rating int,
Location STRING,
PRIMARY KEY(UserID)
);

create table Items(
ItemID int NOT NULL,
Name STRING,
Started STRING,
Ends STRING,
Description STRING,
Currently FLOAT,
First_Bid FLOAT,
Number_of_Bids int,
Buy_Price FLOAT,
UserID STRING,
Location STRING, 
Country STRING,
PRIMARY KEY(ItemID),
FOREIGN KEY(UserID) REFERENCES Seller(UserID)
);

create table Bids(
ItemID int NOT NULL,
UserID STRING NOT NULL,
Time STRING,
Amount FLOAT,
PRIMARY KEY(ItemID, UserID, Time),
FOREIGN KEY(ItemID) REFERENCES Items(ItemID),
FOREIGN KEY(UserID) REFERENCES Bidder(UserID)
);


create table Category(
ItemID int NOT NULL,
Category_Name STRING,
PRIMARY KEY(ItemID, Category_Name),
FOREIGN KEY(ItemID) REFERENCES Items(ItemID)
);

