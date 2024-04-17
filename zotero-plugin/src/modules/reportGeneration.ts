// import { spawn } from "child_process";

import { UITool, TagElementProps } from "zotero-plugin-toolkit/dist/tools/ui";

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
    static registerSummaries() { 
        const zp = Zotero.getActiveZoteroPane();
        const sortedItems = zp.getSortedItems()
        ztoolkit.log("[ReportGen] selectedItemsLength: " + sortedItems.length)
        
        this.setSummarizeButton()

        for (let index = 0; index < sortedItems.length; index++) {
            ztoolkit.log("[ReportGen] index: " + index + " " + sortedItems.length)
            const item = sortedItems[index];

            ztoolkit.log("[ReportGen] isRegualarItem: " + item.isRegularItem())
            // if the item is not a pdf
            if(!item.isRegularItem()){ continue }

            ztoolkit.log("[ReportGen] hasSummaryNote: " + this.hasSummaryNote(item))
            // if item already has a summary note
            if(this.hasSummaryNote(item)){ continue }

            var pdfFilePath = this.getPDFFilePath(item)
            ztoolkit.log("[ReportGen] pdfFilePath: " + pdfFilePath)
            // if could not get file path
            if(!pdfFilePath){ continue }

        }
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
        const attachmentIDs = item.getAttachments()
        ztoolkit.log(attachmentIDs)
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            const attachmentID = attachmentIDs.at(attachmentIndex);
            if(attachmentID === undefined){ continue; }

            const attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){ continue; }

            const filePath = attachment.getFilePath()
            if(filePath){ return filePath }
            // ztoolkit.log("[ReportGen] filePath in folder: " + filePath + " " + !filePath)
        }
        return false
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
    private static setSummarizeButton(){
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
            }
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