/*Question 1 a,b,c create a procedure that creates a column SalePrice in table Product that holds 
the sale price 10% off if ProductStandardPrice is $400 or above and 15% off if less than $400*/
ALTER TABLE Product
DROP COLUMN SalePrice;

ALTER TABLE Product
ADD SalePrice DECIMAL(6,2);

CREATE OR REPLACE PROCEDURE ProductLineSale
AS
BEGIN
	UPDATE Product
        SET SalePrice = ProductStandardPrice*0.9
        WHERE ProductStandardPrice >= 400;
    UPDATE Product
        SET SalePrice = ProductStandardPrice*0.85
        WHERE ProductStandardPrice < 400;
END;
/
    
/* Question 2 a,b Created a sequence to auto increment PriceUpdatedID for logging purposes (was it supposed to be ProductID?)
Then created a trigger to catch a insert into PriceUpdate and add in the increamented PriceUpdateID
Then created a trigger to log old and new prices in PriceUpdate*/
CREATE SEQUENCE id_sequence
    MINVALUE 1
    START WITH 1
    INCREMENT BY 1
CACHE 10;

CREATE OR REPLACE TRIGGER PriceUpdateID_on_insert
    BEFORE INSERT ON PriceUpdate
    FOR EACH ROW
BEGIN
  SELECT id_sequence.nextval
  INTO :new.PriceUpdateID
  FROM dual;
END;
/

create or replace TRIGGER StandardPriceUpdate
    AFTER UPDATE OF ProductStandardPrice ON Product
    FOR EACH ROW
BEGIN
    INSERT INTO PriceUpdate(OldPrice, NewPrice) VALUES(:OLD.ProductStandardPrice, :NEW.ProductStandardPrice);
END;
/

/*Updating product to test trigger*/
UPDATE Product SET ProductStandardPrice=174 WHERE ProductStandardPrice=175;
UPDATE Product SET ProductStandardPrice=201 WHERE ProductStandardPrice=200;
UPDATE Product SET ProductStandardPrice=175 WHERE ProductStandardPrice=174;
UPDATE Product SET ProductStandardPrice=200 WHERE ProductStandardPrice=201;