package report.generation;

import org.grobid.core.*;
import org.grobid.core.analyzers.GrobidAnalyzer;
import org.grobid.core.data.*;
import org.grobid.core.document.Document;
import org.grobid.core.document.DocumentSource;
import org.grobid.core.factory.*;
import org.grobid.core.main.*;
import org.grobid.core.utilities.*;
import org.grobid.core.engines.*;
import org.grobid.core.engines.config.GrobidAnalysisConfig;
import org.grobid.core.engines.config.GrobidAnalysisConfig.GrobidAnalysisConfigBuilder;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Arrays;

public class PdfSegmentation {
    private static Engine engine;
    private static GrobidAnalyzer analyzer;
    private static GrobidAnalysisConfig analysisConfig;

    public static String pdfSegmenting(String pdfPath) {
        String result;
        String tei = "";
        // Biblio object for the result
        try {
            //Have been found to can be speed up using multithreading, might learn GNU parallel
            tei = engine.fullTextToTEI(new File(pdfPath), analysisConfig);
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        result = tei;
        // System.out.println("tei: " + tei);

        return result;
    }
    
    public static String parseHeader(String pdfPath){
        BiblioItem resultBib; 
        Document resultDoc;
        String result = "";
        try {
            //Have been found to can be speed up using multithreading, might learn GNU parallel
            DocumentSource docummentSource = DocumentSource.fromPdf(new File(pdfPath));
            Document document = new Document(docummentSource); 

            result = engine.getAbstract(document);
            // engine.getParsers().getHeaderParser();
            
            // result = engine.processHeader(pdfPath, analysisConfig, null);
            // result = engine.getAbstract(resultDoc);
            result = "<abstract>" + result + "</abstract>";
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        return result;
    }

    public static void generateEngine(){
        if(engine == null){
            try {
                // String pGrobidHome = "C:\\Users\\DELL\\Prototype\\grobid-0.7.3\\grobid-home";
                String pGrobidHome = "lib/grobid-0.7.3/grobid-home";

                // If the location is customised:
                GrobidHomeFinder grobidHomeFinder = new GrobidHomeFinder(Arrays.asList(pGrobidHome));

                // The grobid yaml config file needs to be instantiate using the correct
                // grobidHomeFinder or it will use the default
                // locations
                GrobidProperties.getInstance(grobidHomeFinder);

                System.out.println("[PdfSegmentation] >>>>>>>> GROBID_HOME=" + GrobidProperties.getGrobidHome());

                engine = GrobidFactory.getInstance().createEngine(true);
                // engine = GrobidFactory.getInstance().createEngine(false);
                analyzer = GrobidAnalyzer.getInstance();
                

                // analysisConfig = GrobidAnalysisConfig.defaultInstance();
                analysisConfig = GrobidAnalysisConfig.builder()    
                    .withSentenceSegmentation(false)
                    .withPreprocessImages(false)
                    .withProcessVectorGraphics(false)
                    // .consolidateCitations(10)
                    // .consolidateHeader(10)
                    .build();
                // analysisConfig = GrobidAnalysisConfig
                
            } catch (Exception e) {
                // If an exception is generated, print a stack trace
                e.printStackTrace();
            }
        }
    }
}
