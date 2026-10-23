import java.awt.Desktop;
import java.io.File;
import java.io.IOException;
import java.util.Random;
import java.util.Set;
import java.util.TimerTask;
import java.util.stream.Collectors;
import java.util.stream.Stream;

public class Worker extends TimerTask {

    private String dir;
    private boolean finished = false;
    private Set<String> files;
    private Random rand = new Random();

    public Worker(String dir) {
        this.dir = dir;
        this.files = listFilesUsingJavaIO(dir);
    }

    public boolean isFinished() {
        return finished;
    }

    public void run() {
            if (files.isEmpty()) {
            finished = true;
            cancel();
            return;
            }
            int random = 0;
            if (files.size() > 1) random = rand.nextInt(files.size() - 1);
            String image = (String) files.toArray()[random];
            while (!image.endsWith(".jpg") && !image.endsWith(".png") && !image.endsWith(".jpeg") && !image.endsWith(".gif") && !image.endsWith(".bmp")) {
                files.remove(image);
                if (files.isEmpty()) {
                    finished = true;
                    cancel();
                    return;
                }
                random = rand.nextInt(files.size());
                image = (String) files.toArray()[random];
            }
            try {
                Desktop.getDesktop().open(new File(dir + "\\" + image));
            } catch (IOException e) {
                e.printStackTrace();
            }
            files.remove(image);
    }

    public static Set<String> listFilesUsingJavaIO(String dir) {
        System.out.print(dir);
        return Stream.of(new File(dir).listFiles())
                .filter(file -> !file.isDirectory())
                .map(File::getName)
                .collect(Collectors.toSet());
    }

}
