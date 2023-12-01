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

async function postProduct() {
    // product with code, name, description, price, quantity, stock
    const prompt = require('prompt-sync')();
    let product_code = prompt('Product code: ');
    let product_name = prompt('Product name: ');
    let product_description = prompt('Product description: ');
    let product_price = prompt('Product price: ');
    let product_quantity = prompt('Product quantity: ');
    let product_stock = prompt('Product stock: ');

    const response = await fetch('http://127.0.0.1:5000/RegisterProduct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: product_code,
            name: product_name,
            description: product_description,
            price: product_price,
            quantity: product_quantity,
            min_stock: product_stock,
        }),
    });
    const data = await response.json();
    console.log(data);

    return data;
}

async function removeProduct() {
    // product with code and quantity
    const prompt = require('prompt-sync')();
    let product_code = prompt('Product code: ');
    let product_quantity = prompt('Product quantity: ');

    const response = await fetch('http://127.0.0.1:5000/RemoveProduct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: product_code,
            quantity: product_quantity,
        }),
    });
    const data = await response.json();
    console.log(data);

    return data;
}

async function getProducts() {
    const response = await fetch('http://127.0.0.1:5000/GetProduct');

    const data = await response.json();
    console.log(data);
    return data;
}

async function getstocklog() {
    const prompt = require('prompt-sync')();
    let initial_date = prompt('Initial date: ');
    let final_date = prompt('Final date: ');

    const response = await fetch('http://127.0.0.1:5000/GetStockLog', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            initial_date: initial_date,
            final_date: final_date,
        }),
    });
    const data = await response.json();
    console.log(data);

    return data;
}

async function getproductswithoutmovement() {
    const prompt = require('prompt-sync')();
    let initial_date = prompt('Initial date: ');
    let final_date = prompt('Final date: ');

    const response = await fetch('http://127.0.0.1:5000/GetProductsWithoutMovement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            initial_date: initial_date,
            final_date: final_date,
        }),
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
        console.log('What do you want to do?');
        console.log('1. Register');
        console.log('2. Register Product');
        console.log('3. Remove Product');
        console.log('4. Get Products');
        console.log('5. Get Stock Log');
        console.log('6. Get Products Without Movement');
        console.log('7. Get Notifications About Products That Have Not Been Sold In The Last 3 Days');
        console.log('8. Get Notifications About Products That Need To Be Replenished');
        console.log('9. Exit');
        let user_choice = prompt();

        if (user_choice === '1') {
            await postData();

        }

        else if (user_choice === '2') {
            await postProduct();
        }

        else if (user_choice === '3') {
            await removeProduct();
        }

        else if (user_choice === '4') {
            await getProducts();
        }

        else if (user_choice === '5') {
            await getstocklog();
        }

        else if (user_choice === '6') {
            await getproductswithoutmovement();
        }

        else if (user_choice === '7') {
            const fs = require('fs');
            try {
                const data = fs.readFileSync('data2.txt', 'utf8');
                console.log(data);
            } catch (err) {
                console.error(err);
            }

            fs.writeFile('data2.txt', '', function (err) {
                if (err) throw err;
                // console.log('File is cleaned!');
            });

        }

        else if (user_choice === '8') {
            const fs = require('fs');
            try {
                const data = fs.readFileSync('data.txt', 'utf8');
                console.log(data);
            } catch (err) {
                console.error(err);
            }

            fs.writeFile('data.txt', '', function (err) {
                if (err) throw err;
                // console.log('File is cleaned!');
            });

        }

        else if (user_choice === '9') {
            worker.terminate()

            break;
        }
    }
}

main().then(() => console.log('Done'));
