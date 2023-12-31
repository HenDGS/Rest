// const { parentPort } = require('worker_threads');
// const EventSource = require('eventsource');
//
// const es = new EventSource('http://127.0.0.1:8001/stream');
//
// let buffer = [];
//
// es.onmessage = function (event) {
//     buffer.push(event.data);
//     console.log(buffer);
// };
//
// parentPort.on('message', (msg) => {
//     if (msg === 'getBuffer') {
//         parentPort.postMessage(buffer);
//     }
// });
//
// es.onerror = function (error) {
//     console.error(`EventSource failed: ${error}`);
// };

const EventSource = require('eventsource');
const fs = require("fs");

const es = new EventSource('http://127.0.0.1:8001/stream');

// let buffer = [];

es.onmessage = function (event) {
    // let new_data  = new Date().toString() + ' Message: ' + event.data;
    // fs.appendFile('data.txt', new_data + '\n', function (err) {
    //     if (err) throw err;
    //     // console.log('Saved!');
    // });

    if (event.data.startsWith('Products that haven\'t been sold in the last 3 days')) {
        let new_data  = new Date().toString() + ' Message: ' + event.data;
        fs.appendFile('data2.txt', new_data + '\n', function (err) {
            if (err) throw err;
            // console.log('Saved!');
        });
    }

    else {
        let new_data  = new Date().toString() + ' Message: ' + event.data;
        fs.appendFile('data.txt', new_data + '\n', function (err) {
            if (err) throw err;
            // console.log('Saved!');
        });
    }
}

// es.onerror = function (error) {
//     console.error(`EventSource failed: ${error}`);
// };