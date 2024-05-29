import time
import tasks.xml_parser as xml_parser

def main():
    start = time.time()

    xml_parser.parse_xml_folder()
    # s_papers = summary.summarize_folder(
    #     papers,
    #     summary.PreProcessAlgo.NONE.value, 
    #     summary.SumAlgo.TEXTRANK.value
    # )
    end = time.time()
    print(end - start)

if __name__ == "__main__":
    main()