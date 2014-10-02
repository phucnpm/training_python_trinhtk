define([
	'dojo/_base/declare',
	'dojo/router',
	'dojo/Stateful'
], function(declare, router, Stateful) {
	return declare(Stateful, {
		router: null,
		idGreeting : null
	});
});
