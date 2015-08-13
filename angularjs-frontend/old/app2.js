var app = angular.module('app',['ui.router']);

app.config(function($stateProvider, $urlRouterProvider) {
  //
  // For any unmatched url, redirect to /state1
  $urlRouterProvider.otherwise("/state1");
  //
  // Now set up the states
  $stateProvider
    .state('state1', {
      url: "/state1/",
      templateUrl: "state1.html"
    })
    
    
    .state('state2', {
      url: "/state2/:id",
      templateUrl: "/state2.html",
      controller: 'MainCtrl'
    });
});


app.controller("MainCtrl", function($scope, $stateParams ) { 
  
  $scope.edit = $stateParams.id;
  

});

   