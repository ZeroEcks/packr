(function () {
    'use strict';

    var deps = ['$scope', '$location'];
    function homeController($scope, $location) {
        var self = this; // jshint ignore:line

        $scope.goAbout = function () {
            $location.path('/about');
        };

        $scope.goFAQ = function () {
            $location.path('/faq');
        };

        $scope.goServices = function () {
            $location.path('/services');
        };

        $scope.goWhyUs = function () {
            $location.path('/why-us');
        };

        $scope.goTrack = function () {
            $location.path('/track');
        };

        $scope.goBook = function () {
            $location.path('/book');
        };

        $scope.goOrders = function () {
            $location.path('/orders');
        };
    }

    homeController.$inject = deps;
    angular.module('App').controller('HomeController', homeController);
})();
