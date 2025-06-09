# Python Proxy

A simple server that proxies the request to https://en.wikipedia.org/ and modifying the response content

## Usage

### Run the Proxy Server

```bash
cd src
flask run
```

By default, the app is running on `localhost:5000`. You can change the host and port using command-line arguments:

```bash
flask run --host 0.0.0.0 --port 8888
```

## Contributing

Pull requests are welcome! Please open an issue first to discuss changes.
