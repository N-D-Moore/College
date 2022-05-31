/*Clearing DBMS of all Tables and Views if present*/
DROP TABLE Salesperson;
DROP TABLE DoesBusinessIn;
DROP TABLE OrderLine;
DROP TABLE PriceUpdate;
DROP TABLE Orders; --
DROP TABLE Product; --
DROP TABLE ProductLine;
DROP TABLE Territory; --
DROP TABLE Customer; --
DROP VIEW customerbystate;
DROP VIEW dataforcustomer;
DROP VIEW pastpurchasehistory;
DROP VIEW productlinesalescomparison;
DROP VIEW totalvalueforproducts;

/*1.a
Create table Customer with columns:
CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode, CustomerEmail, CustomerUserName, CustomerPassword*/
CREATE TABLE Customer (
    CustomerID int,
    CustomerName varchar(50),
    CustomerAddress varchar(50),
    CustomerCity varchar(50),
    CustomerState varchar(50),
    CustomerPostalCode varchar(50),
    CustomerEmail varchar(50),
    CustomerUsername varchar(50),
    CustomerPassword varchar(50),
    PRIMARY KEY(CustomerID)
);

/*1.a
Create table Territroy with columns:
TerritoryID, TerritoryName*/
CREATE TABLE Territory(
    TerritoryID int,
    TerritoryName varchar(50),
    PRIMARY KEY(TerritoryID)
);

/*1.a
Create table Salesperson with columns:
SalespersonID, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUserName, SalespersonPassword,TerritoryID*/
CREATE TABLE Salesperson(
    SalespersonID int,
    SalespersonName varchar(50),
    SalespersonPhone int,
    SalespersonEmail varchar(50),
    SalespersonUserName varchar(50),
    SalespersonPassword varchar(50),
    TerritoryID int,
    PRIMARY KEY(SalespersonID),
    FOREIGN KEY(TerritoryID) REFERENCES Territory
);

/*1.a
Create table DoesBusinessIn with columns:
CustomerID, TerritoryID*/
CREATE TABLE DoesBusinessIn(
    CustomerID int,
    TerritoryID int,
    PRIMARY KEY(CustomerID, TerritoryID),
    FOREIGN KEY(CustomerID) REFERENCES Customer,
    FOREIGN KEY(TerritoryID) REFERENCES Territory
);

/*1.a
Create table ProductLine with columns:
ProductLineID, ProductLineName*/
CREATE TABLE ProductLine(
    ProductLineID int,
    ProductLineName varchar(50),
    PRIMARY KEY(ProductLineID)
);

/*1.a
Create table Product with columns:
ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID, Photo*/
CREATE TABLE Product(
    ProductID int,
    ProductName varchar(50),
    ProductFinish varchar(50),
    ProductStandardPrice varchar(50),
    ProductLineID int,
    Photo varchar(50),
    PRIMARY KEY(ProductID),
    FOREIGN KEY(ProductLineID) REFERENCES ProductLine
);

/*1.a
Create table Orders with columns:
OrderID, OrderDate, CustomerID*/
CREATE TABLE Orders(
    OrderID int,
    OrderDate date,
    CustomerID int,
    PRIMARY KEY(OrderID),
    FOREIGN KEY(CustomerID) REFERENCES Customer
);

/*1.a
Create table OrderLine with columns:
OrderID, ProductID, OrderedQuantity, SalePrice*/
CREATE TABLE OrderLine(
    OrderID int,
    ProductID int,
    OrderedQuantity int,
    SalePrice int,
    FOREIGN KEY(OrderID) REFERENCES Orders,
    FOREIGN KEY(ProductID) REFERENCES Product
);

/*1.a
Create table PriceUpdate with columns:
PriceUpdateID, DateChanged, OldPrice, NewPrice*/
CREATE TABLE PriceUpdate(
    PriceUpdateID int,
    DateChanged date DEFAULT SYSDATE,
    OldPrice int,
    NewPrice int,
    PRIMARY KEY(PriceUpdateID)
);

/*1.a
Create view ProductLineSalesComparison with columns:
ProductName, Ordered Quantity*/
CREATE VIEW ProductLineSalesComparison AS
SELECT P.ProductName, SUM(OL.OrderedQuantity) AS "Ordered Quantity"
FROM ProductLine PL, Product P, OrderLine OL
WHERE P.ProductLineID = PL.ProductLineID AND OL.ProductID = P.ProductID
GROUP BY P.ProductName;

/*1.a
Create view TotalValueForProducts with columns:
ProductName, Total Value of Orders*/
CREATE VIEW TotalValueForProducts AS
SELECT P.ProductName, SUM(OL.OrderedQuantity*P.ProductStandardPrice) AS "Total Value of Orders"
FROM Product P, OrderLine OL
WHERE OL.ProductID = P.ProductID
GROUP BY P.ProductName;

/*1.a
Create view DataForCustomer with columns:
ProductName, ProductStandardPrice*/
CREATE VIEW DataForCustomer AS
SELECT P.ProductName, P.ProductStandardPrice
FROM Product P;

/*1.a
Create view CustomerByState with columns:
CustomerState, Number of Customers*/
CREATE VIEW CustomerByState AS
SELECT C.CustomerState, COUNT(C.CustomerState) AS "Number of Customers"
FROM Customer C
GROUP BY C.CustomerState;

/*1.a
Create view PastPurchaseHistory with columns:
CustomerID, OrderDate, OrderedQuantity, ProductStandardPrice, ProductName*/
CREATE VIEW PastPurchaseHistory AS
SELECT O.CustomerID, O.OrderDate, OL.OrderedQuantity, P.ProductStandardPrice, P.ProductName
FROM Orders O, OrderLine OL, Product P
WHERE O.OrderID = OL.OrderID AND OL.ProductID = P.ProductID
ORDER BY O.CustomerID;

/*1.b Generate Relation Diagram by File -> Data Modeler -> Import -> Data Dictionary*/

/*2 Insert given data into table Customer*/
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(1, 'Contemporary Casuals', '1355 S Hines Blvd', 'Gainesville', 'FL', '32601-2871');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(2, 'Value Furnitures', '15145 S.W. 17th St.', 'Plano', 'TX', '75094-7734');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode, CustomerEmail, CustomerUserName, CustomerPassword) VALUES(3, 'Home Furnishings', '1900 Allard Ave', 'Albany', 'NY', '12209-1125',  'homefurnishings?@gmail.com', 'CUSTOMER1', 'CUSTOMER1#');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(4, 'Eastern Furniture', '1925 Beltline Rd.', 'Carteret', 'NJ', '07008-3188');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(5, 'Impressions', '5585 Westcott Ct.', 'Sacramento', 'CA', '94206-4056');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(6, 'Furniture Gallery', '325 Flatiron Dr.', 'Boulder', 'CO', '80514-4432');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(7, 'New Furniture', 'Palace Ave', 'Farmington', 'NM', '');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(8, 'Dunkins Furniture', '7700 Main St', 'Syracuse', 'NY', '31590');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(9, 'A Carpet', '434 Abe Dr', 'Rome', 'NY', '13440');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(12, 'Flanigan Furniture', 'Snow Flake Rd', 'Ft Walton Beach', 'FL', '32548');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(13, 'Ikards', '1011 S. Main St', 'Las Cruces', 'NM', '88001');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(14, 'Wild Bills', 'Four Horse Rd', 'Oak Brook', 'Il', '60522');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(15, 'Janets Collection', 'Janet Lane', 'Virginia Beach', 'VA', '10012');
INSERT INTO Customer(CustomerID, CustomerName, CustomerAddress, CustomerCity, CustomerState, CustomerPostalCode) VALUES(16, 'ABC Furniture Co.', '152 Geramino Drive', 'Rome', 'NY', '13440');

/*2 Insert given data into table Territory*/
INSERT INTO Territory VALUES(1, 'SouthEast');
INSERT INTO Territory VALUES(2, 'SouthWest');
INSERT INTO Territory VALUES(3, 'NorthEast');
INSERT INTO Territory VALUES(4, 'NorthWest');
INSERT INTO Territory VALUES(5, 'Central');

/*2 Insert given data into table SalesPerson*/
INSERT INTO SalesPerson(SalespersonId, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUsername, SalespersonPassword, TerritoryID) VALUES(1, 'Doug Henny', '8134445555', 'salesperson?@gmail.com', 'SALESPERSON', 'SALESPERSON#',1);
INSERT INTO SalesPerson(SalespersonId, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUsername, SalespersonPassword, TerritoryID) VALUES(2, 'Robert Lewis', '8139264006', '', '', '', 2);
INSERT INTO SalesPerson(SalespersonId, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUsername, SalespersonPassword, TerritoryID) VALUES(3, 'William Strong', '5053821212', '', '', '', 3);
INSERT INTO SalesPerson(SalespersonId, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUsername, SalespersonPassword, TerritoryID) VALUES(4, 'Julie Dawson', '4355346677', '', '', '', 4);
INSERT INTO SalesPerson(SalespersonId, SalespersonName, SalespersonPhone, SalespersonEmail, SalespersonUsername, SalespersonPassword, TerritoryID) VALUES(5, 'Jacob Winslow', '2238973498', '', '', '', 5);

/*2 Insert given data into table DoesBusinessIn*/
INSERT INTO DoesBusinessIn VALUES(1, 1);
INSERT INTO DoesBusinessIn VALUES(2, 2);
INSERT INTO DoesBusinessIn VALUES(3, 3);
INSERT INTO DoesBusinessIn VALUES(4, 4);
INSERT INTO DoesBusinessIn VALUES(5, 5);
INSERT INTO DoesBusinessIn VALUES(6, 1);
INSERT INTO DoesBusinessIn VALUES(7, 2);

/*2 Insert given data into table ProductLine*/
INSERT INTO ProductLine(ProductLineID, ProductLineName) VALUES(1, 'Cherry Tree');
INSERT INTO ProductLine(ProductLineID, ProductLineName) VALUES(2, 'Scandinavia');
INSERT INTO ProductLine(ProductLineID, ProductLineName) VALUES(3, 'Country Look');

/*2 Insert given data into table Product*/
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID, Photo) VALUES(1, 'End Table', 'Cherry', 175, 1, 'table.jpg');
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(2, 'Coffee Table', 'Natural Ash', 200, 2);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(3, 'Computer Desk', 'Natural Ash', 375, 2);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(4, 'Entertainment Center', 'Natural Maple', 650, 3);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(5, 'Writers Desk', 'Cherry', 325, 1);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(6, '8-Drawer Desk', 'White Ash', 750, 2);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(7, 'Dining Table', 'Natural Ash', 800, 2);
INSERT INTO Product(ProductID, ProductName, ProductFinish, ProductStandardPrice, ProductLineID) VALUES(8, 'Computer Desk', 'Walnut', 250, 3);

/*2 Insert given data into table Orders*/
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1001, '21/Aug/16', 1);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1002, '21/Jul/16', 8);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1003, '22/ Aug/16', 15);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1004, '22/Oct/16', 5);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1005, '24/Jul/16', 3);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1006, '24/Oct/16', 2);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1007, '27/ Aug/16', 5);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1008, '30/Oct/16', 12);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1009, '05/Nov/16', 4);
INSERT INTO Orders(OrderID, OrderDate, CustomerID) VALUES(1010, '05/Nov/16', 1);

/*2 Insert given data into table OrderLine*/
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1001, 1, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1001, 2, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1001, 4, 1);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1002, 3, 5);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1003, 3, 3);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1004, 6, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1004, 8, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1005, 4, 4);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1006, 4, 1);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1006, 5, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1006, 7, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1007, 1, 3);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1007, 2, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1008, 3, 3);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1008, 8, 3);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1009, 4, 2);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1009, 7, 3);
INSERT INTO OrderLine(OrderID, ProductID, OrderedQuantity) VALUES(1010, 8, 10);

/*2 no inserts given for PriceUpdate
INSERT INTO PriceUpdate VALUES();*/


/*3.1 Which products have a standard price of less than $ 275?
ProductName             ProductStandardPrice
End Table               175
Coffee Table            200
Computer Desk           250*/
SELECT P.ProductName, P.ProductStandardPrice
FROM Product P
WHERE P.ProductStandardPrice < 275;

/*3.2 List the unit price, product name, and product ID for all products in the Product table. 
ProductStandardPrice            ProductName                 ProductID
175                             End Table                   1
200                             Coffee Table                2
375                             Computer Desk               3
650                             Entertainment Center        4
325                             Writers Desk                5
750                             8-Drawer Desk               6
800                             Dining Table                7
250                             Computer Desk               8*/
SELECT P.ProductStandardPrice, P.ProductName, P.ProductID
FROM Product P;

/*3.3 What is the average standard price for all products in inventory? 
Average Price of All Products
440.625*/
SELECT AVG(P.ProductStandardPrice) AS "Average Price of All Products"
FROM Product P;

/*3.4 How many different items were ordered on order number 1004? 
OrderID         Total Items Ordered
1004            4*/
SELECT OL.OrderID, SUM(OL.OrderedQuantity) AS "Total Items Ordered"
FROM OrderLine OL
WHERE OrderID='1004' group by OL.OrderID;

/*3.5 Which orders have been placed since 10/ 24/ 2010? 
OrderID         OrderDate
1001            21-AUG-16
1002            21-JUL-16
1003            22-Aug-16
1004            22-OCT-16
1005            24-JUL-16
1006            24-OCT-16
1007            27-AUG-16
1008            30-OCT-16
1009            05-NOV-16
1010            05-NOV-16*/
SELECT O.OrderID, O.OrderDate
FROM Orders O
WHERE O.OrderDate > '24/Oct/10';

/*3.6 What furniture does COSC3380 carry that isnâ€™t made of cherry? 
Product Name                ProductFinish
Coffee Table                Natural Ash
Computer Desk               Natural Ash
Entertainment Center        Natural Maple
8-Drawer Desk               White Ash
Dining Table                Natural Ash
Comptuer Desk               Walnut*/
SELECT P.ProductName, P.ProductFinish
FROM Product P
WHERE NOT P.ProductFinish='Cherry';

/*3.7 List product name, finish, and standard price for all desks and all tables that cost more than $ 300 in the Product table. 
ProductName             ProductFinish           ProductStandardPrice
Computer Desk           Natural Ash             375
Writers Desk            Cherry                  325
8-Drawer Desk           Whiter Ash              750
Dining Table            Natural Ash             800*/
SELECT P.ProductName, P.ProductFinish, P.ProductStandardPrice
FROM Product P
WHERE P.ProductStandardPrice > 300 AND (P.ProductName LIKE '%Desk%' OR P.ProductName LIKE '%Table%');

/*3.8 Which products in the Product table have a standard price between $ 200 and $ 300? 
ProductName         ProductStandardPrice
Computer Desk       250*/
SELECT P.ProductName, P.ProductStandardPrice
FROM Product P
WHERE P.ProductStandardPrice > 200 AND P.ProductStandardPrice < 300;

/*3.9 List customer, city, and state for all customers in the Customer table whose address is Florida, Texas, California, or Hawaii. 
List the customers alphabetically by state and alphabetically by customer within each state. 
CustomerName            CustomerCity            CustomerState
Contemprary Casuals     Gainesville             FL
Flanigan Furniture      Ft Walton Beach         FL
Impressions             Sacramento              CA
Value Furnitures        Plano                   TX*/
SELECT C.CustomerName, C.CustomerCity, C.CustomerState
FROM Customer C
WHERE C.CustomerState IN ('FL', 'TX', 'CA', 'HI')
ORDER BY C.CustomerName;

/*3.10 Count the number of customers with addresses in each state to which we ship. 
CustomerState           Number of Customers
NJ                      1
CA                      1
NM                      2
VA                      1
IL                      1
NY                      4
CO                      1
FL                      2
TX                      1*/
SELECT C.CustomerState, Count(*) AS "Number of Customers"
FROM Customer C
GROUP BY C.CustomerState;

/*3.11 Count the number of customers with addresses in each city to which we ship. List the cities by state. 
CustomerCity            CustomerState           Number of Customers
Sacramento              CA                      1
Boulder                 CO                      1
FT Walton Beach         FL                      1
Gainesville             FL                      1
Oak Brook               IL                      1
Carteret                NJ                      1
Farmington              NM                      1
Las Cruces              NM                      1
Albany                  NY                      1
Rome                    NY                      2
Syracuse                NY                      1
Plano                   TX                      1
Virginia Beach          VA                      1*/
SELECT C.CustomerCity, C.CustomerState, Count(*) AS "Number of Customers"
FROM Customer C
GROUP BY C.CustomerCity, C.CustomerState
ORDER BY C.CustomerState;

/*3.12 Find only states with more than one customer. 
CustomerState           Number of Customers
NM                      2
NY                      4
FL                      2*/
SELECT C.CustomerState, Count(*) AS "Number of Customers"
FROM Customer C 
GROUP BY C.CustomerState
HAVING COUNT(*)>1;

/*3.13 List, in alphabetical order, the product finish and the average standard price for each finish for selected finishes having an average standard price less than 750. 
ProductFinish             Average Price
Cherry                    250
Natural Ash               458.333
Natural Maple             650
Walnut                    250*/
SELECT P.ProductFinish, AVG(P.ProductStandardPrice) AS "Average Price"
FROM Product P
GROUP BY P.ProductFinish
HAVING AVG(P.ProductStandardPrice)<750 
ORDER BY P.ProductFinish;

/*3.14 What is the total value of orders placed for each furniture product? 
ProductName             Total Value Ordered
8-Drawer Desk           1500
Writers Desk            650
Computer Desk           7875
Coffee Table            800
Entertainment Center    5200
Dining Table            4000
End Table               875*/
SELECT P.ProductName, SUM(P.ProductStandardPrice*OL.OrderedQuantity) AS "Total Value Ordered"
FROM Product P, OrderLine OL
WHERE P.ProductID=OL.ProductID 
GROUP BY P.ProductName;
