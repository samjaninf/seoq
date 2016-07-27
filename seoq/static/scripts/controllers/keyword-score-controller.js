'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', '$http', function ($scope, $http) {
	console.log('worked!')
	$scope.request_data = {'url': '', 'keyword': ''}
	$scope.keyword_score = function () {
		var netloc = $scope.request_data.url;
		var keywords = $scope.request_data.keyword;
		$http.get("/api/kw-score/"+'?url='+ netloc +'&keywords=' + keywords)
		.then(function(response) {
			$scope.myWelcome = response.data;
		});
	};
}]);