(function () {
    'use strict';

    var deps = ['$scope', '$location', '$mdSidenav'];
    function sidenavController($scope, $location, $mdSidenav) {
        var self = this; // jshint ignore:line

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

        self.goHome = function () {
            $location.path('/');
        };
    }

    sidenavController.$inject = deps;
    angular.module('App').controller('SidenavController', sidenavController);
})();
