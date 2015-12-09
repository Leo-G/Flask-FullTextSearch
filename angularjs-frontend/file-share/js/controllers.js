angular.module('siteApp.services').factory('Image', function($resource) {
  return $resource('/api/v1/images/:id', { id:'@image.id' }, {
    update: {
      method: 'PUT',
      
     
     
    }
    }, {
    stripTrailingSlashes: false
    });
});



angular.module('siteApp.controllers').controller('ImageListController', function($scope, $state,  $window, $auth, Image) {



 var columnDefs = [ {headerName: "Sr No", width: 50, cellRenderer: function(params) {
            return params.node.id + 1;
            }},{ 
    
    headerName: "id",
    field: "id",
    width: 100
  }, {
    headerName: "name",
    field: "name",
    width: 300
  }, {
    headerName: "file_path",
    field: "file_path",
    width: 500
  }, {
    headerName: "creation_date",
    field: "creation_date"
  }, {
    headerName: "tag",
    field: "tag",
    width: 100
  }];


  $scope.gridOptions = {
    columnDefs: columnDefs,
    rowData: null,
    enableSorting: true,
    enableColResize: true,
    rowSelection: 'single',

  };
    
     Image.get(function(data) {
    $scope.images = data.images;
    $scope.gridOptions.rowData = $scope.images;
    $scope.gridOptions.api.onNewRows();
    $scope.gridOptions.api.sizeColumnsToFit();
  });

}).controller('FileCreateController', function($scope, $state, $stateParams, $timeout, toaster, $window, Upload) {
  
    $scope.uploadPic = function(file) {
    file.upload = Upload.upload({
      url: 'http://staging-search/api/v1/images/',
      data: {file: file, name: $scope.username, description:"test", tag:"test"},
    });

    file.upload.then(function (response) {
      $timeout(function () {
        file.result = response.data;
          toaster.pop({
                type: 'success',               
                body: response.data ,
                showCloseButton: true,
                
                });
          $state.go('files'); 
      });
    }, function (response) {
      if (response.status > 0)
        $scope.errorMsg = response.status + ': ' + response.data;
        
        toaster.pop({
                type: 'error',
                title: 'Error',
                body: $scope.errorMsg,
                showCloseButton: true,
                timeout: 0
                });
    }, function (evt) {
      // Math.min is to fix IE which reports 200% sometimes
      file.progress = Math.min(100, parseInt(100.0 * evt.loaded / evt.total));
    });
    }

 
});

  