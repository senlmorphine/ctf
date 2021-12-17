const { ipcRenderer, contextBridge } = require('electron')

contextBridge.exposeInMainWorld('electron',
  {
    safeEval: (input) => ipcRenderer.invoke('safeEval', input)
  }
)