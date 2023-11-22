package report.generation;

import org.grobid.core.*;
import org.grobid.core.data.*;
import org.grobid.core.factory.*;
import org.grobid.core.main.*;
import org.grobid.core.utilities.*;
import org.grobid.core.engines.Engine;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Arrays;

public class PdfSegmentation {
    public void pdfSegmenting() {
        // String pdfPath = "paper\\automatic-text-summarization-a-comprehensive-survey.pdf";
        String pdfPath = "paper/automatic-text-summarization-a-comprehensive-survey.pdf";
        String outputPath = "output/grobid-output.txt";
        try {
            // String pGrobidHome = "C:\\Users\\DELL\\Prototype\\grobid-0.7.3\\grobid-home";
            String pGrobidHome = "/media/vy/vy/prototype/grobid-0.7.3/grobid-home";
            // If the location is customised:
            GrobidHomeFinder grobidHomeFinder = new GrobidHomeFinder(Arrays.asList(pGrobidHome));

            // The grobid yaml config file needs to be instantiate using the correct
            // grobidHomeFinder or it will use the default
            // locations
            GrobidProperties.getInstance(grobidHomeFinder);

            System.out.println(">>>>>>>> GROBID_HOME=" + GrobidProperties.getGrobidHome());

            Engine engine = GrobidFactory.getInstance().createEngine();

            // Biblio object for the result
            BiblioItem resHeader = new BiblioItem();
            String tei = engine.processHeader(pdfPath, 1, resHeader);
            printToFile(tei, outputPath);
        } catch (Exception e) {
            // If an exception is generated, print a stack trace
            e.printStackTrace();
        }
    }

    private void printToFile(String text, String filepath){
        try{
            PrintWriter out = new PrintWriter(filepath);
            out.write(text);
            out.close();
        } catch(FileNotFoundException e){
            e.printStackTrace();
        }
    }
}
