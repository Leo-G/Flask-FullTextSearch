angular.module('siteApp', ['ui.router', 'ngResource', 'siteApp.controllers', 'siteApp.services', "angularGrid" , 'satellizer','toaster', 'ngAnimate', 'ngFileUpload']);

angular.module('siteApp').config(function($stateProvider, $urlRouterProvider, $authProvider) {
	
	  // Satellizer configuration that specifies which API
            // route the JWT should be retrieved from
            $authProvider.loginUrl = '/users/auth';

            // Redirect to the auth state if any other states
            // are requested other than users
            $urlRouterProvider.otherwise('/');
  $stateProvider. state('auth', {
	url: '/login',
	templateUrl: 'auth/login.html',
	controller: 'AuthController',
        resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
     
  }).state('sites', { // state for showing all sites
    url: '/',
    templateUrl: 'sites-new/partials/sites.html',
    controller: 'SiteListController',
        resolve: {
          loginRequired: loginRequired
        }
  }).state('viewSite', { //state for showing single site
    url: '/sites/:id/view',
    templateUrl: 'sites-new/partials/site-view.html',
    controller: 'SiteViewController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('newSite', { //state for adding a new site
    url: '/sites/new',
    templateUrl: 'sites-new/partials/site-add.html',
    controller: 'SiteCreateController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('editSite', { //state for updating a site
    url: '/sites/:id/edit',
    templateUrl: 'sites-new/partials/site-edit.html',
    controller: 'SiteEditController',
    resolve: {
          loginRequired: loginRequired
        }
  }).state('files', { // state for showing all images
    url: '/file-share',
    templateUrl: 'file-share/index.html',
    controller: 'ImageListController',
        resolve: {
          loginRequired: loginRequired
        }
  }).state('newFile', { //state for adding a new image
    url: '/file-share/new',
    templateUrl: 'file-share/add.html',
    controller: 'FileCreateController',
    resolve: {
          loginRequired: loginRequired
        }
      
  }).state('logout', {
        url: '/logout',
        template: null,
        controller: 'LogoutCtrl'
      });
      
   
  
   function skipIfLoggedIn($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
       
       
        deferred.reject();
        
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }
    
   function loginRequired($q, $location, $auth, $state) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }
    
    
});

//Initialize controllers and services
angular.module('siteApp.controllers', []);
angular.module('siteApp.services', []);
               