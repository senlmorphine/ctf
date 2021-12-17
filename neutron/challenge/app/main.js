const {app, BrowserWindow, ipcMain} = require('electron')
const path = require('path')
const HOST = process.env.HOST || 'http://electron.lol:1337'
function createWindow () {
    const mainWindow = new BrowserWindow({
        width: 1400,
        height: 800,
        webPreferences: {
            sandbox:true,
            contextIsolation: true,
            preload: path.join(__dirname, 'preload.js'),
    }
    })
    
    mainWindow.loadURL(HOST);
    ipcMain.handle('safeEval', (event, input) => {
        if (mainWindow) {
            eval(input);
        }
     })
     mainWindow.webContents.on('will-navigate', (event, navigationUrl) => {
        event.preventDefault();
    })
    mainWindow.webContents.on('will-redirect', (event, navigationUrl) => {
        event.preventDefault();
    })
    mainWindow.webContents.setWindowOpenHandler(() => {
        return { action: "deny" };
    });

   
}
delete require('electron').nativeImage.createThumbnailFromPath



app.whenReady().then(() => {
  createWindow()
  
  app.on('activate', function () {
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })

})


app.on('window-all-closed', function () {
  if (process.platform !== 'darwin') app.quit()
})
