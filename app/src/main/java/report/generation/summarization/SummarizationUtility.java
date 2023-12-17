package report.generation.summarization;

import opennlp.tools.tokenize.SimpleTokenizer;
import opennlp.tools.util.StringList;

public class SummarizationUtility {
    public static StringList tokenize(String text) {
        text = text.replaceAll("\\p{Punct}", "");
        StringList list = new StringList(SimpleTokenizer.INSTANCE.tokenize(text));
        return list;
    }
}
