angular.module('siteApp', ['ui.router', 'ngResource', 'siteApp.controllers', 'siteApp.services', "angularGrid"]);

angular.module('siteApp').config(function($stateProvider) {
  $stateProvider.state('sites', { // state for showing all sites
    url: '/',
    templateUrl: 'partials/sites.html',
    controller: 'SiteListController'
  }).state('viewSite', { //state for showing single site
    url: '/sites/:id/view',
    templateUrl: 'partials/site-view.html',
    controller: 'SiteViewController'
  }).state('newSite', { //state for adding a new site
    url: '/sites/new',
    templateUrl: 'partials/site-add.html',
    controller: 'SiteCreateController'
  }).state('editSite', { //state for updating a site
    url: '/sites/:id/edit',
    templateUrl: 'partials/site-edit.html',
    controller: 'SiteEditController'
  });
}).run(function($state) {
  $state.go('sites'); //make a transition to sites state when app starts
});