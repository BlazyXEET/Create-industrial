import java.io.IOException;
import java.nio.file.*;
import java.util.*;
import javax.tools.*;
import com.sun.source.util.JavacTask;

public class JavaSyntaxCheck {
    public static void main(String[] args) throws IOException {
        JavaCompiler compiler = ToolProvider.getSystemJavaCompiler();
        DiagnosticCollector<JavaFileObject> dc = new DiagnosticCollector<>();
        var stream = Files.walk(Path.of(args[0]));
        List<java.io.File> files;
        try (stream) {
            files = stream.filter(p -> p.toString().endsWith(".java")).map(Path::toFile).toList();
        }
        try (StandardJavaFileManager fm = compiler.getStandardFileManager(dc, null, null)) {
            var sources = fm.getJavaFileObjectsFromFiles(files);
            JavacTask task = (JavacTask)compiler.getTask(null, fm, dc, List.of("--release", "21", "-proc:none"), null, sources);
            task.parse();
        }
        for (var d : dc.getDiagnostics()) {
            System.err.println(d);
        }
        if (dc.getDiagnostics().stream().anyMatch(d -> d.getKind() == Diagnostic.Kind.ERROR))
            throw new AssertionError("Java syntax invalid");
        System.out.println("PASS: parsed " + files.size() + " Java source files under JDK 21");
    }
}
