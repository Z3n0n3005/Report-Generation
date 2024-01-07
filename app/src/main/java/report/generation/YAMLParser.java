package report.generation;

import java.io.File;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

import report.generation.segmentation.SectionList;

public class YAMLParser {
    public static SectionList parseYAML(String filePath) {
        // System.out.println("[YAMLParser] parseYAML");
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
        mapper.findAndRegisterModules();
        SectionList sectionList;

        try{
            sectionList = mapper.readValue(new File(filePath), SectionList.class);
            return sectionList;
        } catch(Exception e){
            e.printStackTrace();
        }

        return null;
    }
    
}
