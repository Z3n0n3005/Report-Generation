package report.generation;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;

public class XMLParser {
    public static String paragraph = "";
    public static void parseXML(String filePath){
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();

        try {

            // optional, but recommended
            // process XML securely, avoid attacks like XML External Entities (XXE)
            dbf.setFeature(XMLConstants.FEATURE_SECURE_PROCESSING, true);

            // parse XML file
            DocumentBuilder db = dbf.newDocumentBuilder();

            Document doc = db.parse(new File(filePath));

            // optional, but recommended
            // http://stackoverflow.com/questions/13786607/normalization-in-dom-parsing-with-java-how-does-it-work
            doc.getDocumentElement().normalize();

            System.out.println("------");
            System.out.println("Root Element :" + doc.getDocumentElement().getNodeName());
            System.out.println("------");

            // get <staff>
            NodeList list = doc.getElementsByTagName("div");
            parseDiv(list);

            System.out.println(paragraph);
        }
        catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }
    }

    private static void parseDiv(NodeList divList){
        for(int i = 0; i < divList.getLength(); i++){
            Node div = divList.item(i);
            if(div.getNodeType() == Node.ELEMENT_NODE){
                Element divElement = (Element) div;
                String xmlns = divElement.getAttribute("xmlns");
                // System.out.println("[XMLParser] xmlns=" + xmlns);
                NodeList childList = divElement.getElementsByTagName("head");
                parseHead(childList);
            }
        }
    }

    private static void parseHead(NodeList headList){
        for(int i = 0; i < headList.getLength(); i++){
            Node head = headList.item(i);
            if(head.getNodeType() == Node.ELEMENT_NODE){
                Element headElement = (Element) head;
                if(headElement.hasAttribute("n")){
                    String n = headElement.getAttribute("n");
                    // System.out.println("[XMLParser] n=" + n);
                }
                NodeList childList = headElement.getElementsByTagName("p");
                childList = headElement.getChildNodes();
                // headElement.
                System.out.println("[XMLParser] childList length " + childList.item(0).getTextContent());
                parseP(childList);
            }
        }
    }

    private static void parseP(NodeList pList){
        for(int i = 0; i < pList.getLength(); i++){
            Node p = pList.item(i);
            if(p.getNodeType() == Node.ELEMENT_NODE){
                Element pElement = (Element) p;
                String pContent = pElement.getTextContent();
                System.out.println("[XMLParser] pContent " + pContent);
                paragraph += pContent; 
            }
        }
    }
}
