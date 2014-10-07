define([
	'dojo/_base/declare',
	'dojo/router',
	'dojo/Stateful'
], function(declare, router, Stateful) {
	var app = declare(Stateful, {
		router: null,
		idGreeting : null
	});
	var instance;

	app.getDefaultInstance = function() {
		if (!instance) {
			instance = new app();
		}
		return instance;
	};

	return app.getDefaultInstance();
});
