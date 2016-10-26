(function () {
    'use strict';

    var deps = ['$scope', '$location', '$mdSidenav', '$window'];
    function sidenavController($scope, $location, $mdSidenav, $window) {
        var self = this; // jshint ignore:line

        $scope.admin = angular.fromJson($window.localStorage.getItem('detailedUser')).role_id == 3;

        $scope.$on('toggleLeft', function(event, mass) { buildToggler('left')();});
        function buildToggler(componentId) {
            return function() {
                $mdSidenav(componentId).toggle();
            };
        }

        self.goServices = function () {
            $location.path('/services');
        };

        self.goWhyUs = function () {
            $location.path('/why-us');
        };

        self.goContact = function () {
            $location.path('/contact');
        };

        self.goQuote = function () {
            $location.path('/quote');
        };

        self.goTrack = function () {
            $location.path('/track');
        };

        self.goBook = function () {
            $location.path('/book');
        };

        self.goOrders = function () {
            $location.path('/orders');
        };

        self.goHome = function () {
            $location.path('/');
        };

        self.goRoles = function () {
            $location.path('/roles');
        };
    }

    sidenavController.$inject = deps;
    angular.module('App').controller('SidenavController', sidenavController);
})();
