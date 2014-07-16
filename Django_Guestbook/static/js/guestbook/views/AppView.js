define([
	'dojo/_base/declare',
	'dijit/layout/ContentPane',
	'./_ViewBaseMixin',
	'dojo/text!./templates/AppView.html',
	'dojo/i18n!../nls/common'
], function(declare, ContentPane, _ViewBaseMixin, template, nls) {

	return declare([ContentPane, _ViewBaseMixin], {
		templateString: template,
		nls: nls
	});

});
