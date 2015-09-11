angular.module('siteApp', ['ui.router', 'ngResource', 'siteApp.controllers', 'siteApp.services', "angularGrid" , 'satellizer']);

angular.module('siteApp').config(function($stateProvider, $urlRouterProvider, $authProvider) {
	
	  // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/users/auth';

            // Redirect to the auth state if any other states
            // are requested other than users
            $urlRouterProvider.otherwise('/');
  $stateProvider. state('auth', {
	url: '/',
	templateUrl: 'auth/login.html',
	controller: 'AuthController'
  }).state('sites', { // state for showing all sites
    url: '/sites-new',
    templateUrl: 'sites-new/partials/sites.html',
    controller: 'SiteListController'
  }).state('viewSite', { //state for showing single site
    url: '/sites/:id/view',
    templateUrl: 'sites-new/partials/site-view.html',
    controller: 'SiteViewController'
  }).state('newSite', { //state for adding a new site
    url: '/sites/new',
    templateUrl: 'sites-new/partials/site-add.html',
    controller: 'SiteCreateController'
  }).state('editSite', { //state for updating a site
    url: '/sites/:id/edit',
    templateUrl: 'sites-new/partials/site-edit.html',
    controller: 'SiteEditController'
  });
}).run(function($state) {
  $state.go('auth'); //make a transition to sites state when app starts
});


               