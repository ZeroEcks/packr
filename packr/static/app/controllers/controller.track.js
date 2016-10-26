(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope', '$routeParams'];
    function trackController(DataService, ErrorHelperService, $scope, $routeParams) {
        var self = this; // jshint ignore:line
        $scope.track = {
            con_number: "",
            eta: "",
            pickup_address: "",
            delivery_address: "",
            statuses: [
                {'status': "", 'date': 0, 'address': ""}
            ]
        };

        $scope.submit = function () {
            var send_data = {con_number: $scope.track.con_number};

            DataService.post('/api/track/', send_data)
                .then(function (data) {
                    $scope.track.eta = data.eta;
                    $scope.track.pickup_address = data.pickup_address;
                    $scope.track.delivery_address = data.delivery_address;
                    $scope.track.statuses = data.statuses;
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.trackForm);
                });
        };

        if ($routeParams.id !== undefined) {
            $scope.track.con_number = $routeParams.id;
            $scope.submit();
        }
    }

    trackController.$inject = deps;
    angular.module('App').controller('TrackController', trackController);
})();
