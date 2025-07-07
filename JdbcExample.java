import java.sql.*;

public class JdbcExample {

    public static void main(String[] args) {

        String url = "jdbc:mysql://localhost:3306/your_database";
        String user = "your_username";
        String password = "your_password";

        try {
            // 1. Load the Driver
            Class.forName("com.mysql.cj.jdbc.Driver");

            // 2. Establish Connection
            Connection connection = DriverManager.getConnection(url, user, password);

            // 3. Create Statement
            Statement statement = connection.createStatement();

            // 4. Execute Query
            ResultSet resultSet = statement.executeQuery("SELECT * FROM your_table");

            // 5. Process Result
            while (resultSet.next()) {
                System.out.println(resultSet.getInt("id") + "\t" + resultSet.getString("name"));
            }

            // 6. Close Connection
            resultSet.close();
            statement.close();
            connection.close();

        } catch (ClassNotFoundException e) {
            System.err.println("MySQL JDBC driver not found.");
            e.printStackTrace();
        } catch (SQLException e) {
            System.err.println("Database connection error.");
            e.printStackTrace();
        }
    }
}