(function () {
    'use strict';

    var deps = ['DataService', 'AuthService', '$location'];
    function loginController(DataService, AuthService, $location) {
        var self = this; // jshint ignore:line
        self.user = {
            email: '',
            password: ''
        };

        self.login = function () {
            DataService.post('/api/user/auth', self.user)
                .then(function (result) {
                    var parsedToken = AuthService.parseToken(result.access_token);
                    AuthService.setLocalUser(result.access_token, parsedToken.firstname);
                    $location.path('/');
                });
        };
    }

    loginController.$inject = deps;
    angular.module('App').controller('LoginController', loginController);
})();
