'use strict';

angular.module('seoq').controller('keywordScoreController',	['$scope', '$http', function ($scope, $http) {
	$scope.request_data = {
		'url': '',
		'keyword': ''
	}

  var csrftoken = $('#my_token').val();
  $scope.animation = false;
  $scope.bad_status_code = false;
  $scope.bad_url = true;
  $scope.validate_url = function(qscraper_url){
    console.log(qscraper_url)
    var qscraper_var = qscraper_url + '/api/validation/url/?url='
    $http({
      method: 'GET',
      url: qscraper_var + $scope.request_data.url,
    }).success(function(data, status){
      $scope.bad_url = !data.valid_url;
      $scope.bad_status_code = $scope.bad_url;
      if ($scope.bad_url) {
          $scope.bad_status_code = true;
          $scope.status_message = 'Invalid url. Try adding www.'
      };
    }).error(function(data, status){

    });
  }
  $scope.startReport = function(qscraper_url, username){
    var keyword_disabled = document.getElementById('keywords_input').getAttribute('disabled');
		var url = qscraper_url + '/api/seoq-tool/start-report/';
    document.getElementById('how-website').className = "animation-line";
		var data = {
			url: $scope.request_data.url,
		};
    if ($scope.request_data.keyword) {
      data.keywords = $scope.request_data.url;
    }
    if (username) {
      data.username = username;
    }
    $http({
      method: 'POST',
      url: url,
      data: data
    }).success(function (data, status) {
      $scope.animation = true;
      $scope.bad_status_code = false;
      $scope.analysis_message = "we are getting your site score. It'll take some minutes to finish";
      var obtained_pk = data.report;
      url = qscraper_url + '/api/seoq-tool/report-status/' + obtained_pk;
      setInterval(function(){
        $http({
          method: 'GET',
          url: url
        }).success(function (data, status) {
                var redirect_url = data.redirect_url;
                if (data.site_report && (keyword_disabled != null || !$scope.request_data.keyword)) {
                  window.location.assign('/www' + redirect_url);
                }else if(data.site_report && !data.keyword_report){
                  $scope.analysis_message = "we are done with your site score, now we are getting your keyword phrase score. It'll take some minutes to finish"
                }
                else if(data.site_report && data.keyword_report){
                  window.location.assign('/www' + redirect_url);
                }
              }).error(function (data, status) {

              });
      }, 2000);
    }).error(function (data, status) {
      if (status==400) {
        $scope.bad_status_code = true;
        if (data.error == 404) {
          $scope.status_message = 'the page you request does not exist'
        }
        if (data.error == 403) {
          $scope.status_message = 'the page you request does not allow to be access. Please, verify it is a public url'
        }
        if (data.error == 500) {
          $scope.status_message = 'the page you request returned a 500 error. Please, check everything is all right with your server'
        }
      }
    });
  }
}]);
