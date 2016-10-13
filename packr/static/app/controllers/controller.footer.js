(function () {
    'use strict';

    var deps = ['$scope', '$location', '$mdFooter'];
    function footerController($scope, $location, $mdFooter) {
        var self = this; // jshint ignore:line

    }

    footerController.$inject = deps;
    angular.module('App').controller('FooterController', footerController);
})();
