(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope', '$routeParams'];
    function viewOrderController(DataService, ErrorHelperService, $scope, $routeParams) {
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

        $scope.search = function () {
            var send_data = {con_number: $scope.con_number};

            DataService.post('/api/lookup/', send_data)
                .then(function (data) {
                    data.eta = new Date(data.eta);
                    data.pickup.date = new Date(data.pickup.date);
                    data.pickup.time = new Date("1970-01-01T" + data.pickup.time);
                    $scope.driver = data;
                    for (var i = 0; i < $scope.driver.drivers.length; i++) {
                        if ($scope.driver.drivers[i].id == $scope.driver.driver) {
                            $scope.driver.driver = $scope.driver.drivers[i].full_name;
                            break;
                        }
                    }
                    $scope.found = true;
                })
                .catch(function (error) {
                    $scope.found = false;
                    ErrorHelperService.displayInputControlError(error.message, self.searchForm);
                });
        };

        if ($routeParams.id !== undefined) {
            $scope.con_number = $routeParams.id;
            $scope.search();
        }
    }

    viewOrderController.$inject = deps;
    angular.module('App').controller('ViewOrderController', viewOrderController);
})();
