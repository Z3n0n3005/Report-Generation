package report.generation.summarization;

public class Node {
    private String word;
    public String getWord() {
		return word;
	}
	public void setWord(String word) {
		this.word = word;
	}
	public Node() {
		super();
		// TODO Auto-generated constructor stub
	}
	public int getFreq() {
		return freq;
	}
	public Node(String word, int freq) {
		super();
		this.word = word;
		this.freq = freq;
	}
	public void setFreq(int freq) {
		this.freq = freq;
	}
	private int freq;
}
