// Pile générique bornée
import java.util.ArrayList;

public class Pile<T> {
    private final ArrayList<T> elements = new ArrayList<>();
    private static final int MAX = 64;

    public boolean empiler(T x) {
        if (elements.size() >= MAX) return false;
        elements.add(x);
        return true;
    }

    @Override
    public String toString() { return "Pile(" + elements.size() + ")"; }
}
