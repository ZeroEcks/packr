(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope'];
    function updateDriverController(DataService, ErrorHelperService, $scope) {
        var self = this; // jshint ignore:line
        $scope.con_number = '';
        $scope.found = false;

        $scope.driver = {
            driver: -1,
            type: "",
            dangerous: "none",
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
            adminComments: "",
            customerComments: "",
            cost: 0,
            eta: "",
            statuses: [
            ],
            packages: [
            ],
            drivers: [
            ]
        };

        $scope.status = {
            status: "",
            address: ""
        };

        $scope.submitStatus = function () {
            var send_data = {con_number: $scope.con_number, status: $scope.status};
            send_data.status = JSON.stringify(send_data.status);

            DataService.post('/api/update/status', send_data)
                .then(function (data) {
                    $scope.search(); //Update the form.
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.statusForm);
                });
        };

        $scope.search = function () {
            var send_data = {con_number: $scope.con_number};

            DataService.post('/api/lookup/', send_data)
                .then(function (data) {
                    data.eta = new Date(data.eta);
                    data.pickup.date = new Date(data.pickup.date);
                    data.pickup.time = new Date("1970-01-01T" + data.pickup.time);
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
                cost: $scope.driver.cost,
                adminComments: $scope.driver.adminComments
            };

            DataService.post('/api/update/driver', send_data)
                .then(function (data) {
                    $scope.search(); //Update the form.
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.driverForm);
                });
        };
    }

    updateDriverController.$inject = deps;
    angular.module('App').controller('UpdateDriverController', updateDriverController);
})();
