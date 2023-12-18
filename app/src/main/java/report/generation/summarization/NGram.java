package report.generation.summarization;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import opennlp.tools.ngram.NGramModel;
import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.tokenize.SimpleTokenizer;
import opennlp.tools.util.StringList;

import report.generation.util.Utility;

public class NGram {
	File stopwordFile = new File("./build/resources/stopwords.txt");
	// File modelFile = new File("../models/en-sent.bin");
    File modelFile = new File("../models/opennlp-en-ud-ewt-sentence-1.0-1.9.3.bin");
    private NGramModel model;
    private String[] sentences;
    private String text;
    private Map<String, Integer> map = new HashMap<>();
    private List<Node> list;
    private List<String> sorted;
    private String test = "";

    public File getStopwordFile() {
		return stopwordFile;
	}

	public void setStopwordFile(File stopwordFile) {
		this.stopwordFile = stopwordFile;
	}

	public File getModelFile() {
		return modelFile;
	}

	public void setModelFile(File modelFile) {
		this.modelFile = modelFile;
	}

	public NGramModel getModel() {
		return model;
	}

	public void setModel(NGramModel model) {
		this.model = model;
	}

	public String[] getSentences() {
		return sentences;
	}

	public void setSentences(String[] sentences) {
		this.sentences = sentences;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Map<String, Integer> getMap() {
		return map;
	}

	public void setMap(Map<String, Integer> map) {
		this.map = map;
	}

	public List<Node> getList() {
		return list;
	}

	public void setList(List<Node> list) {
		this.list = list;
	}

	public List<String> getSorted() {
		return sorted;
	}

	public void setSorted(List<String> sorted) {
		this.sorted = sorted;
	}

	public String getTest() {
		return test;
	}

	public void setTest(String test) {
		this.test = test;
	}

	/**
     * This method is to break the whole document into set of token (words)
     * In this step, it is necessary to remove all punctuation by using replaceAll()
     * @param text is the input text from the text area in View
     * @return the list of word defined in StringList in OpenNLP
     */
    public StringList tokenize(String text) {
    	this.test = text.replaceAll("\\p{Punct}", "");
    	StringList list = new StringList(SimpleTokenizer.INSTANCE.tokenize(this.test));
    	return list;
    }
    
    /**
     * This method is to generate NGram model for doing counting frequency of each token
     * @param list is the return of the tokenize() step above
     * @param min is the minimum number of n-gram
     * @param max is the maximum of n-gram
     */
    public void generate(StringList list, int min, int max) {
        this.model = new NGramModel();
        this.model.add(list, min, max);
    }

    public void generate(StringList list, int num) {
        this.model = new NGramModel();
        this.model.add(list, num, num);
        // print();
    }

    public void print() {
        System.out.println("Total ngrams: " + this.model.numberOfGrams());
        for (StringList ngram : this.model) {
            System.out.println(this.model.getCount(ngram) + " - " + ngram);
        }
    }

    /**
     * This method is to sort the tokens based on its frequency in descending order
     */
    public void sort() {

        Collections.sort(this.list, (a,b) -> b.getFreq() - a.getFreq());
        this.sorted = new ArrayList<>();
        for (Node node : this.list) {
            this.sorted.add(node.getWord().replace("[", "").replace("]", ""));
        }
        // printList();

    }

    public void printList() {
        for (Node node : this.list) {
            System.out.println(node.getFreq() + " - " + node.getWord());
        }
    }
    
    /**
     * This method is to remove all stop words identified by the stop word list
     * @throws IOException
     */
    public void filterStopWords() throws IOException {
    	File file = stopwordFile;
        this.list = new ArrayList<>();
        for (StringList gram : this.model) {
            this.list.add(new Node(gram.getToken(0),this.model.getCount(gram)));
        }
        List<String> stopwords = Utility.readFileAsList(file);
        
        for (String word : stopwords){
            for (int i = 0; i<this.list.size();i++){
                Node node = this.list.get(i);
                if (node.getWord().equals(word)){
                    // System.out.print(word + " ");
                    this.list.remove(node);
                }
            }
        }
    }

    /**
     * This method is to break the whole text into list of sentences
     * @return the list of sentences 
     * @throws IOException
     */
    public void getSentenceUsingModel(String text) throws IOException {
        File modelfile = modelFile;
    	this.text = text.replaceAll("([A-Z])\\.", "$1");

        InputStream is = new FileInputStream(modelfile);
        SentenceModel model = new SentenceModel(is);

        SentenceDetectorME sd = new SentenceDetectorME(model);

        this.sentences = sd.sentDetect(this.text);
    }
    
    public void printSentence(){
        for(String sentence: sentences){
            System.out.println(sentence);
        }
    }

    /**
     * This method is to search the presentation of the word in sentence
     * @param word
     * @return the sentence that match the word
     */
    public String search(String word) {
        String firstMatchSentence = null;
        for (int i = 0; i < this.sentences.length; i++) {
            if (this.sentences[i].contains(word)) {
            	firstMatchSentence = this.sentences[i];
            }
        }
        return firstMatchSentence;
    }
    
    /**
     * This method to count number of word which appear in sentence
     * @param word: got from sorted token list
     * @param sentence: got from list of sentences
     * @return the frequency of word in sentence
     */
    public int countWords(String word, String sentence){
        int count = 0;
        String[] words = sentence.split("\\s+");
        for (String i : words){
            if (word.equals(i)){
                count++;
                
            }
        }
        return count;
    }

}



