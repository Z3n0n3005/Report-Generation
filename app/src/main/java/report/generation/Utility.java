package report.generation;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Map;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.annotation.JsonFormat.Feature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class Utility {
    public static void printToFile(String text, String filepath){
        try{
            PrintWriter out = new PrintWriter(filepath);
            out.append(text);
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
    
    public static List<String> readFileAsList (File file) {
		ArrayList<String> list = new ArrayList<>();
		try (FileReader f = new FileReader(file)){
			StringBuffer sb = new StringBuffer();
			while (f.ready()) {
				char c = (char) f.read();
				if (c == '\n') {
					list.add(sb.toString());
					sb = new StringBuffer();
				} else sb.append(c);
			    if (sb.length() > 0) {
			        list.add(sb.toString());
			    }
			}
		} catch (Exception e) {
			e.printStackTrace();
		}
		return list;
	}
	
    public void toFile(String text) throws IOException {
        File output = new File("./ngram.txt");
        if (output.exists()) {
        	output.delete();
            FileWriter write = new FileWriter("./ngram.txt");
            write.write(text);
            write.close();
        } else {
            FileWriter write = new FileWriter("./ngram.txt");
            write.write(text);
            write.close();
        }

    }

	
	public static String readFile(File file) throws IOException {
		String text = "";
		Scanner scan = new Scanner(file);
		while(scan.hasNextLine()) {
			text += scan.nextLine()+"\n";
		}
		return text;
	}
}