(function () {
    'use strict';

    var deps = ['DataService', 'ToastService', '$location', '$scope'];
    function ordersController(DataService, ToastService, $location, $scope) {
        var self = this; // jshint ignore:line
        $scope.orders = {
            orders: [

            ]
        };

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
    }

    ordersController.$inject = deps;
    angular.module('App').controller('OrdersController', ordersController);
})();
