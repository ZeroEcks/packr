(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$location', '$scope'];
    function bookingController(DataService, ErrorHelperService, $location, $scope) {
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
                postCode: ""
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
            var modified_booking = angular.copy($scope.booking);

            modified_booking.pickup.dateTime = new Date(
                modified_booking.pickup.date.getFullYear(),
                modified_booking.pickup.date.getMonth(),
                modified_booking.pickup.date.getDate(),
                modified_booking.pickup.time.getHours(),
                modified_booking.pickup.time.getMinutes(),
                modified_booking.pickup.time.getSeconds(),
                modified_booking.pickup.time.getMilliseconds()
            );

            modified_booking.packages = JSON.stringify(modified_booking.packages);
            modified_booking.delivery = JSON.stringify(modified_booking.delivery);
            modified_booking.pickup = JSON.stringify(modified_booking.pickup);

            DataService.post('/api/book/', modified_booking)
                .then(function (data) {
                    $location = '/';
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.quoteForm);
                });
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
