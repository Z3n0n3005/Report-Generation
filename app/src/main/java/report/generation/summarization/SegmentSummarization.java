package report.generation.summarization;

import report.generation.segmentation.SectionList;

import java.io.IOException;
import java.util.ArrayList;

import report.generation.segmentation.Section;

public class SegmentSummarization {

    /**
     * Summarize all segments from the provided section list
     * @param pdfSegmentationList list of pdf segmentations
     * @param k number of sentence in each summary
     * @throws IOException
     */

    public static SectionList summarizeSegmentsLSA(SectionList pdfSegmentationList, int k) throws IOException{
        SectionList summaryList = new SectionList();
        ArrayList<Section> sectionList = pdfSegmentationList.getSectionList(); 

        // Set abstract summary
        String abstractStr = pdfSegmentationList.getAbstractSeg();
        String abstractSummary = LSA.summarize(abstractStr, k);
        summaryList.setAbstractSeg(abstractSummary);

        // Set summary of all sections
        for(Section section: sectionList){
            String sectionHeadStr = section.getHeader();
            String sectionContentStr = section.getContent();
            String sectionContentSummary = LSA.summarize(sectionContentStr, k);

            Section summarySection = new Section(sectionHeadStr, sectionContentSummary);
            summaryList.appendSectionList(summarySection);
        }
        
        return summaryList;
    }
}
