# Report-Generation  
Note: The current project can only be run in a Linux environment due to problem with GPU drivers.  
[![Using Zotero Plugin Template](https://img.shields.io/badge/Using-Zotero%20Plugin%20Template-blue?style=flat-square&logo=github)](https://github.com/windingwind/zotero-plugin-template)
## How to use  
1. Set the current directory to be ```./Report-Generation```
2. Depending on the your needs.   
2.1. If you have a path to a paper, then ```./report-gen.sh -f [path-to-pdf] -a [lsa | textrank]```  
2.2. If you want to convert the whole folder, then ```./report-gen.sh - [path-to-folder] -a [lsa | textrank]```  
3. Get result in the ```./output``` folder

## Example
```
./report-gen.sh -f paper -a lsa
```
