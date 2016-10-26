(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope', '$location'];
    function processController(DataService, ErrorHelperService, $scope, $location) {
        var self = this; // jshint ignore:line
        $scope.con_number = '';
        $scope.found = false;

        $scope.driver = {
            driver: -1,
            cost: 0,
            eta: "",
            drivers: [
            ]
        };

        $scope.search = function () {
            var send_data = {con_number: $scope.con_number};

            DataService.post('/api/lookup/', send_data)
                .then(function (data) {
                    data.eta = new Date(data.eta);
                    $scope.driver = data;
                    $scope.found = true;
                })
                .catch(function (error) {
                    $scope.found = false;
                    ErrorHelperService.displayInputControlError(error.message, self.searchForm);
                });
        };

        $scope.submit = function () {
            var send_data = {con_number: $scope.con_number,
                driver: $scope.driver.driver,
                eta: $scope.driver.eta,
                cost: $scope.driver.cost
            };

            DataService.post('/api/update/admin', send_data)
                .then(function (data) {
                    $scope.search(); //Update the form.
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.processForm);
                });
        };
        
        $scope.markProcessed = function () {
            var status = {
                status: 'processed',
                address: 'On The Hub Depot'
            };
            var send_data = {con_number: $scope.con_number, status: status};
            send_data.status = JSON.stringify(send_data.status);

            DataService.post('/api/update/status', send_data)
                .then(function (data) {
                    $location.path('/orders');
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.statusForm);
                });
        };
    }

    processController.$inject = deps;
    angular.module('App').controller('ProcessController', processController);
})();
