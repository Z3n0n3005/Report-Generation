/*
 * This Java source file was generated by the Gradle 'init' task.
 */
package report.generation;

import java.util.ArrayList;

public class App {
    static String pdfPath = "paper/automatic-text-summarization-a-comprehensive-survey.pdf";
    static String pdfSegOutputPath = "output/grobid-output.xml";
    static String xmlParseOutputPath = "output/xml-parse-output.yaml";

    public static void main(String[] args) {
        System.out.println("[App] Start timing");
        long startTime = System.nanoTime();
        
        // Engine generation
        PdfSegmentation.generateEngine();

        long engineGenerationEndTime = System.nanoTime();
        double engineGenerationTime = (engineGenerationEndTime - startTime)/1000000;
        System.out.println("[App] Engine generation time: " + engineGenerationTime );
        
        // PDF Segmenation
        String pdfSegResult = PdfSegmentation.pdfSegmenting(pdfPath);
        Utility.printToFile(pdfSegResult, pdfSegOutputPath);

        long pdfSegEndTime = System.nanoTime();
        double pdfSegTime = (pdfSegEndTime - engineGenerationEndTime)/1000000;
        System.out.println("[App] First PDF Segmentation time = " + pdfSegTime);

        String secondPdfSegResult = PdfSegmentation.pdfSegmenting(pdfPath);
        long secondPdfSegEndTime = System.nanoTime();
        double secondPdfSegTime = (secondPdfSegEndTime - pdfSegEndTime)/1000000;
        System.out.println("[App] Second PDF Segmentation time = " + secondPdfSegTime);

        //XML Parsing
        SectionList xmlParseResult = XMLParser.parseXML(pdfSegOutputPath);
        Utility.printToYamlFile(xmlParseResult, xmlParseOutputPath);

        long endTime = System.nanoTime();
        double totalTime = (endTime - startTime)/1000000;
        System.out.println("[App] Time elapsed = " + totalTime);
    }
}
