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
            NodeList list = doc.getElementsByTagName("author");
            System.out.println("[XMLParser] list: " + list);
            for (int temp = 0; temp < list.getLength(); temp++) {

                Node node = list.item(temp);
                System.out.println("[XMLParser] temp: " + temp);
                System.out.println("[XMLParser] node: " + node);
                if (node.getNodeType() == Node.ELEMENT_NODE) {

                    Element element = (Element) node;
                    String forename = element.getAttribute("forename");
                    System.out.println("[XMLParser] forename: " + forename);
                    // get staff's attribute
                    // String id = element.getAttribute("id");

                    // // get text
                    // String firstname = element.getElementsByTagName("firstname").item(0).getTextContent();
                    // String lastname = element.getElementsByTagName("lastname").item(0).getTextContent();
                    // String nickname = element.getElementsByTagName("nickname").item(0).getTextContent();

                    // NodeList salaryNodeList = element.getElementsByTagName("salary");
                    // String salary = salaryNodeList.item(0).getTextContent();

                    // // get salary's attribute
                    // String currency = salaryNodeList.item(0).getAttributes().getNamedItem("currency").getTextContent();

                    // System.out.println("Current Element :" + node.getNodeName());
                    // System.out.println("Staff Id : " + id);
                    // System.out.println("First Name : " + firstname);
                    // System.out.println("Last Name : " + lastname);
                    // System.out.println("Nick Name : " + nickname);
                    // System.out.printf("Salary [Currency] : %,.2f [%s]%n%n", Float.parseFloat(salary), currency);

                }
            }
        }
        catch (ParserConfigurationException | SAXException | IOException e) {
            e.printStackTrace();
        }
    }
}
