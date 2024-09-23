const manifest = (() => {
function __memo(fn) {
	let value;
	return () => value ??= (value = fn());
}

return {
	appDir: "_app",
	appPath: "_app",
	assets: new Set(["favicon.png"]),
	mimeTypes: {".png":"image/png"},
	_: {
		client: {"start":"_app/immutable/entry/start.Xly0OGcr.js","app":"_app/immutable/entry/app.CI2vTpyM.js","imports":["_app/immutable/entry/start.Xly0OGcr.js","_app/immutable/chunks/entry.BVgVxtpL.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/entry/app.CI2vTpyM.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/chunks/index.lnKugwF0.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-RUTRF6f_.js')),
			__memo(() => import('./chunks/1-DdcuVaEp.js')),
			__memo(() => import('./chunks/2-Bdt8VggT.js').then(function (n) { return n._; }))
		],
		routes: [
			{
				id: "/[...catchall]",
				pattern: /^(?:\/(.*))?\/?$/,
				params: [{"name":"catchall","optional":false,"rest":true,"chained":true}],
				page: { layouts: [0,], errors: [1,], leaf: 2 },
				endpoint: null
			}
		],
		matchers: async () => {
			
			return {  };
		},
		server_assets: {}
	}
}
})();

const prerendered = new Set([]);

const base = "";

export { base, manifest, prerendered };
//# sourceMappingURL=manifest.js.map
