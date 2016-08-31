(function () {
    'use strict';

    function sidenavController($scope, $timeout, $mdSidenav, $log) {
        $scope.$on('toggleLeft', function(event, mass) { buildToggler('left')();});
        function buildToggler(componentId) {
            return function() {
                $mdSidenav(componentId).toggle();
            };
        }
    }

    angular.module('App').controller('SidenavController', sidenavController);
})();
