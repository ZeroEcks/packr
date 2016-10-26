(function () {
    'use strict';

    var deps = ['DataService', 'ToastService', '$window', '$q', '$location'];
    function authService (DataService, ToastService, $window, $q, $location) {
        return {
            parseToken: parseToken,
            setLocalUser: setLocalUser,
            clearLocalUser: clearLocalUser,
            isUserLoggedIn: isUserLoggedIn,
            redirectIfNotAuthenticated: redirectIfNotAuthenticated,
            skipIfAuthenticated: skipIfAuthenticated,
            setAuthHeaders: setAuthHeaders,
            logoutUser: logoutUser
        };

        function parseToken(token) {
            var base64Url = token.split('.')[1];
            var base64 = base64Url.replace('-', '+').replace('_', '/');
            return JSON.parse($window.atob(base64));
        }

        function isUserLoggedIn() {
            var userInfo = angular.fromJson($window.localStorage.getItem('user'));
            return (angular.isObject(userInfo) && angular.isDefined(userInfo.token));
        }

        function setLocalUser(token, firstname) {
            $window.localStorage.setItem('user', angular.toJson({
                token: token,
                firstname: firstname,
            }));
            DataService.get('/api/user', self.user)
                .then(function(result) {
                    $window.localStorage.setItem('detailedUser', result);
            });
        }

        function setAuthHeaders(config) {
            var userInfo = angular.fromJson($window.localStorage.getItem('user'));
            if (angular.isObject(userInfo) && angular.isDefined(userInfo.token)) {
                config.headers.Authorization = 'JWT ' + userInfo.token;
            }
        }

        function clearLocalUser() {
            $window.localStorage.removeItem('user');
        }

        function redirectIfNotAuthenticated() {
            var deferred = $q.defer();

            if (isUserLoggedIn()) {
                deferred.resolve();
            } else {
                $location.path('/login');
                ToastService.propagateWarningToast('You must be logged in to do that.');
            }

            return deferred.promise;
        }

        function skipIfAuthenticated() {
            var deferred = $q.defer();

            if (isUserLoggedIn()) {
                $location.path('/');
            } else {
                deferred.resolve();
            }

            return deferred.promise;
        }

        function logoutUser() {
            var userInfo = angular.fromJson($window.localStorage.getItem('user'));
            if (angular.isObject(userInfo) && angular.isDefined(userInfo.token)) {
                $window.localStorage.removeItem('user');
                $window.localStorage.removeItem('detailedUser');
                $location.path('/');
            }
        }
    }

    authService.$inject = deps;
    angular.module('App').factory('AuthService', authService);
})();