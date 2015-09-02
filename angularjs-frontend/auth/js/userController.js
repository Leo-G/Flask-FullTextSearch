(function() {

    'use strict';

    angular
        .module('authApp')
        .controller('TaskController', TaskController);  

    function TaskController($http) {

        var vm = this;
        
        vm.task;
        vm.error;

        vm.getUsers = function() {

            // This request will hit the index method in the AuthenticateController
            // on the Laravel side and will return the list of users
            $http.get('/users/').success(function(data) {
                vm.users = data.users;
            }).error(function(error) {
                vm.error = error;
            });
        }
    }
    
})();