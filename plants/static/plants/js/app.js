var app = angular.module('PlantsDemo', ['ui.directives', 'chart.js']);

app.config(function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{$');
	$interpolateProvider.endSymbol('$}');
});

app.factory('plantService', function ($http, $window) {
	var service = {};
	service.all = function () {
		return $http.get($window.PLANTS_URL);
	};
	service.create = function (name) {
		return $http.post($window.PLANTS_URL, { name: name });
	};
	service.delete = function (id) {
		return $http.delete($window.PLANTS_URL + id + '/');
	};
	return service;
});

app.factory('monitorService', function ($http, $window) {
	var service = {};
	service.updateData = function (params) {
		return $http.get($window.MONITOR_URL, { params: params });
	};
	return service;
});

app.factory('reportService', function ($http, $window) {
	var service = {};
	service.query = function (params) {
		return $http.get($window.REPORTS_URL, { params: params });
	};
	return service;
});

app.controller('mainCtrl', function ($scope, plantService, monitorService, reportService) {
	$scope.plants = [];
	$scope.monitor = {};
	$scope.report = {};
	$scope.chart = {
		options: { legend: { display: true } },
		series: ['Expected', 'Observed']
	};
	$scope.datepickerOpts = {
		dateFormat: 'yy-mm-dd',
		changeMonth: true,
		changeYear: true
	};

	$scope.getPlants = function () {
		plantService.all().then(function (resp) {
			$scope.plants = resp.data;
		});
	};
	$scope.createPlant = function (name) {
		plantService.create(name).then(function (resp) {
			$scope.getPlants();
		});
	};
	$scope.deletePlant = function (id) {
		plantService.delete(id).then(function (resp) {
			$scope.getPlants();
		});
	};

	$scope.updateData = function () {
		$scope.monitorBtnDisabled = true;
		monitorService.updateData($scope.monitor).then(function (resp) {
			$scope.monitorBtnDisabled = false;
		});
	};

	$scope.updateChart = function () {
		$scope.chart.labels = [];
		$scope.chart.data = [[], []];
		reportService.query($scope.report).then(function (resp) {
			resp.data.forEach(function (e) {
				$scope.chart.labels.push(e.date);
				if ($scope.reportType == 'energy') {
					$scope.chart.data[0].push(e.energy_expected);
					$scope.chart.data[1].push(e.energy_observed);
				} else if ($scope.reportType == 'irradiation') {
					$scope.chart.data[0].push(e.irradiation_expected);
					$scope.chart.data[1].push(e.irradiation_observed);
				}
			});
		});
	};

	$scope.getPlants();
});
