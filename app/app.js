const { app, BrowserWindow, ipcMain } = require("electron");
const { PythonShell } = require('python-shell');
const path = require("node:path");

function createWindow(){
	const window = new BrowserWindow({
		webPreferences: {
			preload: path.join(__dirname, 'preload.js')
		},
		width: 800,
		height: 600
	});

	ipcMain.on('Upload Folder', function (event, folderDir){
		const python = new PythonShell('improve-base-model.py');
		python.send(folderDir);
		python.on('message', message => window.webContents.send('Python Log', message));
		python.end((err, code, signal) => console.log("Finished"));
	});

	window.loadFile("app.html");
}

app.whenReady().then(() => {
	createWindow()
	app.on("activate", function (){
		if(BrowserWindow.getAllWindows().length == 0) createWindow();
	});
})

app.on("window-all-closed", () => {
	if(process.platform !== "darwin") app.quit()
})