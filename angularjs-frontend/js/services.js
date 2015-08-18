angular.module('siteApp.services', []).factory('Site', function($resource) {
  return $resource('/sites/:id', { id:'@site.id' }, {
    update: {
      method: 'PUT',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});