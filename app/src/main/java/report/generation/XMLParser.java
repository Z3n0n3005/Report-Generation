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
import java.util.ArrayList;

public class XMLParser {
    public static String paragraph;
    public static SectionList sectionList;

    public static SectionList parseXML(String filePath) {
        DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
        paragraph = "";
        sectionList = new SectionList();
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

            NodeList list = doc.getElementsByTagName("div");
            parseDiv(list);
        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }

        return sectionList;
    }

    private static void parseDiv(NodeList divList) {
        String currentHead = "";
        for (int i = 0; i < divList.getLength(); i++) {
            Node div = divList.item(i);
            if (div.getNodeType() == Node.ELEMENT_NODE) {
                Element divElement = (Element) div;
                NodeList headList = divElement.getElementsByTagName("head");
                NodeList pList = divElement.getElementsByTagName("p");
                String n = getNFromHead(headList);
                
                parseP(pList);

                if (n.length() < 3) {
                    boolean condCurrentHeadNotEmpty = !currentHead.isEmpty();
                    boolean condParagraphNotEmpty = !paragraph.isEmpty();

                    if(condCurrentHeadNotEmpty && condParagraphNotEmpty){
                        sectionList.appendSectionList(new Section(currentHead, paragraph));
                    }

                    currentHead = parseHead(headList);
                    paragraph = "";
                } else {
                }
            }
        }
    }

    private static String getNFromHead(NodeList headList) {
        String result = "0.";
        Node head = headList.item(0);

        if (head != null && head.getNodeType() == Node.ELEMENT_NODE) {
            Element headElement = (Element) head;
            if (headElement.hasAttribute("n")) {
                result = headElement.getAttribute("n");
            }
        }
        return result;
    }

    private static String parseHead(NodeList headList) {
        String result = "";
        Node head = headList.item(0);
        if (head != null && head.getNodeType() == Node.ELEMENT_NODE) {
            Element headElement = (Element) head;
            result = headElement.getTextContent();
        }
        return result;
    }

    private static void parseP(NodeList pList) {
        for (int i = 0; i < pList.getLength(); i++) {
            Node p = pList.item(i);
            if (p.getNodeType() == Node.ELEMENT_NODE) {
                Element pElement = (Element) p;
                String pContent = pElement.getTextContent();
                // System.out.println("[XMLParser] pContent " + pContent);
                paragraph += pContent;
            }
        }
    }

    public static String getParagraph() {
        return paragraph;
    }

    public static void setParagraph(String paragraph) {
        XMLParser.paragraph = paragraph;
    }

    public static SectionList getSectionList() {
        return sectionList;
    }

    public static void setSectionList(SectionList sectionList) {
        XMLParser.sectionList = sectionList;
    }
}
