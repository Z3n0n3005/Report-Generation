package report.generation.segmentation;

public class Section {
    public String header; 
    public String content;

    public Section(String header, String content){
        this.header = header;
        this.content = content;
    }

    public Section(){
        super();
    }

    public String getHeader(){
        return header;
    }

    public String getContent(){
        return content;
    }
}
