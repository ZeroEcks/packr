(function () {
    'use strict';

    var deps = ['DataService', 'ToastService', '$location', '$scope', '$window'];
    function ordersController(DataService, ToastService, $location, $scope, $window) {
        var self = this; // jshint ignore:line
        $scope.orders = {
            orders: [

            ]
        };

        $scope.driver = angular.fromJson($window.localStorage.getItem('detailedUser')).role_id == 2;
        $scope.admin = angular.fromJson($window.localStorage.getItem('detailedUser')).role_id == 3;

        DataService.post('/api/orders/', {})
            .then(function (data) {
                $scope.orders.orders = data.orders;
            })
            .catch(function (error) {
                ToastService.createWarningToast(error.message);
            });

        $scope.newOrder = function () {
            $location.path('/book');
        };

        $scope.trackOrder = function (order) {
            $location.path('/track').search({id: order});
        };

        $scope.conNote = function (order) {
            $location.path('/view-order').search({id: order});
        };

        $scope.process = function (order) {
            $location.path('/process').search({id: order});
        };

        $scope.driverNotes = function (order) {
            $location.path('/driver').search({id: order});
        };

        $scope.statusUpdate = function (order) {
            $location.path('/status').search({id: order});
        };
    }

    ordersController.$inject = deps;
    angular.module('App').controller('OrdersController', ordersController);
})();
