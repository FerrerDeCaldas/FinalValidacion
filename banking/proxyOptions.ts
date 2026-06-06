import { existsSync, readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const DEFAULT_WEBSERVER_PORT = Number(process.env.WEBSERVER_PORT ?? process.env.FRAPPE_WEBSERVER_PORT ?? 9000);

function getWebserverPort() {
	const configUrl = new URL('../../../sites/common_site_config.json', import.meta.url);
	const configPath = fileURLToPath(configUrl);

	if (!existsSync(configPath)) {
		return DEFAULT_WEBSERVER_PORT;
	}

	const common_site_config = JSON.parse(
		readFileSync(configUrl, 'utf8')
	) as { webserver_port: string | number };

	return Number(common_site_config.webserver_port ?? DEFAULT_WEBSERVER_PORT);
}

const webserver_port = getWebserverPort();

export default {
	'^/(app|api|assets|files|private)': {
		target: `http://127.0.0.1:${webserver_port}`,
		ws: true,
		router: function (req) {
			const site_name = req.headers?.host?.split(':')[0];
			return `http://${site_name ?? 'localhost'}:${webserver_port}`;
		}
	}
};
