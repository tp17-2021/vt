# Vote machine frontend
Svelte frontend for the Voting Machine. Calls api backend on the same machine, that generates PDFs to print and calls gateway to send the votes to the backend.

## How to build
Used node --version v16.10.0 and Windows 10 for building, but it should work on any OS.

### First setup
Install dependencies using npm:
```bash
npm i
```

## Development mode
To start the development mode with automatic browser reloading after code change, run the following command:
```bash
npm run dev
```

Then open localhost:5000 in your browser.

### Debug mode
to enable debug mode, run the following command in browser console:
```js
debug(true)
```

In debug mode, vote is valid on load and first party is chosen automatically.

To disable debug mode, run the following command:
```js
debug(false)
```

## Production build
To build the production optimized version, run the following command:
```bash
npm run build
```

## Design requirements
### Scss components
Components from id-sk are used - see [documentation](https://idsk.gov.sk/)

### Screen size requirements
- (from EV-11) Portrait mode 768x1366 pixels
- everything should fit into the screen without scrolling

## Websocket testing tool
To simplify testing of the websocket connection, websocket mockup is included
```
cd test
npm i
node websocketMock.js
```
Then select the message you want to send to the client

Browser with CORS disabled is needed for testing>
```
"C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="C:/Chrome dev session" --disable-web-security
```


