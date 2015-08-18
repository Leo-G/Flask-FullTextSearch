var app = angular.module("site_update", ["ngResource"]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.factory("Sites", function($resource) {
  return $resource("/sites/:id");
});

app.controller("UpdateCtrl", function($scope, Sites) {


  

  
  $scope.edit = function(site_id) {

  Sites.get({id:site_id}, function(data) {
    $scope.site1 = data.site;
    
  });

   };
  

});