const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  send: (channel, data) => {
    ipcRenderer.send(channel, data);
    console.log('Preload Send:', channel, data);
  },
  receive: (channel, func) => {
    ipcRenderer.on(channel, (event, ...args) => func(...args));
    console.log('Preload Receive:', channel);
  },
});



// // gui/preload.js
// const { contextBridge, ipcRenderer } = require('electron');

// const SEND_CHANNELS = [
//   'getDefaults',
//   'run-lipidimea-cli-steps',
//   'open-file-dialog',
//   'request-filename-and-directory',
//   'open-directory-dialog',
//   'write-yaml',
//   'file-dialog-selection'
// ];
// const RECEIVE_CHANNELS = [
//   'returnDefaults',
//   'python-result-experiment',
//   'file-content',
//   'selected-param-save-directory',
//   'directory-selected'
// ];

// contextBridge.exposeInMainWorld('api', {
//   send(channel, ...args) {
//     if (SEND_CHANNELS.includes(channel)) {
//       ipcRenderer.send(channel, ...args);
//     } else {
//       console.warn(`api.send blocked invalid channel: ${channel}`);
//     }
//   },
//   receive(channel, callback) {
//     if (RECEIVE_CHANNELS.includes(channel)) {
//       ipcRenderer.on(channel, (event, ...args) => callback(...args));
//     } else {
//       console.warn(`api.receive blocked invalid channel: ${channel}`);
//     }
//   }
// });
