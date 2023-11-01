async function getData() {
    const response = await fetch('http://127.0.0.1:5000/TodoList');
    const data = await response.json();
    console.log(data);
    return data;
}

async function postData() {
    const prompt = require('prompt-sync')();
    let user_name = prompt('What is your name? ');
    console.log(user_name);

    const response = await fetch('http://127.0.0.1:5000/RegisterClient', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: user_name }),
    });
    const data = await response.json();
    console.log(data);

    return data;
}


// async function main() {
//     // start the sse_client.js in another worker thread
//     const { Worker } = require('worker_threads');
//     const worker = new Worker('./sse_client.js');
//
//     while (true) {
//         const prompt = require('prompt-sync')();
//         let user_choice = prompt('What do you want to do? 1. Register 2. Get Data 3. Exit ');
//         console.log(user_choice);
//
//         if (user_choice === '1') {
//             await postData();
//         } else if (user_choice === '2') {
//             await getData();
//         } else if (user_choice === '3') {
//             // print the worker thread's buffer
//             console.log(worker.buffer);
//         } else if (user_choice === '4') {
//             break;
//         }
//     }
// }

async function main() {
    const { Worker } = require('worker_threads');
    const worker = new Worker('./sse_client.js');
    const prompt = require('prompt-sync')();

    while (true) {
        // let user_choice = prompt('What do you want to do? 1. Register 2. Get Data 3. SSE 4.Exit ');
        console.log('What do you want to do?');
        console.log('1. Register');
        console.log('2. Get Data');
        console.log('3. SSE');
        console.log('4. Exit');
        let user_choice = prompt();

        if (user_choice === '1') {
            await postData();

        } else if (user_choice === '2') {
            await getData();

        } else if (user_choice === '3') {
            const fs = require('fs');
            try {
                const data = fs.readFileSync('data.txt', 'utf8');
                console.log(data);
            } catch (err) {
                console.error(err);
            }

            fs.writeFile('data.txt', '', function (err) {
                if (err) throw err;
                console.log('File is cleaned!');
            });

        } else if (user_choice === '4') {
            worker.terminate()

            break;
        }
    }
}

main().then(() => console.log('Done'));
