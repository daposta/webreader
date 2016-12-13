angular.module("getbookmarks.services", ["ngResource", 'tangcloud']).
    factory('Word', function ($resource) {
        var Word = $resource('/api/v1/words/');
        Word.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return Word;
    });

angular.module("getbookmarks", ["getbookmarks.services"]).
    config(function ($routeProvider) {
        $routeProvider
            .when('/', {templateUrl: '/static/views/stories/list.html', controller: WordListController})
            .when('/words/new', {templateUrl: '/static/views/stories/create.html', controller: WordCreateController})
            //.when('/words/:storyId', {templateUrl: '/static/views/stories/detail.html', controller: StoryDetailController});
    });

function WordListController($scope, Word) {
    $scope.words = Word.query();
    
}

function WordCreateController($scope, $routeParams, $location,  $http) {

    

    $scope.save = function () {
       
         console.log($scope);
         var payload = {'url': $scope.word.url
         }; 
         console.log(payload);

         $http({method:'POST', url: '/api/v1/words', data:payload})
        .then(function(response) {
            toastr.success("Submitted New URL");
            console.log(response)
            $scope.words = response.data;
        },  function errorCallback(err){
             
          
             });


        //  $scope.word.$save(function (word, headers) {
        //     toastr.success("Submitted New Story");
        //     console.log(word);
        //     console.log(headers);
        //     //$location.path('/');
        // });
    	
    };
}


function StoryDetailController($scope, $routeParams, $location, Story) {
    var storyId = $routeParams.storyId;
    
    $scope.story = Story.get({storyId: storyId});

}
