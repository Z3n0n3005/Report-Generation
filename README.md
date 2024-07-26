# Report-Generation  
  
[![Using Zotero Plugin Template](https://img.shields.io/badge/Using-Zotero%20Plugin%20Template-blue?style=flat-square&logo=github)](https://github.com/windingwind/zotero-plugin-template)
## How to use  
1. Set the current directory to be ```./Report-Generation/docker```
2. Open the terminal in the current directory.
3. Run ```docker compose up```.
4. Access your localhost on port 5000.
5. Choose a pre-processing method, and a summarization method.
6. Upload a PDF file.
7. Obtain the result

## Machine Environment for Benchmarking
|Component|Detail                                        |
|---------|----------------------------------------------|
|CPU      |Ryzen 5 5500                                  |  
|RAM      |16GB                                          |
|GPU      |None was used to emulate a laptop environment.|

## List of libraries used  
- grobid-client-python  
- requests  
- flask[async]  
- redis  
- werkzeug  
- summa  
- pyzotero  
- asyncio  
- accelerate  
- nltk  
- numpy  
- transformers  
- torch  
