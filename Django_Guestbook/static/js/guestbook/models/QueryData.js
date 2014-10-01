define([
	'dojo/_base/declare',
	'dojo/_base/lang',
	'dojo/_base/url',
	'dojo/io-query',
	'./_ModelBase'
], function(declare, lang, url, ioQuery, _ModelBase) {

	return declare(_ModelBase, {

		cursor: null,
		hasNext: false,
		hasPrev: false,
		limit: 10,
		nextLink: null,
		prevLink: null,
		selfLink: null,
		totalItems: null,

		getNextQueryOption: function() {
			var nextLink = this.get('nextLink');
			if (!nextLink) return;
			var query = ioQuery.queryToObject(new url(nextLink).query);
			return {
				start: query.cursor,
				count: query.limit
			};
		}
	});
});
