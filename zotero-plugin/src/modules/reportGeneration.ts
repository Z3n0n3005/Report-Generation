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
    // static readonly ITEM_KEY = "3XNTQMIM"
    static readonly IP_LOCAL_HOST = "127.0.0.1"
    static readonly IP_LOCAL_ROUTER = "192.168.100.28"
    static readonly URL_BASE = "http://" + this.IP_LOCAL_ROUTER + ":5000"
    static readonly URL_SUMMARY = "/summarize"
    static readonly URL_UPLOAD = "/upload"
    static readonly URL_GET_PDF_FILE_ZOTERO = "/getPdfFileZotero"
    

    @reportGen
    private static generateSummaries() { 
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        // ztoolkit.log("[ReportGen] selectedItemsLength: " + sortedItems.length)
        
        // this.setSummarizeButton()
        const keyList = []
        const itemKeyPair:{[key:string]: Zotero.Item} = {}
        for (let index = 0; index < sortedItems.length; index++) {
            const item = sortedItems[index];
            // ztoolkit.log("display titles")
            // ztoolkit.log(item.getDisplayTitle())
            const pdfFilePath = this.getFilePath(item)
            const pdfFileItemKey = this.getFileItemKey(item)

            // if could not get file path
            if(!pdfFilePath || !pdfFileItemKey){ continue }

            keyList.push(pdfFileItemKey)
            // ztoolkit.log("From self")
            // ztoolkit.log(item)
            itemKeyPair[pdfFileItemKey] = item
            // ztoolkit.log("From dictionary:")
            // ztoolkit.log(itemKeyPair[item.key])
            ztoolkit.log("Dictionary: ")
            ztoolkit.log(itemKeyPair)
        }
        ReportGenerationFactory.summarize(keyList, itemKeyPair)

    }

    @reportGen
    private static getFilePath(item:Zotero.Item):string|false{
        // ztoolkit.log("[ReportGen] isRegualarItem: " + item.isRegularItem())
        // if the item is not a pdf
        if(!item.isRegularItem()){ return false }

        // ztoolkit.log("[ReportGen] hasSummaryNote: " + this.hasSummaryNote(item))
        // if item already has a summary note
        if(this.hasSummaryNote(item)){ return false }

        const pdfFilePath = this.getPDFFilePath(item)
        // ztoolkit.log("[ReportGen] pdfFilePath: " + pdfFilePath)
        // if could not get file path
        if(!pdfFilePath){ return false }
        return pdfFilePath
    }

    @reportGen
    private static getFileItemKey(item:Zotero.Item):string|false{
        if(!item.isRegularItem()){ return false }

        if(this.hasSummaryNote(item)){ return false }

        const attachmentIDs = item.getAttachments()
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            const attachmentID = attachmentIDs.at(attachmentIndex)
            if(attachmentID === undefined){ continue }

            const attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){ continue }
            return attachment.key
        }
        return false
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
            // ztoolkit.log("[ReportGen] " + noteTitle);
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
        // ztoolkit.log("userID: " + Zotero.Users.getCurrentUserID())
        // ztoolkit.log("itemID: " + item.key)
        const attachmentIDs = item.getAttachments()
        // ztoolkit.log(attachmentIDs)
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
    private static summarize(keyList:string[], itemKeyPair:{[key:string]:Zotero.Item}){
        const postPdfFileList:Array<Promise<any>> = []

        keyList.forEach((key) => {
            ztoolkit.log(key)
            postPdfFileList.push(this.postZoteroFile(key))
        })

        Promise.allSettled(postPdfFileList)
        .then((res) => {
            // ztoolkit.log(res)
            return this.getSummaryResult()
        })
        .then((res) =>  {
            // ztoolkit.log(res[0])
            res.forEach((sum:{id:string, name:string, abstract_seg:string, segments:[{header:string, content:string}]}) => {
                const itemKey = String(sum.id)
                const item = itemKeyPair[itemKey]
                const segments = sum.segments
                ztoolkit.log(sum)
                ztoolkit.log(itemKey + " " + this.ITEM_KEY)
                ztoolkit.log(itemKey === this.ITEM_KEY)
                ztoolkit.log(item)
                ztoolkit.log(itemKeyPair)
                // ztoolkit.log(itemKeyPair[this.ITEM_KEY])
                if(item !== undefined){
                    this.addSummaryNote(item, segments)
                } else {
                    ztoolkit.log("item is undefined " + itemKey)
                }
            })
        })
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
    private static addSummaryNote(item:Zotero.Item, segments:[{header:string, content:string}]){
        const htmlPrefix = "<div data-schema-version=\"9\">";
        const htmlSufix = "</div>"
        const htmlNoteTitle = "<p>" + NoteTitle + "</p>";
        var htmlContent = ""
        var contents = segments
        contents.forEach((content:any) => {
            htmlContent += "<strong><p>" + content.header + "</p></strong>"
            htmlContent += "<p>" + content.content + "</p>"
        })

        const htmlFinal = htmlPrefix + htmlNoteTitle + htmlContent + htmlSufix
        var noteItem = new Zotero.Item("note")
        const zp = Zotero.getActiveZoteroPane()
        const sortedItems = zp.getSortedItems()
        ztoolkit.log(htmlFinal)
        noteItem.setNote(htmlFinal)
        noteItem.parentID = item.id
        item.saveTx()
        noteItem.saveTx()
        // item.(htmlFinal)
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
