package report.generation.segmentation;

import java.util.ArrayList;

public class SectionList {
    public String abstractSeg;
    public ArrayList<Section> sectionList;

    public SectionList(){
        sectionList = new ArrayList<>();
    }

    public void appendSectionList(Section section){
        this.sectionList.add(section);
    }

    public void setAbstractSeg(String abstractSeg){
        this.abstractSeg = abstractSeg;
    }

    public String toString(){
        String result = "";
        result += "Abstract: " + abstractSeg + "\n";
        for(Section section : sectionList){
            result += "Header: " + section.header + "\n";
            result += "Content: " + section.content + "\n";
        }
        return result;
    }
    
    public ArrayList<Section> getSectionList(){
        return sectionList;
    }

    public Section getSection(int index){
        return getSectionList().get(index);
    }

    public String getAbstractSeg(){
        return abstractSeg;
    }

}
