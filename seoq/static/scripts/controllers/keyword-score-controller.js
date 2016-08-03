'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', '$http', '$httpProvider', function ($scope, $http, $httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      $scope.request_data = {
		'url': '',
		'keyword': ''
	}
	$scope.animation = false;
	$scope.startReport = function(){
		var keyword_disabled = document.getElementById('keywords').getAttribute('disabled')
		var url = '/api/start-report/';
		var data = {
			url: $scope.request_data.url
		};
		 $http.post(url, data)
            .success(function (data, status) {
            	$scope.animation = true;
            	$scope.analysis_message = "we are getting your site score";
            	var obtained_pk = data.report;
            	url = '/api/site-score/';
            	data = {
            		pk: obtained_pk
            	}
		 		$http.post(url, data)
            	.success(function (data, status) {
            		var redirect_url = data.redirect_url;
            		if (keyword_disabled != null) {
            			window.location.assign(redirect_url);
            		}else{
            			$scope.analysis_message = "we are done with your site score, now we are getting your keyword phrase score";
            			url = '/api/kw-score/';
            			data = {
            				keywords: $scope.request_data.keyword,
            				pk: obtained_pk
            			}
            			$http.post(url, data)
            			.success(function (data, status) {
            				var redirect_url = data.redirect_url;
            				window.location.assign(redirect_url);
            			}).error(function (data, status) {

            			});
            		};
            	}).error(function (data, status) {

            	});
            })
            .error(function (data, status) {

            });
	}
}]);