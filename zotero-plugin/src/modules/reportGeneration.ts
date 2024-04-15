// import { spawn } from "child_process";

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
        var zp = Zotero.getActiveZoteroPane();
        var sortedItems = zp.getSortedItems()
        ztoolkit.log("[ReportGen] selectedItemsLength: " + sortedItems.length)

        for (let index = 0; index < sortedItems.length; index++) {
            
            ztoolkit.log("[ReportGen] index: " + index + " " + sortedItems.length)
            const item = sortedItems[index];

            ztoolkit.log("[ReportGen] isRegualarItem: " + item.isRegularItem())
            if(!item.isRegularItem()){
                continue;
            }
            ztoolkit.log("[ReportGen] hasSummaryNote: " + this.hasSummaryNote(item))
            if(this.hasSummaryNote(item)){
                continue;
            }
            // if(!this.hasPDFAttachment(item)){
            //     continue;
            // }
            var pdfFilePath = this.getPDFFilePath(item)
            ztoolkit.log("[ReportGen] pdfFilePath: " + pdfFilePath)
            if(!pdfFilePath){
                continue;
            }

        }
    }

    @reportGen
    private static hasSummaryNote(item:Zotero.Item):boolean{
        // ztoolkit.log(DebugReportGen + "isNote: " + item.isNote() + ", itemName: " + item.getDisplayTitle())
        var noteIDs = item.getNotes()
        // ztoolkit.log(noteIDs)
        for (let noteIndex = 0; noteIndex < noteIDs.length; noteIndex++){
            var noteID = noteIDs.at(noteIndex);
            if(noteID === undefined){
                continue;
            }
            var note = Zotero.Items.get(noteID);
            var noteTitle = note.getNoteTitle()
            ztoolkit.log("[ReportGen] " + noteTitle);
            if(noteTitle === NoteTitle){
                return true
            }
        }
        return false
    }

    @reportGen
    private static hasPDFAttachment(item:Zotero.Item):boolean{
        var attachmentIDs = item.getAttachments()
        ztoolkit.log(attachmentIDs)
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            var attachmentID = attachmentIDs.at(attachmentIndex);
            if(attachmentID === undefined){
                continue;
            }
            var attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){
                return true
            }
        }

        return false
    }

    @reportGen
    private static getPDFFilePath(item:Zotero.Item):string|false{
        var attachmentIDs = item.getAttachments()
        ztoolkit.log(attachmentIDs)
        for (let attachmentIndex = 0; attachmentIndex < attachmentIDs.length; attachmentIndex++){
            var attachmentID = attachmentIDs.at(attachmentIndex);
            if(attachmentID === undefined){
                continue;
            }

            var attachment = Zotero.Items.get(attachmentID)
            if(!attachment.isPDFAttachment()){
                continue;
            }

            var filePath = attachment.getFilePath()
            if(filePath){
                return filePath
            }
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
}