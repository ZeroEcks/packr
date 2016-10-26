(function () {
    'use strict';

    var deps = ['DataService', '$location', '$mdToast'];
    function contactController(DataService, $location, $mdToast) {
        var self = this; // jshint ignore:line
        self.contact = {
            email: '',
            content: ''
        };

        self.send_message = function () {
            DataService.post('/api/contact/', self.contact)
                .then(function (result) {
                    console.log(result);
                    $mdToast.show(
                        $mdToast.simple()
                            .textContent('Message Sent!')
                            .position('left')
                            .hideDelay(3000)
                    );
                    $location.path('/');
                });
        };
    }

    contactController.$inject = deps;
    angular.module('App').controller('ContactController', contactController);
})();
