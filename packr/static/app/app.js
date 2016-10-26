(function () {
    'use strict';

    var appDeps = [
        'ngRoute',
        'ngMaterial',
        'ngMessages'
    ];
    var app = angular.module('App', appDeps);

    app.config(function ($interpolateProvider, $routeProvider, $locationProvider, $httpProvider, $mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('purple')
            .accentPalette('yellow');
        $interpolateProvider.startSymbol('//');
        $interpolateProvider.endSymbol('//');

        // Route authentication resolution method wrappers
        function requiresLogin(AuthService) {
            return AuthService.redirectIfNotAuthenticated();
        }

        function skipIfLoggedIn(AuthService) {
            return AuthService.skipIfAuthenticated();
        }

        $routeProvider
            .when('/', {
                templateUrl: 'static/views/home.html'
            })
            .when('/contact', {
                template: '<contact></contact>'
            })
            .when('/register', {
                template: '<register></register>',
                resolve: {
                    'skipIfLoggedIn': skipIfLoggedIn
                }
            })
            .when('/login', {
                template: '<login></login>',
                resolve: {
                    'skipIfLoggedIn': skipIfLoggedIn
                }
            })
            .when('/protected', {
                template: '<protected></protected>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/about', {
                templateUrl: 'static/views/about.html'
            })
            .when('/book', {
                template: '<booking></booking>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/driver', {
                template: '<driver></driver>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/quote', {
                template: '<quote></quote>'
            })
            .when('/track', {
                template: '<track></track>'
            })
            .when('/orders', {
                template: '<orders></orders>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/roles', {
                template: '<roles></roles>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/view-order', {
                template: '<vieworder></vieworder>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/process', {
                template: '<process></process>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/status', {
                template: '<status></status>',
                resolve: {
                    'requiresLogin': requiresLogin
                }
            })
            .when('/services', {
                templateUrl: 'static/views/services.html'
            })
            .when('/why-us', {
                templateUrl: 'static/views/why-us.html'
            })
            .when('/faq', {
                templateUrl: 'static/views/faq.html'
            })
            .when('/terms', {
                templateUrl: 'static/views/terms.html'
            })
            .when('/privacy', {
                templateUrl: 'static/views/privacy.html'
            })
            .otherwise({
                templateUrl: 'static/views/404.html'
            });

        $locationProvider.html5Mode(true);

        $httpProvider.interceptors.push(function ($window, $q, $location, $injector) {
            return {
                request: function (config) {
                    config.headers = config.headers || {};

                    var AuthService = $injector.get('AuthService');
                    AuthService.setAuthHeaders(config);

                    return config;
                },
                responseError: function (response) {
                    var AuthService = $injector.get('AuthService');
                    var message = response.data.description;

                    if (AuthService.isUserLoggedIn() && (response.status === 401 || response.status === 403)) {
                        AuthService.clearLocalUser();
                        $location.path('/login');
                        message = 'You must be logged in to do that.';
                    }

                    if (angular.isDefined(message)) {
                        var ToastService = $injector.get('ToastService');
                        ToastService.propagateWarningToast(message);
                    }

                    return $q.reject(response);
                }
            };
        });
    });

    app.run(function (ToastService) {
        ToastService.listenForWarningToast();
    });
})();
