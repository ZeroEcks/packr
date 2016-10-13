(function () {
    'use strict';

    var deps = ['$scope', '$location'];
    function footerController($scope, $location) {
        var self = this; // jshint ignore:line

        self.goAbout = function () {
            $location.path('/about');
        };
    }

    footerController.$inject = deps;
    angular.module('App').controller('FooterController', footerController);
})();
