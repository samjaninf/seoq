'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', '$http', function ($scope, $http) {
	$scope.request_data = {
		'url': '',
		'keyword': ''
	}

  var csrftoken = $('#my_token').val();
	$scope.animation = false;
	$scope.startReport = function(){
		var keyword_disabled = document.getElementById('keywords').getAttribute('disabled')
		var url = '/api/start-report/';
		var data = {
			url: $scope.request_data.url,
      csrfmiddlewaretoken: csrftoken
		};
    var headers = {
      'X-CSRFToken': csrftoken
    };
		 $http.post(url, data, headers)
            .success(function (data, status) {
            	$scope.animation = true;
            	$scope.analysis_message = "we are getting your site score";
            	var obtained_pk = data.report;
            	url = '/api/site-score/';
            	data = {
            		pk: obtained_pk,
                csrfmiddlewaretoken: csrftoken
            	}

		 		$http.post(url, data, headers)
            	.success(function (data, status) {
            		var redirect_url = data.redirect_url;
            		if (keyword_disabled != null) {
            			window.location.assign(redirect_url);
            		}else{
            			$scope.analysis_message = "we are done with your site score, now we are getting your keyword phrase score";
            			url = '/api/kw-score/';
            			data = {
            				keywords: $scope.request_data.keyword,
                    csrfmiddlewaretoken: csrftoken,
            				pk: obtained_pk
            			}
            			$http.post(url, data, headers)
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
