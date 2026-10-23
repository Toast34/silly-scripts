import javax.swing.*;
import javax.swing.border.Border;
import javax.swing.border.LineBorder;
import java.awt.*;
import java.io.File;
import java.io.IOException;
import java.util.Random;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.Stream;

import static javax.swing.SwingConstants.*;
import static javax.swing.WindowConstants.*;

public class TimedImages {

    public static void main(String[] args) throws Exception {
        // for (File file:
        // new File(args[0]).listFiles()) {
        //     System.out.println(file.getName());
        // }

        MainMenu menu = new MainMenu();
        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(EXIT_ON_CLOSE);
        frame.setSize(800,600);
        frame.add(menu);
        frame.setVisible(true);
    }
/*
    public static void windowManager() {
        JFrame meinFrame = new JFrame("Image Timer 1.0");
        meinFrame.setDefaultCloseOperation(EXIT_ON_CLOSE);
        meinFrame.setSize(800, 800);
        JLabel header = new JLabel("Image Timer v1.0", CENTER);
        header.setVerticalAlignment(TOP);
        meinFrame.add(header);
        meinFrame.setVisible(true);
        //imageDisplay(args[0], Long.parseLong(args[1]));
    }

    public static void imageDisplay(String dir, long minutes) throws IOException, InterruptedException {
        boolean finished = false;
        Set<String> files = listFilesUsingJavaIO(dir);
        Random rand = new Random();

        while (!finished) {
            int size = files.size();
            if (size == 0) return;
            int random = 0;
            if (size > 1) random = rand.nextInt(size - 1);
            String image = (String) files.toArray()[random];
            Desktop.getDesktop().open(new File(dir + "\\" + image));
            if (files.isEmpty()) finished = true;
            files.remove(image);
            Thread.sleep(minutes * 60 * 1000);
        }
    }

    public static Set<String> listFilesUsingJavaIO(String dir) {
        System.out.print(dir);
        return Stream.of(new File(dir).listFiles())
                .filter(file -> !file.isDirectory())
                .map(File::getName)
                .collect(Collectors.toSet());
    }
 */
}
