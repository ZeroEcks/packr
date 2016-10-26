(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$location', '$scope'];
    function ordersController(DataService, ErrorHelperService, $location, $scope) {
        var self = this; // jshint ignore:line
        $scope.orders = {
            orders: [

            ]
        };

        DataService.post('/api/orders/', {})
            .then(function (data) {
                $scope.orders.orders = data.orders;

                console.log($scope.orders);
            })
            .catch(function (error) {
                ErrorHelperService.displayInputControlError(error.message, self.trackForm);
            });

        $scope.newOrder = function () {
            $location.path('/book');
        };

        $scope.trackOrder = function (order) {
            $location.path('/track?id=' + order);
        };
    }

    ordersController.$inject = deps;
    angular.module('App').controller('OrdersController', ordersController);
})();
