(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$location', '$scope'];
    function quoteController(DataService, ErrorHelperService, $location, $scope) {
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
            ],
            result: 0
        };

        $scope.submit = function () {
            var modified_quote = angular.copy($scope.quote);

            modified_quote.packages = JSON.stringify(modified_quote.packages);

            DataService.post('/api/quote/', modified_quote)
                .then(function (data) {
                    $scope.quote.result = data.quote;
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.quoteForm);
                });
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
