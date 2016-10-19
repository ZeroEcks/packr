(function () {
    'use strict';

    var deps = ['$location', '$scope'];
    function quoteController($location, $scope) {
        var self = this; // jshint ignore:line
        $scope.quote = {
            businessName: "",
            contactName: "",
            phone: "",
            email: "",
            type: "",
            dangerous: "none",
            street: "",
            suburb: "",
            state: "",
            postCode: "",
            packages: [
                {'weight': 0, 'length': 0, 'width': 0, 'height': 0}
            ]
        };

        $scope.submit = function () {
            console.log($scope.quote);
        };

        $scope.addPackage = function () {
            $scope.quote.packages.push({'weight': 0, 'length': 0, 'width': 0, 'height': 0});
        };

        $scope.removePackage = function (index) {
            $scope.quote.packages.splice(index, 1);
        };
    }

    quoteController.$inject = deps;
    angular.module('App').controller('QuoteController', quoteController);
})();
