'use strict';

var kbox = angular.module('kinderboxApp', ['ngResource']);

//Set constant to use gloablly
kbox.constant('KINDERBOX_IP','10.0.0.47');

kbox.config(function ($routeProvider, $provide) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl' //display dasboard info
      })
      .when('/albums', {
        templateUrl: 'views/albums.html',
        controller: 'ShowAlbumCtrl'
      })
      .when('/new-playlist', {
        templateUrl: 'views/new_playlist.html',
        controller: 'PlaylistCtrl'
      })
      .when('/new-rfid', {
        templateUrl: 'views/new_rfid.html',
        controller: 'RfidCtrl'
      })
      .when('/match-rfid', {
        templateUrl: 'views/matching_rfid.html',
        controller: 'MatchRfidCtrl'
      })
      .when('/rfid-status', {
        templateUrl: 'views/rfid_status.html',
        controller: 'RfidStatusCtrl'
      })
      .when('/help', {
        templateUrl: 'views/help.html',
        controller: 'HelpCtrl'
      })
      .otherwise({
        redirectTo: '/'
      });

    //$provide.value('kinderboxIp', '10.0.0.47'); //geht auch
    //$provide.factory('kinderboxIP', function() { return '10.0.0.47'; });
      
  });


kbox.service('myFaye', function (KINDERBOX_IP) {
  //$faye("http://10.0.0.47:9292/faye") //set faye url in one place
  var faye = new Faye.Client('http://' + KINDERBOX_IP + ':9292/faye');
  return faye;
});

//Services = angular.module('kinderboxApp.Services', [] );
kbox.service('playlistAlbumService', function ($http, KINDERBOX_IP) {
  this.getAlbums = function() {
    console.log('Search Clicked here');
    //return $http.jsonp('http://10.0.0.47/cgi-bin/getRFID2.py');
    //http://10.0.0.47/cgi-bin/json-data-example.json
    //return $http.get('http://10.0.0.47/cgi-bin/json-data-example.json');
    return $http.get('http://' + KINDERBOX_IP + '/cgi-bin/getItem.py');
    //return $http.jsonp('http://www.reddit.com/user/spilcm/comments/.json&jsonp=JSON_CALLBACK');
    //return $http.jsonp('http://www.reddit.com/search.json?q=angularjs&jsonp=JSON_CALLBACK'); //OK
    //return $http.jsonp('http://www.reddit.com/search.json?q=angularjs'); //NOT OK, callback is missing.
  };

});

kbox.service('kinderboxAPI', function ($http, KINDERBOX_IP) {
  console.log('kinderboxAPI');

  return {
      deleteAlbum: function(obj, callback) {
        console.log('API call: deleteAlbum', obj);

        //Call server to delete here
        //http://10.0.0.47/cgi-bin/deleteAlbum.py?rfid=12234
        $http.post('http://' + KINDERBOX_IP + '/cgi-bin/deleteItem.py', obj)
        //$http.get('http://10.0.0.47/cgi-bin/getItem.py')
          .success(function(data, status, headers, config) {
             console.log("yay, success...", status, data);

             //execute the function defined in the callback
             callback("Delete Album successful");

          });

        return;
        
      },

      enableKinderbox: function(callback) {


        $http.get('http://' + KINDERBOX_IP + '/cgi-bin/enableKinderbox.py')
          .success(function(data, status, headers, config) {
             console.log("yay, success...", status, data);

             //execute the function defined in the callback
             callback("Enable kindrbox successful");

          });

        return;

      },

      sayHello: function() {
        console.log('API call: sayHello');
      }
  } 


});

//same as service
kbox.factory('kinderboxAPIprovider', function ($http, KINDERBOX_IP) {
  console.log('kinderboxAPIprovider');

  return {
      deleteAlbum: function(obj, callback) {
        console.log('API call: deleteAlbum', obj);
        //Call server to delete here
        //http://10.0.0.47/cgi-bin/deleteAlbum.py?rfid=12234
        //$http.post('http://10.0.0.47/cgi-bin/getItem.py', obj)
        $http.get('http://' + KINDERBOX_IP + '/cgi-bin/getItem.py')
          .success(function(data, status, headers, config) {
             console.log("yay, success...", status);
             //execute the function defined in the callback
             callback("Delete Album successful");
          });

        return;
        
      },



      getRFIDinfo: function() {
        //return $http.get('http://10.0.0.47/cgi-bin/getRFID.py');
        //optinaly we can handle the call here as well.

      },

      getstatus: function () {

      },

      sayHello: function() {
        console.log('API call: sayHello');
      }
  }  

});




kbox.service('rfidInfoService', function ($http, KINDERBOX_IP) {
  this.getInfo = function() {
    console.log('rfidInfoService');
    return $http.get('http://' + KINDERBOX_IP + '/cgi-bin/getRFID.py');
  };
});

kbox.service('myTodoListService', function() {
  var todo = [];

  this.add = function(msg) {
    todo.push(msg);
  };
  this.get = function() {
    //todo.pull();
    return todo;
  };

});


kbox.service('statusService', function (playlistAlbumService, rfidInfoService, myTodoListService) {
  this.getStatus = function() {
    console.log('Get status service.');

    var kinderboxStatus = {};
    var remember = 0;

    playlistAlbumService.getAlbums()
      .success(function(data, status, headers, config) {
        var musicAlbums = data.data;
        console.log('statusService musicAlbums results: ', status, data.data);
        

        var playableAlbums = 0;
        var notplayable = 0;

        //$scope.musicAlbums.each do 
        //_.each(musicAlbums, alert("found item"));
        notplayable = _.where(musicAlbums, {rfid: null }).length;
        console.log('Not playable: ', notplayable)

        kinderboxStatus.notplayable = notplayable;
        kinderboxStatus.playable = musicAlbums.length - notplayable;
        kinderboxStatus.usedRFID = kinderboxStatus.playable;
        kinderboxStatus.requestRFID = kinderboxStatus.notplayable;

        //add to todo list
        if(notplayable > 0 && notplayable != remember) {
          myTodoListService.add("Please update your kinderbox, there are " + notplayable + " new album wating for RFID.");
          remember = notplayable; //need this variable to avoid adding same message anytime the user refresh.
        }


      })
      .error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        console.log('playlistAlbumService response with an error', status);
      });

    return kinderboxStatus;

  };


});


kbox.service('rfidStatusService', function (rfidInfoService) {
  this.getRFIDStatus = function() {
    console.log('Get RFID status service.');

    var rfidStatus = {};

    rfidInfoService.getInfo()
      .success(function(data, status, headers, config) {
        var items = data.data;
        console.log('rfidStatusService results: ', status, data.data);
        
        var freeRFID = 0;
        var usedRFID = 0;

        freeRFID = _.where(items, {free: 'yes'}).length;
        usedRFID = _.where(items, {free: 'no'}).length;

        rfidStatus.total = items.length;
        rfidStatus.freeRFID = freeRFID;
        rfidStatus.usedRFID = usedRFID;

      })
      .error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        console.log('playlistAlbumService response with an error', status);
      });

    return rfidStatus;

  };


});



//start the RFID scan service from RaspBerry PI
kbox.service('rfidService', function ($http, KINDERBOX_IP) {
  this.startRFIDScan = function() {
    console.log('start RFID scan service in Pi.');
    return $http.get('http://' + KINDERBOX_IP + '/cgi-bin/enableScanRFID.py');
  };

});


//calling the update service from pi.
kbox.service('updateKinderboxService', function ($http, KINDERBOX_IP) {
  this.startUpdateKinderbox = function() {
    console.log('start updateting the kinderbox with new album and rfid number in Pi.');
    return $http.get('http://' + KINDERBOX_IP + '/cgi-bin/mappingAlbumWithRFID.py');
    //simulation: using for UX development, prevent real request to server
    //return $http.get('http://10.0.0.47/cgi-bin/getRFID.py');
  };

});


kbox.directive('rfidItems', function() {
  return {
    scope: {
      barcode : '@',
      rfid : '@',
      title: '@',
      cover: '@'
    },
    restrict: 'E',
    templateUrl: 'views/rfid-search-results.html'
  };

});

kbox.directive('modalbody', function(KINDERBOX_IP) {
  return {
    scope: {
      title: '@',
      barcode: '@',
      id: '@',
      created: '@'
    },
    restrict: 'E',
    template: '<h4> {{ title }} </h4>' + 
              '<img ng-src="http://' + KINDERBOX_IP + '/images/{{barcode}}/cover.jpg" class="img-polaroid" style="width: 80px;"/>'
  };

});




kbox.directive('uploader2', [function() {

  return {
    restrict: 'E',
    scope: {
      action: '@'
    },

    controller: ['$scope', function ($scope) {

      $scope.progress = 0;
      $scope.avatar = '';
      $scope.uploadDone = false;
      $scope.filename = '';


      $scope.sendFile = function(el) {
        $scope.uploadDone = false;
        console.log('I will send file..');
        console.info(el);
        var $form = $(el).parents('form');
        
        if ($(el).val() === '') {
          return false;
        }

        var fname = $(el).val().split('\\');
        $scope.filename = fname[fname.length-1];
        console.log('filename: ', $scope.filename);
        $scope.filesize = 0;

        $form.attr('action', $scope.action);
        console.log('The scope action: ', $scope.action, $form);
        $scope.$apply(function() {
          $scope.progress = 0;
        });

        $form.ajaxSubmit({
          //console.log("calling ajaxSubmit");
          type: 'POST',
          uploadProgress: function(event, position, total, percentComplete) { 
            $scope.filesize = (total/1000/1000).toFixed(2);//OK
            //$scope.filesize = Math.ceil(total/1000/1000);
            //$scope.filesize = Math.round(total / 1000 / 1000) ;
            //$scope.filesize = Math.pow(total, 1);
            $scope.$apply(function() {
              // upload the progress bar during the upload
              $scope.progress = percentComplete;
              //console.log("uploadProgress: ", event, percentComplete)
            });

            if (percentComplete === 100){
              console.log('percentComplete is done!');
            }

          },
          error: function(event, statusText, responseText, form) { 
            // remove the action attribute from the form
            $form.removeAttr('action');
            console.log('ajaxSubmit, error, somehting happpend.');

            /*
              handle the error ...
            */

          },
          success: function(responseText, statusText, xhr, form) { 
            console.log('ajaxSubmit, success, OK.', responseText, statusText );

            //$scope.notify = "Everything OK!"
            $scope.uploadDone = true;
            //reset to 0 so the spinner will not show.
            $scope.progress = 0;

            var ar = $(el).val().split('\\'), 
            filename =  ar[ar.length-1];
            //console.log("filename: ", filename);

            // remove the action attribute from the form
            $form.removeAttr('action');

            $scope.$apply(function() {
              $scope.avatar = filename;
            });

          },
      
        });

      };

    }],

    link: function(scope, elem, attrs, ctrl) {
      //console.log("Link:", attrs );
      // elem.find('.fake-uploader').click(function() {
      //   elem.find('input[type="file"]').click();
      // });

    },

    replace: false,    
    
    templateUrl: 'views/uploader.html'

  };

}]);




//JSON_CALLBACK({"data": [{"barcode": "2", "name": "test", "rfid": "8699286"}, {"barcode": "137714512109", "name": "None", "rfid": "6853105"}, {"barcode": "137714513012", "name": "None", "rfid": "5202766"}]})
//KHoa, NOTE: must set this in  /etc/lighttpd/lighttpd.conf
// server.modules = (
//         "mod_access",
//         "mod_alias",
//         "mod_cgi",
//         "mod_compress",
//         "mod_redirect",
//         "mod_setenv",
//         "mod_status",
// #       "mod_rewrite",
// )
//setenv.add-response-header = ( "Access-Control-Allow-Origin" => "*", "Access-Control-Allow-Headers" => "X-Requested-With" )
