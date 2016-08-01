'use strict';

/**
 * @ngdoc overview
 * @name seoq
 * @description
 * # seoq
 *
 * Main module of the application.
 */
var app = angular
  .module('seoq', []);

app.config(function($httpProvider) {
$httpProvider.defaults.xsrfCookieName = 'csrftoken';
$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
$httpProvider.defaults.withCredentials = true;
});