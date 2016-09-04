(function () {
    'use strict';

    var deps = ['AuthService', '$location', '$rootScope', '$scope'];
    function navbarController(AuthService, $location, $rootScope, $scope) {
        var self = this; // jshint ignore:line
        $scope.toggleLeft = function(){$rootScope.$broadcast('toggleLeft', 'lmao');};

        self.userLoggedIn = function () {
            return AuthService.isUserLoggedIn();
        };

        self.goLogin = function () {
            $location.path('/login');
        };

        self.goRegister = function () {
            $location.path('/register');
        };

        self.logout = function () {
            AuthService.logoutUser();
        };
    }


    navbarController.$inject = deps;
    angular.module('App').controller('NavbarController', navbarController);
})();
