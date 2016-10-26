(function () {
    'use strict';

    var deps = ['$scope', '$location'];
    function footerController($scope, $location) {
        var self = this; // jshint ignore:line

        self.goAbout = function () {
            $location.path('/about');
        };

        self.goFAQ = function () {
            $location.path('/faq');
        };

        self.goTerms = function () {
            $location.path('/terms');
        };

        self.goPrivacy = function () {
            $location.path('/privacy');
        };
    }

    footerController.$inject = deps;
    angular.module('App').controller('FooterController', footerController);
})();
