import java.sql.*;
import java.util.Scanner;
import java.util.Calendar;
import java.text.ParseException;
import java.text.SimpleDateFormat;

public class project1 {

    String databaseName = "Project_1.db";


    /*SQL statements based off of https://www.tutorialspoint.com/sqlite/sqlite_java.htm
     * and https://www.sqlitetutorial.net/sqlite-java/*/
    public project1() {
    }
    public project1(String databaseName) {
        this.databaseName = databaseName;
    }
    private Connection connect() {
        Connection c = connect(databaseName);
        return c;
    }
    private Connection connect(String databaseName) {
        Connection c = null;
        String url = "jdbc:sqlite:" + databaseName;
        try {
            Class.forName("org.sqlite.JDBC");
            c = DriverManager.getConnection(url);
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        // System.out.println("Opened database successfully");

        // Create a new table
        String sql1 = "CREATE TABLE IF NOT EXISTS Members (\n"
                + "	MemberId TEXT, \n"
                + " MemberPassword TEXT \n"
                //+ "	name TEXT\n"
                + ");";
        String sql2 = "CREATE TABLE IF NOT EXISTS Tasks (\n"
                + "TaskId TEXT, \n Description TEXT, \n DueDate TEXT, \n "
                + "AssignedTo TEXT, \n CreatedOn TEXT, \n CreatedBy TEXT, \n Status TEXT, \n Color TEXT, \n"
                + "CategoryName TEXT \n"
                + ");";
        String sql3 = "CREATE TABLE IF NOT EXISTS Teams (\n"
                + "	TeamId TEXT, \n"
                + " MemberId TEXT, \n"
                + " CreatorId TEXT \n"
                + ");";
        String sql4 = "CREATE TABLE IF NOT EXISTS Categories (\n" +
                "    CategoryName TEXT, \n" +
                "    Description TEXT, \n" +
                "    CreatedBy TEXT, \n" +
                "    CreatedOn DATE \n" +
                ");";
        String sql5 = "CREATE TABLE IF NOT EXISTS Subtasks (\n" +
                "    TaskId TEXT, \n" +
                "    SubtaskId TEXT \n" +
                ");";
        try (Connection conn = DriverManager.getConnection(url); Statement stmt = conn.createStatement()) {
            stmt.execute(sql1);
            stmt.execute(sql2);
            stmt.execute(sql3);
            stmt.execute(sql4);
            stmt.execute(sql5);
        } catch (SQLException e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        //Above code should create the MemberId table if not exists aka no Project_1.db in folder prior to running program

        return c;
    }

    public void insertMembers(String MemberId, String MemberPassword) {
        String sql = "INSERT INTO Members(MemberId,MemberPassword) VALUES(?,?)";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, MemberId);
            pstmt.setString(2, MemberPassword);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void insertTasks(String TaskId, String Description, String DueDate, String AssignedTo, String CreatedOn, String CreatedBy, String Status, String Color, String CategoryName) {

        String sql = "INSERT INTO Tasks(TaskId,Description,DueDate,AssignedTo,CreatedOn,CreatedBy,Status,Color,CategoryName) VALUES(?,?,?,?,?,?,?,?,?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, TaskId);
            pstmt.setString(2, Description);
            pstmt.setString(3, DueDate);
            pstmt.setString(4, AssignedTo);
            pstmt.setString(5, CreatedOn);
            pstmt.setString(6, CreatedBy);
            pstmt.setString(7, Status);
            pstmt.setString(8, Color);
            pstmt.setString(9, CategoryName);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        // Removes category entry in task if category does not exist
        sql = "UPDATE Tasks SET CategoryName=null WHERE CategoryName=? AND NOT EXISTS(SELECT 1 FROM Categories WHERE Categories.CategoryName=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, CategoryName);
            pstmt.setString(2, CategoryName);
            pstmt.executeUpdate();

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void insertTeams(String TeamId, String MemberId, String CreatorId) {
        String sql = "INSERT INTO Teams(TeamId,MemberId,CreatorId) VALUES(?,?,?)";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, TeamId);
            pstmt.setString(2, MemberId);
            pstmt.setString(3, CreatorId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }
    public void insertCategories(String CategoryName, String Description, String CreatedBy, String CreatedOn) {
        String sql = "INSERT INTO Categories(CategoryName, Description, CreatedBy, CreatedOn) VALUES(?,?,?,?)";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, CategoryName);
            pstmt.setString(2, Description);
            pstmt.setString(3, CreatedBy);
            pstmt.setString(4, CreatedOn);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void insertSubtasks(String TaskId, String SubtaskId) {
        // Should only insert if TaskId currently exists.
        String sql = "INSERT INTO Subtasks(TaskId,SubtaskId) SELECT TaskId, ? FROM Tasks WHERE TaskId=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, SubtaskId);
            pstmt.setString(2, TaskId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    // Manipulate Methods
    public void manipulateMembers(String MemberId, String MemberPassword, String NewMemberId, String NewMemberPassword) {
        String sql = "UPDATE Teams SET MemberId=? WHERE MemberId=? AND EXISTS(SELECT 1 FROM Members WHERE MemberId=? AND MemberPassword=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewMemberId);
            pstmt.setString(2, MemberId);
            pstmt.setString(3, MemberId);
            pstmt.setString(4, MemberPassword);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql2 = "UPDATE Members SET MemberId=?, MemberPassword=? WHERE MemberId=? AND MemberPassword=?";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql2)) {
            pstmt.setString(1, NewMemberId);
            pstmt.setString(2, NewMemberPassword);
            pstmt.setString(3, MemberId);
            pstmt.setString(4, MemberPassword);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void manipulateTasks(String TaskId, String NewTaskId, String NewDescription, String NewDueDate, String NewAssignedTo, String NewCreatedOn, String NewCreatedBy, String NewStatus, String NewColor, String NewCategoryName) {
        String sql = "UPDATE Tasks SET TaskId=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewTaskId);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewTaskId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        if (NewTaskId.length() > 0) TaskId = NewTaskId;

        String sql2 = "UPDATE Tasks SET Description=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql2)) {
            pstmt.setString(1, NewDescription);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewDescription);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql3 = "UPDATE Tasks SET DueDate=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql3)) {
            pstmt.setString(1, NewDueDate);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewDueDate);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql4 = "UPDATE Tasks SET AssignedTo=? WHERE TaskId=? AND LENGTH(?)>0 AND EXISTS(SELECT 1 FROM Members WHERE MemberId=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql4)) {
            pstmt.setString(1, NewAssignedTo);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewAssignedTo);
            pstmt.setString(4, NewAssignedTo);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql5 = "UPDATE Tasks SET CreatedOn=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql5)) {
            pstmt.setString(1, NewCreatedOn);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewCreatedOn);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql6 = "UPDATE Tasks SET CreatedBy=? WHERE TaskId=? AND LENGTH(?)>0 AND EXISTS(SELECT 1 FROM Members WHERE MemberId=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql6)) {
            pstmt.setString(1, NewCreatedBy);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewCreatedBy);
            pstmt.setString(4, NewCreatedBy);

            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql7 = "UPDATE Tasks SET Status=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql7)) {
            pstmt.setString(1, NewStatus);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewStatus);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql8 = "UPDATE Tasks SET Color=? WHERE TaskId=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql8)) {
            pstmt.setString(1, NewColor);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewColor);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql9 = "UPDATE Tasks SET CategoryName=? WHERE TaskId=? AND LENGTH(?)>0 AND EXISTS(SELECT 1 FROM Categories WHERE CategoryName=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql9)) {
            pstmt.setString(1, NewCategoryName);
            pstmt.setString(2, TaskId);
            pstmt.setString(3, NewCategoryName);
            pstmt.setString(4, NewCategoryName);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void manipulateTeams(String TeamId, String MemberId, String NewTeamId, String NewMemberId) {
        if (NewMemberId.length() <= 0) NewMemberId = MemberId;
        if (NewTeamId.length() <= 0) NewTeamId = TeamId;

        String sql = "UPDATE Teams SET MemberId=?, TeamId=? WHERE MemberId=? AND TeamId=?";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewMemberId);
            pstmt.setString(2, NewTeamId);
            pstmt.setString(3, MemberId);
            pstmt.setString(4, TeamId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void manipulateCategories(String CategoryName, String NewCategoryName, String NewDescription, String NewCreatedBy, String NewCreatedOn) {
        String sql = "UPDATE Categories SET CategoryName=? WHERE CategoryName=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewCategoryName);
            pstmt.setString(2, CategoryName);
            pstmt.setString(3, NewCategoryName);
            System.out.println();
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        if (NewCategoryName.length() > 0) CategoryName = NewCategoryName;

        sql = "UPDATE Tasks SET CategoryName=? WHERE CategoryName=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewCategoryName);
            pstmt.setString(2, CategoryName);
            pstmt.setString(3, NewCategoryName);
            System.out.println();
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql2 = "UPDATE Categories SET Description=? WHERE CategoryName=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql2)) {
            pstmt.setString(1, NewDescription);
            pstmt.setString(2, CategoryName);
            pstmt.setString(3, NewDescription);
            System.out.println();
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql3 = "UPDATE Categories SET CreatedBy=? WHERE CategoryName=? AND LENGTH(?)>0 AND EXISTS(SELECT 1 FROM Members WHERE MemberId=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql3)) {
            pstmt.setString(1, NewCreatedBy);
            pstmt.setString(2, CategoryName);
            pstmt.setString(3, NewCreatedBy);
            pstmt.setString(4, NewCreatedBy);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql4 = "UPDATE Categories SET CreatedOn=? WHERE CategoryName=? AND LENGTH(?)>0";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql4)) {
            pstmt.setString(1, NewCreatedOn);
            pstmt.setString(2, CategoryName);
            pstmt.setString(3, NewCreatedOn);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void manipulateSubtasks(String TaskId, String SubtaskId, String NewTaskId, String NewSubtaskId) {
        if (NewTaskId.length() <= 0) NewTaskId = TaskId;
        if (NewSubtaskId.length() <= 0) NewSubtaskId = SubtaskId;

        String sql = "UPDATE Subtasks SET TaskId=?, SubtaskId=? WHERE TaskId=? AND SubtaskId=? AND EXISTS(SELECT 1 FROM Tasks WHERE TaskId=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, NewTaskId);
            pstmt.setString(2, NewSubtaskId);
            pstmt.setString(3, TaskId);
            pstmt.setString(4, SubtaskId);
            pstmt.setString(5, NewTaskId);
            pstmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    // Delete Methods
    public void deleteMembers(String MemberId, String MemberPassword) {
        String sql = "DELETE FROM Teams WHERE MemberId=? AND EXISTS(SELECT 1 FROM Members WHERE MemberId=? AND MemberPassword=?)";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, MemberId);
            pstmt.setString(2, MemberId);
            pstmt.setString(3, MemberPassword);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following member from Teams: " + MemberId);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql2 = "DELETE FROM Members WHERE MemberId=? AND MemberPassword=?";
        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql2)) {
            pstmt.setString(1, MemberId);
            pstmt.setString(2, MemberPassword);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following member from Members: " + MemberId);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void deleteTasks(String TaskId) {
        String sql = "DELETE FROM Tasks WHERE TaskId=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, TaskId);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following task: " + TaskId);

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        String sql2 = "DELETE FROM Subtasks WHERE TaskId=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql2)) {
            pstmt.setString(1, TaskId);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the subtasks from the following task: " + TaskId);

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

    }

    public void deleteTeams(String TeamId) {
        String sql = "DELETE FROM Teams WHERE TeamId=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, TeamId);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following team: " + TeamId);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }
    public void deleteCategories(String CategoryName) {
        String sql = "DELETE FROM Categories WHERE CategoryName=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, CategoryName);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following category: " + CategoryName);

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }

        sql = "UPDATE Tasks SET CategoryName=null WHERE CategoryName=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, CategoryName);
            pstmt.executeUpdate();
            System.out.println("Successfully removed tasks from the following category: " + CategoryName);

        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    public void deleteSubtasks(String TaskId, String SubtaskId) {
        String sql = "DELETE FROM Subtasks WHERE TaskId=? AND SubtaskId=?";

        try (Connection conn = this.connect();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setString(1, TaskId);
            pstmt.setString(2, SubtaskId);
            pstmt.executeUpdate();
            System.out.println("Successfully deleted the following subtask: " + SubtaskId);
        } catch (SQLException e) {
            System.out.println(e.getMessage());
        }
    }

    // TableName: name of the table you want to check
    // Row: array of values that you want to check exists as a row in TableName
    public boolean doesTableHaveRow(String TableName, String Row[]) {
        try (Connection conn = this.connect()){
            Statement s = conn.createStatement();
            int numOfTables = 1;
            String tableNames[] = new String[]{TableName};
            String sqlArr[] = new String[numOfTables];
            for (int i = 0; i < numOfTables; i++) {
                sqlArr[i] = "SELECT * FROM " + tableNames[i];
            }
            for (int i = 0; i < numOfTables; i++) { // Go through each table
                ResultSet rs = s.executeQuery(sqlArr[i]);
                ResultSetMetaData rsmd = rs.getMetaData();
                while (rs.next()) { // Go through each row of the current table
                    String currentRow[] = new String[rsmd.getColumnCount()];
                    for (int j = 1; j <= rsmd.getColumnCount(); j++) {
                        String colName = rsmd.getColumnName(j);
                        currentRow[j-1] = rs.getString(colName);
                    }
                    // Returns true if the current row is the row we are searching for
                    for (int j = 0; j < currentRow.length; j++) {
                        if (!currentRow[j].equals(Row[j])) {
                            break;
                        }
                        else {
                            if (j == currentRow.length-1) {
                                return true;
                            }
                        }
                    }
                }
                rs.close();
            }

        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        return false;
    }

    /**
     * Validate member with name and user
     *
     * @param name
     * @param password
     * @return
     */
    public boolean validateMember(String name, String password) {
        try (Connection c = this.connect()){
            Statement s = c.createStatement();
            String sqlCheckExist = "SELECT * FROM Members WHERE MemberId = \"" + name + "\" AND MemberPassword = \""
                    + password + "\"";
            ResultSet rs = s.executeQuery(sqlCheckExist);
            int count = 0;
            while (rs.next()) {
                count++;
            }
            rs.close();
            c.close();
            if (count != 0)
                return true;

        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        return false;
    }

    public int getListTaskOfUser(String user, int startNum) {
        int countTask = 0;
        try (Connection c = this.connect()){
            Class.forName("org.sqlite.JDBC");
            Statement s = c.createStatement();
            String sqlGetTask = "SELECT * FROM Tasks WHERE AssignedTo = \"" + user + "\"";
            ResultSet rs = s.executeQuery(sqlGetTask);
            ResultSetMetaData rsmd = rs.getMetaData();
            while (rs.next()) {
                System.out.println("Task #" + (startNum++) + ":");
                for (int j = 1; j <= rsmd.getColumnCount(); j++) {
                    String colName = rsmd.getColumnName(j);
                    System.out.println("\t" + colName + ": " + rs.getString(colName));
                }
                System.out.println();
                countTask++;
            }
            rs.close();

            String sql2 = "SELECT * FROM Subtasks WHERE EXISTS(SELECT TaskId FROM Tasks " +
                    "WHERE AssignedTo =\""+ user + "\" AND TaskId=Subtasks.TaskId)";
            ResultSet rs2 = s.executeQuery(sql2);
            ResultSetMetaData rsmd2 = rs2.getMetaData();
            startNum=1;
            while (rs2.next()) {
                System.out.println("Subtask #" + (startNum++) + ":");
                for (int j = 1; j <= rsmd2.getColumnCount(); j++) {
                    String colName = rsmd2.getColumnName(j);
                    System.out.println("\t" + colName + ": " + rs2.getString(colName));
                }
                System.out.println();
            }
            rs.close();
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        return countTask;
    }
    
    //Next 4 methods get the number of tasks either total or completed
    public int GetCount(String Individual){
    	int Count = 0;
    	try (Connection c = this.connect()){
                Statement s = c.createStatement();
                String sqlGetCount = "SELECT COUNT(*) AS Total FROM Tasks WHERE AssignedTo = \""+ Individual + "\"";
                ResultSet rs = s.executeQuery(sqlGetCount);
                Count = rs.getInt("Total");
                rs.close();
            } catch (Exception e) {
                System.err.println(e.getClass().getName() + ": " + e.getMessage());
                System.exit(0);
            }
    	return Count;
    }

    public int GetCount(String Individual, String Team){
		int Count = 0;
    	try (Connection c = this.connect()){
                Statement s = c.createStatement();
                String sqlGetCount = "SELECT COUNT(*) AS Total FROM Tasks WHERE AssignedTo = '" + Individual + "' OR AssignedTo = '" + Team + "'";
                ResultSet rs = s.executeQuery(sqlGetCount);
                Count = rs.getInt("Total");
            } catch (Exception e) {
                System.err.println(e.getClass().getName() + ": " + e.getMessage());
                System.exit(0);
            }
    	return Count;
    }

    public int GetCountComplete(String Individual){
		int Count = 0;
    	try (Connection c = this.connect()){
                Statement s = c.createStatement();
                String sqlGetCount = "SELECT COUNT(*) AS Total FROM Tasks WHERE Status = 'COMPLETE' AND AssignedTo = '" + Individual + "'";
                ResultSet rs = s.executeQuery(sqlGetCount);
                Count = rs.getInt("Total");
            } catch (Exception e) {
                System.err.println(e.getClass().getName() + ": " + e.getMessage());
                System.exit(0);
            }
    	return Count;
    }

    public int GetCountComplete(String Individual, String Team){
		int Count = 0;
    	try (Connection c = this.connect()){
                Statement s = c.createStatement();
                String sqlGetCount = "SELECT COUNT(*) AS Total FROM Tasks WHERE Status = 'COMPLETE' AND (AssignedTo = '" + Individual + "' OR AssignedTo = '" + Team + "')";
                ResultSet rs = s.executeQuery(sqlGetCount);
                Count = rs.getInt("Total");
            } catch (Exception e) {
                System.err.println(e.getClass().getName() + ": " + e.getMessage());
                System.exit(0);
            }
    	return Count;
    }
    
    //Validate that the user accessing productivity is team creator
    public boolean validateCreator(String user, String pass) {
    	try (Connection c = this.connect()){
            Statement s = c.createStatement();
            String sqlCheckExist = "SELECT * FROM Teams WHERE CreatorId = \"" + user + "\"";
            ResultSet rs = s.executeQuery(sqlCheckExist);
            int count = 0;
            while (rs.next()) {
                count++;
            }
            rs.close();
            c.close();
            if (count != 0) {
            	if (this.validateMember(user, pass))
            		return true;
            	else
            		return false;
            }

        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        return false;
    }

    public static void main(String args[]) throws ParseException {

        project1 app = new project1();
        Scanner input = new Scanner(System.in);

        System.out.println("=== TASK MANAGER ==="); // PLACEHOLDER for title

        int Choice1;
        do {

            System.out.println(
                    "Insert number of what you wish to do: \n[1] Create \n[2] Edit \n[3] Delete \n[4] Login to see tasks\n[5] Productivity Statistics\n[6] Quit");
            Choice1 = input.nextInt();
            System.out.println(); // skip line after user entry (for readability)
            switch (Choice1) {
                // Create Entity
                case 1: {
                    int Choice2;
                    do {
                        System.out.println("Insert number of what you wish to create: \n[1] Member \n[2] Task \n[3] Team \n[4] Task Category \n[5] Subtask \n[6] Back");
                        Choice2 = input.nextInt();
                        input.nextLine(); // to read the return key
                        System.out.println(); // skip line after user entry (for readability)
                        switch (Choice2) {
                            // Create Member
                            case 1: {
                                System.out.println("Enter Member ID");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                //String why = input.nextLine();
                                String a = input.nextLine();
                                System.out.println("Enter Member Password");
                                String b = input.nextLine();
                                app.insertMembers(a, b);
                                break;
                            }
                            // Create Task
                            case 2: {
                                System.out.println("Enter Task ID");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                //String why = input.nextLine();
                                String a = input.nextLine();
                                System.out.println("Enter Description");
                                String b = input.nextLine();
                                System.out.println("Enter Due Date (MM/dd/yyyy)");
                                String c = input.nextLine();
                                System.out.println("Enter Assigned To");
                                String d = input.nextLine();
                                //Make automatic once users are implemented
                                System.out.println("Enter Created On (MM/dd/yyyy)");
                                String e = input.nextLine();
                                //Make automatic at some point
                                System.out.println("Enter Created By");
                                String f = input.nextLine();
                                //Preset status options maybe?
                                System.out.println("Enter Status (INCOMPLETE/COMPLETE)");
                                String g = input.nextLine();
                                //Preset colors?
                                System.out.println("Enter Color");
                                String h = input.nextLine();
                                //Preset Category
                                System.out.println("Enter Category");
                                String i = input.nextLine();
                                
                                System.out.println("Do you want this task to repeat? (y/n)");
                                String j = input.nextLine();
                                if (j.equalsIgnoreCase("y")) {
                                	System.out.println("Will the task repeat daily, weekly, or monthly (d/w/m)");
                                	String k = input.nextLine();
                                	if (k.equalsIgnoreCase("d")) {
                                		System.out.println("For how many days will this task repeat?");
                                		//parse out int from inputed number
                                    	int l = Integer.parseInt(input.nextLine());
                                    	Calendar cal = Calendar.getInstance();
                                    	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy");
                                    	java.util.Date date = sdf.parse(c);
                                    	cal.setTime(date);
                                    	String m;
                                    	for (int z = 0; z < l; z ++) {
                                    		//code to generate new due date (string c)
                                    		cal.add(Calendar.DATE, 1);
                                    		if(z==0) {
                                    			cal.add(Calendar.DATE, -1);
                                    		}
                                    		m = sdf.format(cal.getTime());
                                    		app.insertTasks(a, b, m, d, e, f, g, h, i);
                                    	}
                                	}
                                	else if (k.equalsIgnoreCase("w")) {
                                		System.out.println("For how many weeks will this task repeat?");
                                		int l = Integer.parseInt(input.nextLine());
                                		Calendar cal = Calendar.getInstance();
                                    	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy");
                                    	java.util.Date date = sdf.parse(c);
                                    	cal.setTime(date);
                                    	String m;
                                    	for (int z = 0; z < l; z ++) {
                                    		//code to generate new due date (string c)
                                    		cal.add(Calendar.WEEK_OF_YEAR, 1);
                                    		if(z==0) {
                                    			cal.add(Calendar.WEEK_OF_YEAR, -1);
                                    		}
                                    		m = sdf.format(cal.getTime());
                                    		app.insertTasks(a, b, m, d, e, f, g, h, i);
                                    	}
                                	}
                                	else if (k.equalsIgnoreCase("m")) {
                                		System.out.println("For how many months will this task repeat?");
                                		int l = Integer.parseInt(input.nextLine());
                                		Calendar cal = Calendar.getInstance();
                                    	SimpleDateFormat sdf = new SimpleDateFormat("MM/dd/yyyy");
                                    	java.util.Date date = sdf.parse(c);
                                    	cal.setTime(date);
                                    	String m;
                                    	for (int z = 0; z < l; z ++) {
                                    		//code to generate new due date (string c)
                                    		cal.add(Calendar.MONTH, 1);
                                    		if(z==0) {
                                    			cal.add(Calendar.MONTH, -1);
                                    		}
                                    		m = sdf.format(cal.getTime());
                                    		app.insertTasks(a, b, m, d, e, f, g, h, i);
                                    	}
                                	}
                                }
                                else {
                                	app.insertTasks(a, b, c, d, e, f, g, h, i);
                                }

                                // Preset subtasks
                                String answer;
                                do {
                                    System.out.println("Do you want to add any subtasks? (y/n)");
                                    answer = input.nextLine();
                                }
                                while (!(answer.equalsIgnoreCase("y") || answer.equalsIgnoreCase("n")));
                                if (answer.equalsIgnoreCase("y")) { // add subtasks until user says to not continue
                                    do {
                                        System.out.println("Enter Task");
                                        String taskId = input.nextLine();
                                        System.out.println("Enter SubTask");
                                        String subtaskId = input.nextLine();
                                        app.insertSubtasks(taskId, subtaskId);
                                        System.out.println("Continue adding subtasks? (y/n)");
                                        answer = input.nextLine();
                                    }
                                    while (answer.equalsIgnoreCase("y"));
                                }

                                break;
                            }
                            // Create Team
                            case 3: {
                                System.out.println("Enter Team ID");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                //String why = input.nextLine();
                                String a = input.nextLine();
                                System.out.println(a);
                                System.out.println("Enter Creator ID");
                                String c = input.nextLine();
                                String d = "y";
                                while(!d.equalsIgnoreCase("n")) {
	                                System.out.println("Enter Member ID");
	                                String b = input.nextLine();
	                                System.out.println(b);
	                                app.insertTeams(a, b, c);
	                                System.out.println("Would you like to add another Member? (y/n)");
	                                d = input.nextLine();
	                                System.out.println(d);
                                }
                                break;
                            }
                            // Create Task Category
                            case 4: {
                                System.out.println("Enter Category Name");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                //String why = input.nextLine();
                                String a = input.nextLine();
                                System.out.println(a);
                                System.out.println("Enter Description");
                                String b = input.nextLine();
                                System.out.println(b);
                                System.out.println("Enter Created By");
                                String c = input.nextLine();
                                System.out.println(c);
                                System.out.println("Enter Created On");
                                String d = input.nextLine();
                                System.out.println(d);
                                app.insertCategories(a, b, c, d);
                                break;
                            }
                            // Create Subtask
                            case 5: {
                                System.out.println("Enter Task ID");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                //String why = input.nextLine();
                                String a = input.nextLine();
                                System.out.println(a);
                                System.out.println("Enter Subtask ID");
                                String b = input.nextLine();
                                System.out.println(b);
                                app.insertSubtasks(a, b);
                                break;
                            }
                            case 6: {
                                break; // exit loop, return to main menu without futher edits
                            }
                            default: {
                                System.out.println("Invalid Entry");
                            }
                        }
                    } while (Choice2 != 6);
                    break;

                }
                // Edit(manipulate) Entity
                case 2: {
                    int Choice2;
                    do {
                        System.out.println("Insert number of what you wish to edit: \n[1] Member \n[2] Task \n[3] Team \n[4] Task Category \n[5] Subtask \n[6] Back");
                        Choice2 = input.nextInt();
                        input.nextLine(); // to read the return key
                        System.out.println(); // skip line after user entry (for readability)
                        switch (Choice2) {
                            // Manipulate Member
                            case 1: {
                                System.out.println("Enter Member ID");
                                String a = input.nextLine();
                                System.out.println("Enter Member Password");
                                String b = input.nextLine();
                                System.out.println("Enter New Member ID");
                                String c = input.nextLine();
                                System.out.println("Enter New Member Password");
                                String d = input.nextLine();
                                app.manipulateMembers(a, b, c, d);
                                break;
                            }
                            // Manipulate Task
                            case 2: {
                                System.out.println("Enter Task ID");
                                //For some reason the first nextLine input gets automatically a NULL look into later
                                String a = input.nextLine();
                                System.out.println("Enter New Task ID (leave blank to skip)");
                                String b = input.nextLine();
                                System.out.println("Enter New Description (leave blank to skip)");
                                String c = input.nextLine();
                                System.out.println("Enter New Due Date (MM/dd/yyyy) (leave blank to skip)");
                                String d = input.nextLine();
                                System.out.println("Enter New Assigned To (leave blank to skip)");
                                String e = input.nextLine();
                                System.out.println("Enter New Created On (MM/dd/yyyy) (leave blank to skip)");
                                String f = input.nextLine();
                                System.out.println("Enter New Created By (leave blank to skip)");
                                String g = input.nextLine();
                                System.out.println("Enter New Status (INCOMPLETE/COMPLETE) (leave blank to skip)");
                                String h = input.nextLine();
                                System.out.println("Enter New Color (leave blank to skip)");
                                String i = input.nextLine();
                                System.out.println("Enter New Category Name (leave blank to skip)");
                                String j = input.nextLine();
                                app.manipulateTasks(a, b, c, d, e, f, g, h, i, j);
                                break;
                            }
                            // Manipulate Team
                            case 3: {
                                System.out.println("Enter Team ID");
                                String a = input.nextLine();
                                System.out.println("Enter Member ID");
                                String b = input.nextLine();
                                System.out.println("Enter New Team ID (leave blank to skip)");
                                String c = input.nextLine();
                                System.out.println("Enter New Member ID (leave blank to skip)");
                                String d = input.nextLine();
                                app.manipulateTeams(a, b, c, d);
                                break;
                            }
                            // Manipulate Task Category
                            case 4: {
                                System.out.println("Enter Category Name");
                                String a = input.nextLine();
                                System.out.println("Enter New Category Name (leave blank to skip)");
                                String b = input.nextLine();
                                System.out.println("Enter New Description (leave blank to skip)");
                                String c = input.nextLine();
                                System.out.println("Enter New Created By (leave blank to skip)");
                                String d = input.nextLine();
                                System.out.println("Enter New Created On (leave blank to skip)");
                                String e = input.nextLine();
                                app.manipulateCategories(a, b, c, d, e);
                                break;
                            }
                            // Manipulate Subtask
                            case 5: {
                                System.out.println("Enter Task ID");
                                String a = input.nextLine();
                                System.out.println("Enter Subtask ID");
                                String b = input.nextLine();
                                System.out.println("Enter New Task ID (leave blank to skip)");
                                String c = input.nextLine();
                                System.out.println("Enter New Subtask ID (leave blank to skip)");
                                String d = input.nextLine();
                                app.manipulateSubtasks(a, b, c, d);
                                break;
                            }
                            case 6: {
                                break; // exit loop, return to main menu without further edits
                            }
                            default: {
                                System.out.println("Invalid Entry");
                            }
                        }
                    } while (Choice2 != 6);
                    break;
                }
                // Delete Entity
                case 3: {
                    int Choice2;
                    do {
                        System.out.println("Insert number of what you wish to delete: \n[1] Member \n[2] Task \n[3] Team \n[4] Task Category \n[5] Subtask \n[6] Back");
                        Choice2 = input.nextInt();
                        input.nextLine(); // to read the return key
                        System.out.println(); // skip line after user entry (for readability)
                        switch (Choice2) {
                            // Delete Member
                            case 1: {
                                System.out.println("Enter Member ID");
                                String a = input.nextLine();
                                System.out.println("Enter Member Password");
                                String b = input.nextLine();
                                app.deleteMembers(a, b);
                                break;
                            }
                            // Delete Task
                            case 2: {
                                System.out.println("Enter Task ID");
                                String a = input.nextLine();
                                app.deleteTasks(a);
                                break;
                            }
                            // Delete Team
                            case 3: {
                                System.out.println("Enter Team ID");
                                String a = input.nextLine();
                                app.deleteTeams(a);
                                break;
                            }
                            // Delete Task Category
                            case 4: {
                                System.out.println("Enter Category Name");
                                String a = input.nextLine();
                                app.deleteCategories(a);
                                break;
                            }
                            // Delete Subtask
                            case 5: {
                                System.out.println("Enter Task ID");
                                String a = input.nextLine();
                                System.out.println("Enter Subtask ID");
                                String b = input.nextLine();
                                app.deleteSubtasks(a, b);
                                break;
                            }
                            case 6: {
                                break; // exit loop, return to main menu without futher edits
                            }
                            default: {
                                System.out.println("Invalid Entry");
                            }
                        }
                    } while (Choice2 != 6);
                    break;
                }
                // Log-in to see task
                case 4: {
                    int inLoginPage = 1;
                    input.nextLine(); // Ignore endline before
                    System.out.println("============LOG IN ===============");
                    do {
                        System.out.print("Name: ");
                        String user = input.nextLine();
                        System.out.print("Password: ");
                        String pass = input.nextLine();
                        if (app.validateMember(user, pass)) {
                            // If this user exist in the database. Try to print all his task
                            int countTask = app.getListTaskOfUser(user, 1);
                            System.out.println("User: " + user + " has " + countTask + " tasks shown above.");
                            inLoginPage = 0;
                        } else {
                            System.out.print("Log-in failed. Do you want to try again? (y/n): ");
                            String isContinue = input.nextLine();
                            if (isContinue.equalsIgnoreCase("n"))
                                inLoginPage = 0;
                        }
                    } while (inLoginPage != 0);
                    break;
                }
                // Print out statistics
                case 5: {
                	//In real world application would be expanded to give yearly/quarterly/monthly/weekly productivity but keeping it simple
                	//for easy generation of data for testing by graders
                	System.out.println("Enter TeamId");
                	String team = input.nextLine(); // eat return symbol
                	String user;
                	float teamPercent = 0;
                	int teamCount = 0;
                	team = input.nextLine();
                	//make user log in to check if creator
                	System.out.println("============LOG IN ===============");
                	System.out.print("Name: ");
                    String Login = input.nextLine();
                    System.out.print("Password: ");
                    String Pass = input.nextLine();
                    //if creator calculate the productivity
                    if(app.validateCreator(Login, Pass)) {
	                	try (Connection c = app.connect()){
	            			System.out.println("connected");
	                        Statement s = c.createStatement();
	                        String sqlGetUsers = "SELECT MemberId FROM Teams WHERE TeamId = '" + team + "'";
	                        ResultSet rs = s.executeQuery(sqlGetUsers);
	                        //get list of users in team and iterate through each member
	                        while (rs.next()) {
	                        	teamCount++;
	                        	user = rs.getString("MemberId");
	                        	//simple productivity by calculating % of completed tasks
	                        	System.out.println("User " + user + " Productivity: " + (float)(app.GetCountComplete(user, team))/(float)(app.GetCount(user, team))*100 + "%");
	                        	teamPercent += (float)(app.GetCountComplete(user, team))/(float)(app.GetCount(user, team))*100;
	                        }
	                    } catch (Exception e) {
	                        System.err.println(e.getClass().getName() + ": " + e.getMessage());
	                        System.exit(0);
	                    }
	                	//simple team productivity by calculating average productivity of the team
	                	System.out.println("Total Team Productivity: " + teamPercent/teamCount + "%");
                	}
                    else
                    	System.out.println("Error: Not creator or failed login");
                	break;
                }
                // Exit loop and program
                case 6: {
                	input.close();
                    break;
                }
                default: {
                    System.out.println("Invalid Entry");
                }
            }
        } while (Choice1 != 6);
    }
}

