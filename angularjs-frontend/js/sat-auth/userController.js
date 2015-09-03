(function() {

    'use strict';

    angular
        .module('authApp')
        .controller('TaskController', TaskController);  

    function TaskController($http, $auth, $state, $scope) {       
        
        $scope.users;
        $scope.error;       

            // This request will hit the index method in the AuthenticateController
            // on the flask side and will return the list of users
            $http.get('/users/').success(function(data) {
                $scope.users = data.users;
            }).error(function(error) {
                $scope.error = error;
            });
        
          $scope.logout = function() {
        
          if ($auth.logout()) {
             $state.go('auth', {});   

    }
    }
    }
    
})();