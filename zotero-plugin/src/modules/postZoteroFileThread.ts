import { parentPort } from "worker_threads";

var api_key 
var library_type  
var library_id
var item_key

// onmessage = function(e) {
//     api_key = e.data['API_KEY']    
//     library_type = e.data['LIBRARY_TYPE']
//     library_id = e.data['LIBRARY_ID']
//     item_key = e.data['ITEM_KEY']
// }
// ztoolkit.log(api_key, library_type, library_id, item_key)
// parentPort?.postMessage(true)
// try{
//     const response = await fetch(
//         this.URL_BASE + this.URL_GET_PDF_FILE_ZOTERO,
//         {
//             method: 'POST',
//             headers: {
//                 'Api-Key': this.API_KEY,
//                 'Library-Type': this.LIBRARY_TYPE,
//                 'Library-Id': this.LIBRARY_ID,
//                 'Item-Key': itemKey
//             }
//         }
//     )
//     ztoolkit.log(response.headers)
// }
// catch(error){
//     throw error
// }