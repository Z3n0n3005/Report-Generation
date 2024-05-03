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
    static readonly API_KEY = "IqssCl6uXkPQqcMP6y52Enj2"
    static readonly LIBRARY_ID = "14142718"
    static readonly LIBRARY_TYPE = "user"
    static readonly ITEM_KEY = "SNXV9A8F"
    static readonly IP_LOCAL_HOST = "127.0.0.1"
    static readonly IP_LOCAL_ROUTER = "192.168.100.28"
    static readonly URL_BASE = "http://" + this.IP_LOCAL_HOST + ":5000"
    static readonly URL_SUMMARY = "/summarize"
    static readonly URL_UPLOAD = "/upload"
    static readonly URL_GET_PDF_FILE_ZOTERO = "/getPdfFileZotero"
    

    @reportGen
    private static generateSummaries() { 
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        ztoolkit.log("[ReportGen] selectedItemsLength: " + sortedItems.length)
        
        // this.setSummarizeButton()
        const keyList = []
        for (let index = 0; index < sortedItems.length; index++) {
            ztoolkit.log("[ReportGen] index: " + index + " " + sortedItems.length)
            const item = sortedItems[index];
            const pdfFilePath = this.getFilePath(item)
            
            // if could not get file path
            if(!pdfFilePath){ continue }
            keyList.push(item.key)
        }
        ReportGenerationFactory.summarize(keyList)

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
    private static summarize(keyList:string[]){
        const postPdfFileList:Array<Promise<any>> = []
        // const worker = new Worker("./postZoteroFileThread.ts")

//        keyList.forEach((key) => {
//           postPdfFileList.push(this.postZoteroFile(key))
//        })

        // Promise.
        // postPdfFileList.push(this.postZoteroFile(keyList[0]))
        const result = this.postZoteroFile(this.ITEM_KEY)
        result.then((res) => {
            ztoolkit.log(res)
            this.getSummaryResult()
        })
        // postPdfFileList.push(this.postZoteroFile(this.ITEM_KEY))
        // Promise.all(postPdfFileList).then((res) => {
        //     this.getSummaryResult()
        // })
    }

    @reportGen
    private static logToNote(content:string){
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        
        // this.setSummarizeButton()
        const standAloneNote = sortedItems[0]
        standAloneNote.setNote(content)
    }

    @reportGen
    private static getFileName(path:string){
        return path.replace(/^.*(\\|\/|\:)/, '')
    }

    @reportGen
    private static async sendPdfFilesAsync(file: File):Promise<boolean>{
        const formData = new window.FormData()
        ztoolkit.log(formData)
        
        if(!file.type.startsWith('application/pdf')){
            throw new Error("Invalid file type: ${file.name}.")
        }

        formData.append('files', file)

        try {
            const response = await fetch(
                this.URL_BASE + this.URL_UPLOAD, 
                {
                    method: 'POST', 
                    body: formData, 
                }
            );

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
    private static async postZoteroFile(itemKey:string):Promise<any>{
        try{
            const response = await fetch(
                this.URL_BASE + this.URL_GET_PDF_FILE_ZOTERO,
                {
                    method: 'POST',
                    headers: {
                        'Api-Key': this.API_KEY,
                        'Library-Type': this.LIBRARY_TYPE,
                        'Library-Id': this.LIBRARY_ID,
                        'Item-Key': itemKey
                    }
                }
            )
            // ztoolkit.log(response)
        }
        catch(error){
            throw error
        }
    }

    @reportGen
    private static async getSummaryResult():Promise<any>{
        try{
            const response = await fetch(
                this.URL_BASE + this.URL_SUMMARY, 
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
    private static addSummaryNote(item:Zotero.Item){
        const htmlPrefix = "<div data-schema-version=\"8\">";
        const htmlSufix = "</div>"
        const htmlNoteTitle = "<p>" + NoteTitle + "<\p>";
        var htmlContent = "<p><strong>Hi</strong></p>"
        const htmlFinal = htmlPrefix + htmlNoteTitle + htmlContent + htmlSufix
        item.setNote(htmlFinal)
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
