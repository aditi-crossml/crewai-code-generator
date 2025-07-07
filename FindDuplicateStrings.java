import java.util.HashMap;
import java.util.Map;

public class FindDuplicateStrings {

    public static void main(String[] args) {
        String[] strings = {"apple", "banana", "apple", "orange", "banana", "apple"};

        Map<String, Integer> stringCounts = new HashMap<>();

        for (String str : strings) {
            stringCounts.put(str, stringCounts.getOrDefault(str, 0) + 1);
        }

        System.out.println("Duplicate strings:");
        for (Map.Entry<String, Integer> entry : stringCounts.entrySet()) {
            if (entry.getValue() > 1) {
                System.out.println(entry.getKey() + ": " + entry.getValue());
            }
        }
    }
}