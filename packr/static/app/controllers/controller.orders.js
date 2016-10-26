(function () {
    'use strict';

    var deps = ['DataService', 'ToastService', '$location', '$scope', '$window', '$filter'];
    function ordersController(DataService, ToastService, $location, $scope, $window, $filter) {
        var self = this; // jshint ignore:line
        $scope.orders = {
            orders: [

            ]
        };

        if ($window.localStorage.getItem('detailedUser') !== null) {
            $scope.driver = angular.fromJson($window.localStorage.getItem('detailedUser')).role_id == 2;
            $scope.admin = angular.fromJson($window.localStorage.getItem('detailedUser')).role_id == 3;
        }

        DataService.post('/api/orders/', {})
            .then(function (data) {
                for (var i = 0; i < data.orders.length; i++) {
                    data.orders[i].createdAt = $filter('date')(data.orders[i].createdAt, 'short');
                    data.orders[i].lastUpdate = $filter('date')(data.orders[i].lastUpdate, 'short');
                }
                $scope.orders.orders = data.orders;
            })
            .catch(function (error) {
                ToastService.propagateWarningToast(error.message);
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
