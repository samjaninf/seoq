'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', '$http', function ($scope, $http) {
	$scope.request_data = {'url': document.getElementById('netloc').innerHTML,
	'keyword': ''}
	$scope.obtained_keyword_score = 0;
	$scope.keyword_score = function () {
		var netloc = $scope.request_data.url;
		var keywords = $scope.request_data.keyword;
		$http.get("/api/kw-score/"+'?url='+ netloc +'&keywords=' + keywords)
		.then(function(response) {
			var obtained_site_score = document.getElementById('site_score').innerHTML;
			var obtained_keyword_score = response.data.keyword_score;
			document.getElementById('kw_score').innerHTML = parseInt(obtained_keyword_score)
			document.getElementById('total_score').innerHTML = parseInt(obtained_keyword_score) +
				parseInt(obtained_site_score)
		});
	};
}]);