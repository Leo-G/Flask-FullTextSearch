var app = angular.module("sites", ["angularGrid", "ngResource"]);

app.config(['$resourceProvider', function($resourceProvider) {
  // Don't strip trailing slashes from calculated URLs
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.factory("Sites", function($resource) {
  return $resource("/sites/:id");
});

app.controller("SitesCtrl", function($scope, Sites) {


  var columnDefs = [{
    headerName: "id",
    field: "id",
    width: 100
  }, {
    headerName: "tag",
    field: "tag",
    width: 300
  }, {
    headerName: "url",
    field: "url",
    width: 500
  }, {
    headerName: "creation_date",
    field: "creation_date"
  }, {
    headerName: "reddit_score",
    field: "reddit_score",
    width: 100
  }, {
    headerName: "ycombinator_score",
    field: "ycombinator_score",
    width: 100
  }];


  $scope.gridOptions = {
    columnDefs: columnDefs,
    rowData: null,
    enableSorting: true,
    enableColResize: true,
    rowSelection: 'single',

  };

  Sites.get(function(data) {
    $scope.site = data.sites;
    $scope.gridOptions.rowData = $scope.site;
    $scope.gridOptions.api.onNewRows();
    $scope.gridOptions.api.sizeColumnsToFit();
  });

   
  

});