(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope', '$routeParams', '$filter'];
    function trackController(DataService, ErrorHelperService, $scope, $routeParams, $filter) {
        var self = this; // jshint ignore:line
        $scope.track = {
            con_number: "",
            eta: "",
            pickup_address: "",
            delivery_address: "",
            statuses: [
            ]
        };

        $scope.submit = function () {
            var send_data = {con_number: $scope.track.con_number};

            DataService.post('/api/track/', send_data)
                .then(function (data) {
                    $scope.track.eta = $filter('date')(data.eta, 'short');
                    $scope.track.pickup_address = data.pickup_address;
                    $scope.track.delivery_address = data.delivery_address;
                    $scope.track.statuses = data.statuses;
                    for (var i = 0; i < $scope.track.statuses.length; i++) {
                        $scope.track.statuses[i].date = $filter('date')($scope.track.statuses[i].date, 'short');
                    }
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
