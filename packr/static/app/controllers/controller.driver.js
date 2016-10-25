(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope'];
    function updateDriverController(DataService, ErrorHelperService, $scope) {
        var self = this; // jshint ignore:line
        $scope.con_number = -1;
        $scope.found = true;

        $scope.driver = {
            type: "",
            dangerous: "none",
            requirePickup: "no",
            pickup: {
                businessName: "",
                contactName: "",
                phone: "",
                email: "",
                street: "",
                suburb: "",
                state: "",
                postCode: "",
                date: "",
                time: ""
            },
            delivery: {
                businessName: "",
                contactName: "",
                phone: "",
                email: "",
                street: "",
                suburb: "",
                state: "",
                postCode: ""
            },
            fragile: "",
            paymentType: "",
            customerComments: "",
            packages: [
                {'weight': 0, 'length': 0, 'width': 0, 'height': 0}
            ]
        };

        $scope.status = {
            status: "",
            address: "",
            time: ""
        };

        $scope.submitStatus = function () {
            var send_data = {con_number: $scope.track.con_number, status: $scope.status};

            DataService.post('/api/update/status', send_data)
                .then(function (data) {
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.driverForm);
                });
        };

        $scope.search = function () {
            var send_data = {con_number: $scope.con_number};

            DataService.post('/api/lookup/', send_data)
                .then(function (data) {
                    $scope.found = true;
                    $scope.driver = data;
                })
                .catch(function (error) {
                    $scope.found = false;
                    ErrorHelperService.displayInputControlError(error.message, self.searchForm);
                });
        };

        $scope.submit = function () {
            var send_data = {con_number: $scope.track.con_number};

            DataService.post('/api/update/', send_data)
                .then(function (data) {
                    $scope.track.eta = data.eta;
                    $scope.track.pickup_address = data.pickup_address;
                    $scope.track.delivery_address = data.delivery_address;
                    $scope.track.statuses = data.statuses;
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.driverForm);
                });
        };
    }

    updateDriverController.$inject = deps;
    angular.module('App').controller('UpdateDriverController', updateDriverController);
})();
