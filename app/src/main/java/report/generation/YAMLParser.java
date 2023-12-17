package report.generation;

import java.io.File;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public interface YAMLParser {
    public static SectionList parseYAML(String filePath) {
        System.out.println("[YAMLParser] parseYAML");
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());
        mapper.findAndRegisterModules();
        SectionList sectionList;

        try{
            sectionList = mapper.readValue(new File(filePath), SectionList.class);
            // System.out.println("[YAMLParser] sectionList: " + sectionList.toString());
            return sectionList;
        } catch(Exception e){
            e.printStackTrace();
        }

        return null;
    }
    
}
