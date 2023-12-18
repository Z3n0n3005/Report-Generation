package report.generation;

import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
import org.xml.sax.SAXException;

import report.generation.segmentation.Section;
import report.generation.segmentation.SectionList;

import javax.xml.XMLConstants;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import java.io.File;
import java.io.IOException;

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

            // Parse XML file
            DocumentBuilder db = dbf.newDocumentBuilder();

            Document doc = db.parse(new File(filePath));

            // optional, but recommended
            doc.getDocumentElement().normalize();

            // Get the NodeList
            NodeList abstractList = doc.getElementsByTagName("abstract");
            NodeList bodyList = doc.getElementsByTagName("div");

            // Parse the abstract
            System.out.println("[XMLParser] abstractList " + abstractList.getLength() + " " + abstractList.item(0).getNodeName());
            
            if (abstractList.getLength() > 1) { // Check if the list contain other tags
                parseAbstract(abstractList);
            } else {
                parseFirstDivInBodyAsAbstract(bodyList);
            }

            // Parse the body
            parseBody(bodyList);
        } catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }

        return sectionList;
    }

    private static void parseAbstract(NodeList abstractList) {
        String abstractSeg = "";

        // Get the div tag list from the <abstract> tag
        for (int i = 0; i < abstractList.getLength(); i++) {
            Node abstractNode = abstractList.item(i);
            if (abstractNode.getNodeType() != Node.ELEMENT_NODE) {
                break;
            }
            Element abstractElement = (Element) abstractNode;
            NodeList divList = abstractElement.getElementsByTagName("div");
            System.out.println("[XMLParser] divList " + divList);

            for (int j = 0; j < divList.getLength(); j++) {
                Node div = divList.item(j);
                if (div.getNodeType() != Node.ELEMENT_NODE) {
                    break;
                }
                Element divElement = (Element) div;
                NodeList pList = divElement.getElementsByTagName("p");
                System.out.println("[XMLParser] pList " + pList);

                for (int k = 0; k < pList.getLength(); k++) {
                    Node p = pList.item(k);
                    if (p.getNodeType() != Node.ELEMENT_NODE) {
                        break;
                    }
                    Element pElement = (Element) p;
                    String pContent = pElement.getTextContent();
                    System.out.println("[XMLParser] pContent " + pContent);
                    abstractSeg += pContent;

                }
            }
        }

        // if (divList == null) {
        // System.out.println("[XMLParser] divList is null");
        // return;
        // }

        // // Get the p tag list from the <div> tag
        // for (int j = 0; j < divList.getLength(); j++) {
        // Node div = divList.item(j);
        // if (div.getNodeType() == Node.ELEMENT_NODE) {
        // Element divElement = (Element) div;
        // pList = divElement.getElementsByTagName("p");
        // System.out.println("[XMLParser] pList " + pList);
        // }
        // }

        // if (pList == null) {
        // System.out.println("[XMLParser] pList is null");
        // return;
        // }

        // // Get the content of the <p> tag
        // for (int k = 0; k < pList.getLength(); k++) {
        // Node p = pList.item(k);
        // if (p.getNodeType() == Node.ELEMENT_NODE) {
        // Element pElement = (Element) p;
        // String pContent = pElement.getTextContent();
        // System.out.println("[XMLParser] pContent " + pContent);
        // abstractSeg += pContent;
        // }
        // }

        System.out.println("[XMLParser] abstractSeg " + abstractSeg);
        sectionList.setAbstractSeg(abstractSeg);
    }

    private static void parseFirstDivInBodyAsAbstract(NodeList divList) {
        String abstractSeg = "";
        Node div = divList.item(0);
        NodeList pList = null;
        if (div.getNodeType() != Node.ELEMENT_NODE) {
            return;
        }
        Element divElement = (Element) div;
        NodeList headList = divElement.getElementsByTagName("head");
        pList = divElement.getElementsByTagName("p");

        for (int k = 0; k < pList.getLength(); k++) {
            Node p = pList.item(k);
            if (p.getNodeType() != Node.ELEMENT_NODE) {
                break;
            }
            Element pElement = (Element) p;
            String pContent = pElement.getTextContent();
            System.out.println("[XMLParser] pContent " + pContent);
            abstractSeg += pContent;
        }

        // System.out.println("[XMLParser] abstractSeg " + abstractSeg);
        sectionList.setAbstractSeg(abstractSeg);
    }

    private static void parseBody(NodeList divList) {
        String currentHead = "";
        for (int i = 0; i < divList.getLength(); i++) {
            Node div = divList.item(i);
            if (div.getNodeType() == Node.ELEMENT_NODE) {
                Element divElement = (Element) div;
                NodeList headList = divElement.getElementsByTagName("head");
                NodeList pList = divElement.getElementsByTagName("p");

                // Get the content of the <head> tag
                currentHead = parseHead(headList);

                // Get the n attribute from the current <head> tag
                String n = getNFromHead(headList);

                // Add the content of the <p> tag to the paragraph
                parseP(pList);

                if (n.isEmpty()) { // Check if this head has no n attribute
                    // Reset the current paragraph
                    paragraph = "";
                } else if (n.length() < 3) {// Check if this is a new section
                    boolean condCurrentHeadNotEmpty = !currentHead.isEmpty();
                    boolean condParagraphNotEmpty = !paragraph.isEmpty();

                    // Save the paragraph to the section list
                    if (condCurrentHeadNotEmpty && condParagraphNotEmpty) {
                        sectionList.appendSectionList(new Section(currentHead, paragraph));
                    }
                    // Reset the current paragraph
                    paragraph = "";
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
            } else {
                result = "";
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
