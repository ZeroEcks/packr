(function () {
    'use strict';

    var deps = ['$location', '$scope'];
    function bookingController($location, $scope) {
        var self = this; // jshint ignore:line
        $scope.booking = {
            type: "",
            dangerous: "none",
            requirePickup: "no",
            pickup: {
                businessName: "",
                contactName: "",
                phone: "",
                email: "",
                street: "",
                suburb: "",
                state: "",
                postCode: "",
                date: "",
                time: ""
            },
            delivery: {
                businessName: "",
                contactName: "",
                phone: "",
                email: "",
                street: "",
                suburb: "",
                state: "",
                postCode: "",
                date: "",
                time: ""
            },
            fragile: "",
            paymentType: "",
            customerComments: "",
            packages: [
                {'weight': 0, 'length': 0, 'width': 0, 'height': 0}
            ]
        };

        $scope.submit = function () {
            console.log($scope.booking);
        };

        $scope.addPackage = function () {
            $scope.booking.packages.push({'weight': 0, 'length': 0, 'width': 0, 'height': 0});
        };

        $scope.removePackage = function (index) {
            $scope.booking.packages.splice(index, 1);
        };
    }

    bookingController.$inject = deps;
    angular.module('App').controller('BookingController', bookingController);
})();
