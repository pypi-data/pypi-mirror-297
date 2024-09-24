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
		client: {"start":"_app/immutable/entry/start.BodKjuQE.js","app":"_app/immutable/entry/app.HgQDinFl.js","imports":["_app/immutable/entry/start.BodKjuQE.js","_app/immutable/chunks/entry.Br8KHvZB.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/entry/app.HgQDinFl.js","_app/immutable/chunks/preload-helper.D6kgxu3v.js","_app/immutable/chunks/scheduler.xQsDa6L3.js","_app/immutable/chunks/index.lnKugwF0.js"],"stylesheets":[],"fonts":[],"uses_env_dynamic_public":false},
		nodes: [
			__memo(() => import('./chunks/0-O5txkm00.js')),
			__memo(() => import('./chunks/1--PJ-eYkf.js')),
			__memo(() => import('./chunks/2-DleTh3G7.js').then(function (n) { return n._; }))
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
