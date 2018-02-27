import java.sql.*;

public class dbtest {
public static void main(String[] args) {
try{
String URL = "jdbc:mysql://zwgaqwfn759tj79r.chr7pe7iynqr.eu-west-1.rds.amazonaws.com/igqxgrcy5dw9rxc2";
String USER = "gqk0vs5rc6nfbj0w";
String PASS = "ib45oys91og5m4q5";
Connection myDbConn = DriverManager.getConnection(URL, USER, PASS);
Statement myStmt = myDbConn.createStatement();
System.out.println(myStmt.toString());
}catch (Exception e) {
	System.out.println(e.getMessage());
}
}
}