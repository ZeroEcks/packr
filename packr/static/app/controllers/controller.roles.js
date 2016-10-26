(function () {
    'use strict';

    var deps = ['DataService', 'ErrorHelperService', '$scope'];
    function rolesController(DataService, ErrorHelperService, $scope) {
        var self = this; // jshint ignore:line
        $scope.roles = {
            users: [
            ],
            roles: [
            ]
        };

        $scope.refresh = function () {
            DataService.post('/api/roles/get', {})
                .then(function (data) {
                    $scope.roles = data;
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.roleForm);
                });
        };

        $scope.update = function (id) {
            var role = null;
            for (var i = 0; i < $scope.roles.users.length; i++) {
                if ($scope.roles.users[i].id == id) {
                    role = $scope.roles.users[i].role;
                    break;
                }
            }

            var send_data = {id: id, role: role};

            DataService.post('/api/roles/update', send_data)
                .then(function (data) {
                    $scope.refresh();
                })
                .catch(function (error) {
                    ErrorHelperService.displayInputControlError(error.message, self.roleForm);
                });
        };

        $scope.refresh();
    }

    rolesController.$inject = deps;
    angular.module('App').controller('RolesController', rolesController);
})();
