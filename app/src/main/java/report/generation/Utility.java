package report.generation;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.util.Map;
import java.util.ArrayList;

import com.fasterxml.jackson.annotation.JsonFormat.Feature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class Utility {
    public static void printToFile(String text, String filepath){
        try{
            PrintWriter out = new PrintWriter(filepath);
            out.write(text);
            out.close();
        } catch(FileNotFoundException e){
            e.printStackTrace();
        }
    }

    public static void printToYamlFile(SectionList sectionList, String filepath){
        ObjectMapper mapper = new ObjectMapper(new YAMLFactory());        
        mapper.findAndRegisterModules(); 
        // mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        // mapper = new ObjectMapper(new YAMLFactory().disable(Feature.WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS));
        try{
            mapper.writeValue(new File(filepath), sectionList);
        } catch(Exception e){
            e.printStackTrace();
        }
        
        // String result = "";

        // try{
        //     PrintWriter out = new PrintWriter(filepath);
        //     out.write(result);
        //     out.close();
        // } catch(FileNotFoundException e){
        //     e.printStackTrace();
        // }
    }
}