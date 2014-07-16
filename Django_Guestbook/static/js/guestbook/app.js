define([
	'dojo/_base/config',
	'dojo/_base/window',
	'dojo/parser',
	'dojo/ready',
	'./views/AppView'
], function(config, win, parser, ready, AppView) {
	ready(function() {
		if (!config.parseOnLoad) {
			parser.parse();
		}
		var view = new AppView(),
			body = win.body();
		view.placeAt(body);
		view.startup();
	});
});
