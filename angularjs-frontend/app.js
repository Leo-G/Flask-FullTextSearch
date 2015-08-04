var module = angular.module("sites", ["angularGrid"]);

module.controller("SitesCtrl", function($scope, $http) {

    var columnDefs = [        
        {headerName: "id", field: "id", width: 100},
        {headerName: "tag", field: "tag", width: 300},
        {headerName: "url", field: "url", width: 500},
        {headerName: "creation_date", field: "creation_date"},
        {headerName: "reddit_score", field: "reddit_score", width: 100},            
        {headerName: "ycombinator_score", field: "ycombinator_score", width: 100}
    ];
   
    
    var rowData = [
    
    {"creation_date":"2015-08-03T20:05:57.879168+00:00","id":2,"reddit_score":null,"tag":"test","url":"http://techarena51.com","ycombinator_score":null},
    {"creation_date":"2015-08-03T20:05:57.879168+00:00","id":3,"reddit_score":null,"tag":"Reference destructing object before use","url":"http://stackoverflow.com/questions/30800720/reference-destructing-object-before-use","ycombinator_score":null},
    {"creation_date":"2015-08-03T20:05:57.879168+00:00","id":4,"reddit_score":null,"tag":"programinn","url":"http://stackoverflow.com/questions/18774718/object-storing-a-non-owning-reference-that-must-be-informed-before-the-reference?rq=1","ycombinator_score":null},
    {"creation_date":"2015-08-03T20:05:57.879168+00:00","id":5,"reddit_score":null,"tag":"boolean","url":"http://stackoverflow.com/questions/18774718/object-storing-a-non-owning-reference-that-must-be-informed-before-the-reference?rq=1","ycombinator_score":null}
        
    ];

    $scope.gridOptions = {
        columnDefs: columnDefs,
        rowData: null,
        enableSorting: true,
        enableColResize: true,
        rowSelection: 'single',


      
    };
    
    $http.get('/sites/sites')
       .success(function(data){
           $scope.gridOptions.rowData = data.sites;
           $scope.gridOptions.api.onNewRows();
           $scope.gridOptions.api.sizeColumnsToFit();
           

           
                      })

});