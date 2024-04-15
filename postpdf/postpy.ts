import * as path from 'path';
import * as request from 'request';
import * as BrowserFS from 'browserfs';

const urlBase: string = 'http://127.0.0.1:5000';
const urlUpload: string = '/upload';
const urlSummarize: string = '/summarize';
const pdfFolder: string = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper';
const pdfPath: string = 'C:\\Users\\DELL\\Prototype\\Report-Generation\\paper\\a-brief-survey-of-text-mining.pdf';

// Initialize BrowserFS
BrowserFS.configure(
    {
        fs: "IndexedDB",
        options: {}
    },
    (error) => {
        if (error) {
            console.error("Failed to initialize BrowserFS:", error);
            return;
        }
        
        // Set BrowserFS as the file system
        const fs = BrowserFS.BFSRequire('fs');
        
        function uploadFile(filePath: string, url: string): Promise<any> {
            const formData = {
                files: fs.createReadStream(filePath)
            };

            return new Promise((resolve, reject) => {
                request.post({ url: url, formData: formData }, (error, response, body) => {
                    if (error) {
                        reject(error);
                    } else {
                        resolve(body);
                    }
                });
            });
        }

        function main(): void {
            const inputFilePaths: string[] = fs.readdirSync(pdfFolder).map(file => path.join(pdfFolder, file));
            
            const promises: Promise<any>[] = inputFilePaths.map(filePath => uploadFile(filePath, urlBase + urlUpload));

            Promise.all(promises)
                .then(results => {
                    results.forEach(result => {
                        console.log(result);
                    });
                })
                .catch(error => {
                    console.error(error);
                });

            request.post({ url: urlBase + urlSummarize }, (error, response, body) => {
                if (!error && response.statusCode === 200) {
                    console.log(body);
                }
            });
        }

        main();
    }
);
