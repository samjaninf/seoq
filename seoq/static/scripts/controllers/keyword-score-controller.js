'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', function ($scope, Validation) {
	console.log('worked!')
	$scope.keyword_score = function (netloc, keyword) {
		Validation.get({url: $scope.myurl}, function(data) {
			$scope.validate = data.valid_url;
		});
	};
}]);