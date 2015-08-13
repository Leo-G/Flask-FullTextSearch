angular.module('siteApp.controllers', []).controller('SiteListController', function($scope, $state,  $window, Site) {

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
  
  Site.get(function(data) {
    $scope.sites = data.sites;
    $scope.gridOptions.rowData = $scope.sites;
    $scope.gridOptions.api.onNewRows();
    $scope.gridOptions.api.sizeColumnsToFit();
  });
  
  
    

  $scope.deleteSite = function(site) { // Delete a site. Issues a DELETE to /api/sites/:id
    
      site.$delete(function() {
        $window.location.href = ''; //redirect to home
      });
    };
}).controller('SiteViewController', function($scope, $stateParams, Site) {
  $scope.site = Site.get({ id: $stateParams.id }); //Get a single site.Issues a GET to /api/sites/:id
}).controller('SiteCreateController', function($scope, $state, $stateParams, Site) {
  $scope.site = new Site();  //create new site instance. Properties will be set via ng-model on UI

  $scope.addSite = function() { //create a new site. Issues a POST to /api/sites
    $scope.site.$save(function() {
      $state.go('sites'); // on success go back to home i.e. sites state.
    });
  };
}).controller('SiteEditController', function($scope, $state, $stateParams, Site) {
  $scope.updateSite = function() { //Update the edited site. Issues a PUT to /api/sites/:id
    $scope.site.$update(function() {
      $state.go('sites'); // on success go back to home i.e. sites state.
    });
  };

  $scope.loadSite = function() { //Issues a GET request to /api/sites/:id to get a site to update
    $scope.site = Site.get({ id: $stateParams.id });
  };

  $scope.loadSite(); // Load a site which can be edited on UI
});