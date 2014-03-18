var app = angular.module('myApp', []);

app.factory('portfolio', function($http, $q) {
	
	var portfolio = {};
	
	var init = function () {
		var deferred = $q.defer();
	
		$http.get('user/').success(function(data, status, headers, config) {
				         this.cash_balance = data.cash_balance;
						 this.user_id = data.id
						 this.purchases = data.purchases;
						 deferred.resolve(this)
					 
			        }); 
			
		return deferred.promise
	}
	
	var place_order = function (order) {
	  var order_deferred = $q.defer();	
	  $http.post('/new_transaction/', order).success(
		    function (portfolio) {
				    if (portfolio.success) {
					    
						this.cash_balance = portfolio.cash_balance 
						this.purchases = portfolio.purchases;
						order_deferred.resolve(this)
						
				    }
				    
				   }

	        );
	   return  order_deferred.promise
	}
	
	portfolio.init = init
	portfolio.place_order = place_order
	return portfolio
      
});
			
			
app.controller('PortfolioController', function($scope, $http, portfolio) {
	portfolio.init().then(function(portfolio){
		$scope.cash_balance = portfolio.cash_balance 
		$scope.purchases = portfolio.purchases;
	})
	$scope.stock = {ticker: '', units: ''};
	
	var transact = function (order) {
		portfolio.place_order(order).then(function(portfolio){
		    if (portfolio.success) {
		    
				$scope.cash_balance = portfolio.cash_balance 
				$scope.purchases = portfolio.purchases;
				$scope.message = "you've just transacted for " + order.units + ' units of ' + order.ticker + ' (' + order.type + ') '
				$scope.stock = {ticker: '', units: ''};
		    }
			else {
				$scope.message = 'sorry, your order couldn"t be placed'
			}
		})
	}

 	$scope.requestQuote = function () {
		 var order = {ticker: $scope.stock.ticker, units: $scope.stock.units}; 
		 $scope.stock = {ticker: '', units: ''}; 
		 $scope.message = 'Placing BUY order for ' + order.units + ' of ' + order.ticker + ' please wait '
		 order.type = 'buy'
		 transact(order)
 	  						  
 	  						  }
	$scope.sellOrder = function (stock) {
		 var order = {ticker: stock.ticker, units: stock.units, id:stock.id};
		 $scope.message = 'Placing SELL order for ' + order.units + ' of ' + order.ticker + ' please wait '
		 order.type = 'sell'
		 transact(order)
						  	}
	
	});
			  

