<%-- 
    Document   : Project 3
    Created on : Nov 8, 2020, 10:20:08 PM
    Author     : Nicholas Moore
    Part 3 of Project 3 creating a webpage to show SalestoDate
--%>
<%@ page import = "java.sql.*" %>
<%@ page import = "java.io.*"%>
<% Class.forName("oracle.jdbc.driver.OracleDriver"); %>

<%@page contentType="text/html" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>JSP Page</title>
    </head>
    <body>
        <h1>SalestoDate</h1>
        <%--Accessing the database and getting data from it--%>
        <%
            String url = "jdbc:oracle:thin:@129.7.240.3:1521:ORCL";
            Connection conn = DriverManager.getConnection(url, "MooreN", "MooreN#");
            Statement statement = conn.createStatement();
            ResultSet resultset = statement.executeQuery("SELECT O.ProductID, P.ProductFinish, SUM(O.OrderedQuantity) FROM OrderLine O, Product P WHERE O.ProductID = P.ProductID GROUP BY O.ProductID, P.ProductFinish ORDER BY O.ProductID");
        %>
        
        <%--Formating table and column ids--%>
        <TABLE BORDER="1" BGCOLOR="CCFFFF" width="50%" cellspacing="1" cellpadding="0" bordercolor="black" border="1">
            <TR>
                <TH bgcolor="DAA520"> <font size="2"/>Product ID</TH>
                <TH bgcolor="DAA520"> <font size="2"/>Product Description</TH>
                <TH bgcolor="DAA520"> <font size="2"/>Number of Times the Product was Ordered</TH>
            </TR>
            
            <%--Populating table--%>
            <% while (resultset.next()) {%>
            <TR>
                <TD> <font size='2'/><center><%= resultset.getString(1)%></center></TD>
                <TD> <font size='2'/><center><%= resultset.getString(2)%></center></TD>
                <TD> <font size='2'/><center><%= resultset.getString(3)%></center></TD>
            </TR>
            
            <%  }%>
            
        </TABLE>
    </body>
</html>
