package report.generation.summarization;

import opennlp.tools.util.StringList;
import org.apache.commons.math3.linear.MatrixUtils;
import org.apache.commons.math3.linear.RealMatrix;
import org.apache.commons.math3.linear.SingularValueDecomposition;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class LSA {
    public static double maxEntry(RealMatrix mat) {
        double max = mat.getEntry(0, 0);
        for (int i = 0; i < mat.getRowDimension(); i++) {
            for (int k = 0; k < mat.getColumnDimension(); k++) {
                if (max < mat.getEntry(i, k)) {
                    max = mat.getEntry(i, k);
                }
            }
        }
        return max;
    }

    public static void printMat(RealMatrix mat) {
        for (int i = 0; i < mat.getRowDimension(); i++) {
            for (int k = 0; k < mat.getColumnDimension(); k++) {
                System.out.printf("%9.3f", mat.getEntry(i, k));
            }
            System.out.println();
        }
    }

    /**
     * Summarize the provided text using LSA
     * @param text that needs to be summarized
     * @param k the number of sentences
     * @return the summary of text
     */
    public static String summarize(String text, int k) throws IOException {
        String summary = "";
        NGram ngram = new NGram();
        StringList list = ngram.tokenize(text);
        ngram.generate(list, 1);
        // ngram.printList();
        ngram.filterStopWords();
        // ngram.printList();
        ngram.sort();
        // ngram.printList();
        ngram.getSentenceUsingModel(text);
        // ngram.printSentence();

        // Check if the number of sentence of the provided text 
        // is not shorter than k 
        if(ngram.getSentences().length <= k){
            for (String sentence : ngram.getSentences()) {
                summary = summary.concat(" ").concat(sentence).trim();
            }

            return summary;
        } 

        Matrix docMat = new Matrix(ngram.getList().size(), ngram.getSentences().length);
    

        for (Node node : ngram.getList()) {
            for (int i = 0; i < ngram.getSentences().length; i++) {
                docMat.add(ngram.getList().indexOf(node), i, ngram.countWords(node.getWord(), ngram.getSentences()[i]));
            }
        }

        // docMat.show();

        //Create RealMatrix
        RealMatrix mat = MatrixUtils.createRealMatrix(docMat.data);
        SingularValueDecomposition svd = new SingularValueDecomposition(mat);
        //Calculate diagonal matrix Σ (m * n)
        RealMatrix S = svd.getS();
        //Calculate transpose of orthogonal matrix V (n * n)
        RealMatrix VT = svd.getVT();
        //Calculate sub matrix of transpose of V (k * n)
        RealMatrix Vp = VT.getSubMatrix(0, k, 0, VT.getColumnDimension() - 1);
        //Calculate sub matrix of Σ (k * k)
        RealMatrix Sp = S.getSubMatrix(0, k, 0, k);
        //Calculate the topic similarity = Σ (k * k) * V (k * n)
        RealMatrix Ap = Sp.multiply(Vp);
        List<String> setSummarySentences = new ArrayList<String>();

        // System.out.println("[LSA] max entry AP: " + maxEntry(Ap));
        // System.out.println("[LSA]");

        for (int i = 0; i <= Ap.getRowDimension() - 1; i++) {
            for (int j = 0; j <= Ap.getColumnDimension() - 1; j++) {
                if (Ap.getEntry(i, j) >= maxEntry(Ap) / 2.5 && !setSummarySentences.contains(ngram.getSentences()[j])) {
                    setSummarySentences.add(ngram.getSentences()[j]);
                }
                if (setSummarySentences.size() == k) {
                    // System.out.println("[LSA] Has reached sentence number limit");
                    break;
                }
            }
        }
        // System.out.println(setSummarySentences);
        for (String string : setSummarySentences) {
            summary = summary.concat(" ").concat(string).trim();
        }
        return summary;
    }
}