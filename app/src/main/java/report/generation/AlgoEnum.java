package report.generation;

public enum AlgoEnum {
    LSA("lsa"),
    TEXTRANK("textrank");
    
    public final String algo;

    private AlgoEnum(String algo){
        this.algo = algo;
    }

    public static AlgoEnum getCurrentAlgo(){
        String currentAlgo = System.getProperty("algo");
        // System.out.println("[AlgoEnum] currentAlgo: " + currentAlgo);
        
        for(AlgoEnum a : values()){
            if(a.algo.equals(currentAlgo)){
                return a;
            }
        }
        return null;
    }
}
