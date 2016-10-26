(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope', '$location'];
    function statusController(DataService, ErrorHelperService, $scope, $location) {
        var self = this; // jshint ignore:line
        $scope.con_number = '';
        $scope.status = {
            status: "",
            address: ""
        };

        $scope.submitStatus = function () {
            var send_data = {con_number: $scope.con_number, status: $scope.status};
            send_data.status = JSON.stringify(send_data.status);

            DataService.post('/api/update/status', send_data)
                .then(function (data) {
                    $location.path('/orders');
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.statusForm);
                });
        };

        if ($routeParams.id !== undefined) {
            $scope.con_number = $routeParams.id;
        }
    }

    statusController.$inject = deps;
    angular.module('App').controller('StatusController', statusController);
})();
