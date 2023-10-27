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

async function main() {
    while (true) {
        const prompt = require('prompt-sync')();
        let user_choice = prompt('What do you want to do? 1. Register 2. Get Data 3. Exit ');
        console.log(user_choice);

        if (user_choice === '1') {
            await postData();
        } else if (user_choice === '2') {
            await getData();
        } else if (user_choice === '3') {
            break;
        }
    }
}

main().then(() => console.log('Done'));
