const { contextBridge, ipcRenderer } = require('electron/renderer')

contextBridge.exposeInMainWorld('electronAPI', {
	uploadFolder: (folderDir) => ipcRenderer.send('Upload Folder', folderDir),
	onPythonLog: (callback) => ipcRenderer.on('Python Log', (_event, value) => callback(value))
});