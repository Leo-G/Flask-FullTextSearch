angular.module('siteApp.controllers', []).controller('SiteListController', function($scope, $state,  $window, Site, $auth) {

$scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };

 var columnDefs = [ {headerName: "Sr No", width: 50, cellRenderer: function(params) {
            return params.node.id + 1;
            }},{ 
    
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
  
    

      $scope.deleteSite = function(selected_id) { // Delete a site. Issues a DELETE to /api/sites/:id
      site = Site.get({ id: selected_id});
      site.$delete({ id: selected_id},function() {
        $window.alert(selected_id + " was deleted successfully");
        $state.go('sites'); //redirect to home
        $state.reload();
      }, function(error) {
    $window.alert(error.status);
    });
    };
}).controller('SiteViewController', function($scope, $stateParams, Site) {
  $scope.site = Site.get({ id: $stateParams.id }); //Get a single site.Issues a GET to /api/sites/:id
  
}).controller('SiteCreateController', function($scope, $state, $stateParams, Site, $window) {
  $scope.site = new Site();  //create new site instance. Properties will be set via ng-model on UI

  $scope.addSite = function() { //create a new site. Issues a POST to /api/sites
    $scope.site.$save(function() {
      $window.alert("Site Saved");
      $state.go('sites'); // on success go back to home i.e. sites state.
    }, function(error) {
    $window.alert(error.data);
    } );
  };
}).controller('SiteEditController', function($scope, $state, $stateParams, $window, Site) {
  $scope.updateSite = function() { //Update the edited site. Issues a PUT to /api/sites/:id
    
    $scope.site.$update(function() {
      $window.alert("Changes Saved");
       $window.location.reload();
      //$state.go('sites'); // on success go back to home i.e. sites state.
    }, function(error) {
    $window.alert(error.data);
    });
  };

  //Required to edit a site
  $scope.loadSite = function() { //Issues a GET request to /api/sites/:id to get a site to update
  $scope.site = Site.get({ id: $stateParams.id }, function() {}, function(error) {
    $window.alert(error.data);
    });
  };

  $scope.loadSite(); // Load a site which can be edited on UI
}).controller('AuthController', function($auth, $state, $window, $scope, toaster) {
	
	
	 $scope.login = function() {

            $scope.credentials = {
                email: $scope.email,
                password: $scope.password
            }
            
            // Use Satellizer's $auth service to login
            $auth.login($scope.credentials).then(function(data) {

                // If login is successful, redirect to sites list
               
				$state.go('sites');
            })
            .catch(function(response){
               
               
               toaster.pop({
                type: 'error',
                title: 'Login Error',
                body: response.data,
                showCloseButton: true,
                timeout: 0
                });
               });
        }
		
        
 
}).controller('LogoutCtrl', function($auth,  $location, toaster) {
	
	
	if (!$auth.isAuthenticated()) { return; }
     $auth.logout()
      .then(function() {
      
        toaster.pop({
                type: 'success',               
                body: 'Bye' ,
                showCloseButton: true,
                
                });
        $location.url('/');
      }); 
		
        
 
}).controller('NavCtrl', function($auth,  $scope) {
	
	
	$scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
		
        
 
});



  