import App from './App.svelte';

import './routes';
import './api/websocket';

const app = new App({
	target: document.body,
	props: {
	}
});

export default app;