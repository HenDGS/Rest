# Rest Project

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
    <ol>
        <li><a href="#about-the-project">About The Project</a></li>
        <li>
        <a href="#getting-started">Getting Started</a>
        <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
        </ul>
        </li>
        <li><a href="#usage">Usage</a></li>
    </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Project to reimplement the [Pyro] middleware project in the REST architecture.

Development of a product inventory management system. Use Rest to provide communication between processes.
Methods available in the stock management system:
- User registration. When accessing the system for the first time,
a stock manager must enter their name, public key and
remote object reference;
- Posting product input and output:
  - When entering the product, the code must be entered,
name, description, quantity, unit price and minimum stock of the product.
product. On issue, you must enter the code and quantity. The
system must also save the date and time of each entry.
- Report generation:
  - Products in stock;
  - Flow of movement (inflows and outflows) of stock
  by period;
  - List of unissued products by period.

Method available from the client:
- Event notification: the stock management system has the task of
the manager, via a method call, the following event notifications
events:
- Product that has reached minimum stock so that replenishment can be
replenished;
- Periodic reports warning of unsold products in order to
to identify the need for promotions.

Client is implemented in JavaScript, and the server is implemented in Python.

SSE (Server-Sent Events) is used to send notifications from the server to the client.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Clone or download the repository, then follow the instructions below.

### Prerequisites

Install the requirements for the client.
* npm
  ```sh
  npm install
  ```
Install the requirements for the server.
* pip
  ```sh
  pip install -r requirements.txt
  ```

<!-- USAGE EXAMPLES -->
## Usage

Start the server (server.py) with python.
```sh
python server.py
```

Start client (js/client.js) with node.
```sh
node client.js
```

Now select the options in the client menu.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[Pyro]: https://github.com/HenDGS/MiddlewarePyro