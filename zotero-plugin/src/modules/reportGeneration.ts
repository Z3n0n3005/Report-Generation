
import { UITool, TagElementProps } from "zotero-plugin-toolkit/dist/tools/ui";
// import * as async from 'async'
// import * as path from 'path'
// import * as fs from 'node:fs'
import { platform } from "node:os";
// import * as mkdirp from 'mkdirp'
// import * as sleep from 'sleep'
import * as fs from 'node:fs'
import { pathToFileURL } from "node:url";

function reportGen(
  target: any,
  propertyKey: string | symbol,
  descriptor: PropertyDescriptor,
) {
  const original = descriptor.value;
  descriptor.value = function (...args: any) {
    try {
      ztoolkit.log(`Calling report gen function ${target.name}.${String(propertyKey)}`);
      return original.apply(this, args);
    } catch (e) {
      ztoolkit.log(`Error in report gen function ${target.name}.${String(propertyKey)}`, e);
      throw e;
    }
  };
  return descriptor;
}

export class ReportGenerationFactory{
    @reportGen
    private static generateSummaries() { 
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        ztoolkit.log("[ReportGen] selectedItemsLength: " + sortedItems.length)
        
        // this.setSummarizeButton()
        const pathList = []
        for (let index = 0; index < sortedItems.length; index++) {
            ztoolkit.log("[ReportGen] index: " + index + " " + sortedItems.length)
            const item = sortedItems[index];
            const pdfFilePath = this.getFilePath(item)
            
            // if could not get file path
            if(!pdfFilePath){ continue }
            pathList.push(<string>pdfFilePath)
        }
        ReportGenerationFactory.summarize(pathList)

    }

    @reportGen
    private static getFilePath(item:Zotero.Item):string|boolean{
        ztoolkit.log("[ReportGen] isRegualarItem: " + item.isRegularItem())
        // if the item is not a pdf
        if(!item.isRegularItem()){ return false }

        ztoolkit.log("[ReportGen] hasSummaryNote: " + this.hasSummaryNote(item))
        // if item already has a summary note
        if(this.hasSummaryNote(item)){ return false }

        const pdfFilePath = this.getPDFFilePath(item)
        // ztoolkit.log("[ReportGen] pdfFilePath: " + pdfFilePath)
        // if could not get file path
        if(!pdfFilePath){ return false }
        return pdfFilePath
    }

    @reportGen
    private static hasSummaryNote(item:Zotero.Item):boolean{
        // ztoolkit.log(DebugReportGen + "isNote: " + item.isNote() + ", itemName: " + item.getDisplayTitle())
        const noteIDs = item.getNotes()
        // ztoolkit.log(noteIDs)
        for (let noteIndex = 0; noteIndex < noteIDs.length; noteIndex++){
            const noteID = noteIDs.at(noteIndex);
            if(noteID === undefined){
                continue;
            }
            const note = Zotero.Items.get(noteID);
            const noteTitle = note.getNoteTitle()
            ztoolkit.log("[ReportGen] " + noteTitle);
            if(noteTitle === NoteTitle){
                return true
            }
        }
        return false
    }

    @reportGen
    private static hasPDFAttachment(item:Zotero.Item):boolean{
        const attachmentIDs = item.getAttachments()
        ztoolkit.log(attachmentIDs)
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            const attachmentID = attachmentIDs.at(attachmentIndex);
            if(attachmentID === undefined){ continue; }

            const attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){ return true }
        }

        return false
    }

    @reportGen
    private static getPDFFilePath(item:Zotero.Item):string|false{
        ztoolkit.log("userID: " + Zotero.Users.getCurrentUserID())
        ztoolkit.log("itemID: " + item.key)
        const attachmentIDs = item.getAttachments()
        ztoolkit.log(attachmentIDs)
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            const attachmentID = attachmentIDs.at(attachmentIndex);
            if(attachmentID === undefined){ continue; }

            const attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){ continue; }

            const filePath = attachment.getFilePath()
            const filePathURL = attachment.getLocalFileURL()
            if(filePath){ return filePathURL }
            // ztoolkit.log("[ReportGen] filePath in folder: " + filePath + " " + !filePath)
        }
        return false
    }

    // This method is currently under construction, might not even work at all
    @reportGen
    private static summarize(pathList:string[]){
        // for(let i = 0; i < pathList.length; i++){
            // const path = pathList[i]
            const path = pathList[0]
            const contentFromURL = Zotero.File.getContentsFromURL(path)
            const resource = Zotero.File.getResource(path)
            const diff = (diffMe:string, diffBy:string) => diffMe.split(diffBy).join('')
            // const diffRes = diff(contentFromURL, resource)
            // this.logToNote("resource: " + diffRes)
            // normal stuffs
            // const pdfFile = new File(
            //     [pdfFileContent], 
            //     this.getFileName(path),
            //     {
            //         type: 'application/pdf'
            //     }
            // )
            // ztoolkit.log("filePath: " + this.getFileName(path))
            // this.sendPdfFilesAsync(pdfFile)
            // .then(result => {
            //     if(!result){ return false}
            //     return this.getSummaryResult()
            // })
            // .then(result => {
            //     ztoolkit.log("Summary result: " + result)

            // })
            // fs.readFile(path, (res) => {
            //     ztoolkit.log(res)
                
            // })
            // async stuffs
            Zotero.File.getBinaryContentsAsync(path)
            .then(res => {
                this.logToNote(diff(res, resource))
                return new File(
                    [res],
                    this.getFileName(path),
                    {
                        type: 'application/pdf'
                    }
                )
            })
            .then(res => {
                // ztoolkit.log("formdata: " + res.name)
                return this.sendPdfFilesAsync(res)
            })
            .then(res => {
                if(!res){ return false}
                return this.getSummaryResult()
            })
            .then(res => {
                ztoolkit.log("Summary result: " + res)
            })
            
        // }
    }

    @reportGen
    private static logToNote(content:string){
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        
        // this.setSummarizeButton()
        const standAloneNote = sortedItems[0]
        standAloneNote.setNote(content)
        // standAloneNote
        // for (let index = 0; index < sortedItems.length; index++) {
        //     ztoolkit.log("[ReportGen] index: " + index + " " + sortedItems.length)
        //     const item = sortedItems[index];
        //     const pdfFilePath = this.getFilePath(item)
            
        //     // if could not get file path
        //     if(!pdfFilePath){ continue }
        // }
    }

    @reportGen
    private static getFileName(path:string){
        return path.replace(/^.*(\\|\/|\:)/, '')
    }

    @reportGen
    private static async sendPdfFilesAsync(file: File):Promise<boolean>{
        const urlBase = "http://127.0.0.1:5000"
        const urlUpload = "/upload"
        const urlSummarize = "/summarize"
        // if(!files.length){
        //     ztoolkit.log('Error: No PDF files selected')
        // }

        const formData = new window.FormData()
        ztoolkit.log(formData)
        
        if(!file.type.startsWith('application/pdf')){
            throw new Error("Invalid file type: ${file.name}.")
        }

        formData.append('files', file)

        try {
            const response = await fetch(urlBase + urlUpload, {
                method: 'POST', 
                body: formData, 
            });

            if(!response.ok){
                return false
            }
            return true
        }
        catch(error){
            throw error
        }

    }

    @reportGen
    private static async getSummaryResult():Promise<any>{
        const urlBase = "http://127.0.0.1:5000"
        const urlUpload = "/upload"
        const urlSummarize = "/summarize"

        try{
            const response = await fetch(urlBase + urlSummarize, 
                {
                    method: 'POST'
                }
            )
            const result = await response.json()
            ztoolkit.log("result: " + result)
            return result
        } catch(error){
            throw error
        }
    }

    @reportGen
    private static getSummaryHTML(filePath:string):string{
        var result = ""
        // const child = spawn(ReportGenPath, [
        //     "--filePath", 
        //     filePath,
        //     "-a", 
        //     "textrank"
        // ])
        return result
    }

    @reportGen
    private static addSummaryNote(item:Zotero.Item){
        const htmlPrefix = "<div data-schema-version=\"8\">";
        const htmlSufix = "</div>"
        const htmlNoteTitle = "<p>" + NoteTitle + "<\p>";
        var htmlContent = "<p><strong>Hi</strong></p>"
        const htmlFinal = htmlPrefix + htmlNoteTitle + htmlContent + htmlSufix
        item.setNote(htmlFinal)
    }

    @reportGen
    private static unregisterNotifier(notifierID: string) {
        Zotero.Notifier.unregisterObserver(notifierID);
    }

    @reportGen
    public static registerSummarizeButton(){
        const toolbarNode = document.getElementById("zotero-items-toolbar")

        const childNodes = toolbarNode?.children
        if(childNodes === undefined){ return }

        const firstNode = childNodes.item(0) 
        if(firstNode === null){ return }

        const tbSummaryNoteAdd = ztoolkit.UI.insertElementBefore({ 
            tag: 'toolbarbutton',
            id: 'zotero-tb-summary-note', 
            classList: ['zotero-tb-button'],
            attributes: {
                'tabindex':-1,
                'tooltiptext':'Add summary notes',
                'type':'panel'
            },
            listeners: [
                {
                  type: "click",
                  listener: () => {
                    this.generateSummaries()
                  },
                },
              ],
        }, firstNode)

        if(tbSummaryNoteAdd === undefined){ return }
        
        // Set label of button
        const childrenNodeSummaryNoteAdd = tbSummaryNoteAdd?.children
        if(childrenNodeSummaryNoteAdd === undefined){ return }

        const labelSummaryNoteAdd = <HTMLElement>childrenNodeSummaryNoteAdd.item(1)
        if(labelSummaryNoteAdd === undefined){ return }

        labelSummaryNoteAdd.innerHTML = "📖"
    }
}