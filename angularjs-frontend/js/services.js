angular.module('siteApp.services', []).factory('Site', function($resource) {
  return $resource('/sites/:id', { id: '@id' }, {
    update: {
      method: 'PUT'
    }
    }, {
    stripTrailingSlashes: false
    });
});