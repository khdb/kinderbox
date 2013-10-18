'use strict';

//kbox = angular.module('kinderboxApp')

//This is the dashboard controller
//inform the user about kinderbox status, i.e. number of albums, number of more RFID needed...
kbox.controller('MainCtrl', function ($scope, statusService, rfidStatusService, myTodoListService, kinderboxAPI, KINDERBOX_IP) {

    console.log("We are in MainCtrl", KINDERBOX_IP);

    $scope.needNewRfid = 0; 
    $scope.status = statusService.getStatus();
    var rfidStatus = rfidStatusService.getRFIDStatus();

    $scope.rfidStatus = rfidStatus;

    //$scope.status.playable = 18;
    //$scope.status.available = 24;

    $scope.todos = [];
    //$scope.todos.push("add more rfid cards");
    $scope.todos = myTodoListService.get();
    // if ($scope.todos.length === 0) {
    //   $scope.todos.push("Nothing to do, enjoy Kinderbox :-)!");
    // };


    
    $scope.enableKinderbox = function() {

      var API = kinderboxAPI;


      API.enableKinderbox( function (success) {
          console.log('What is success? ', success);
          console.log('enableKinderbox called, status:', success);
          //$scope.results.splice(tobeDeleted, 1);

      }); 

        //perform a XHR request to the server for updating albums with rfids
        // kinderboxAPI.enableKinderbox()
        //   .success(function(data, status, headers, config) {
        //   // this callback will be called asynchronously
        //   // when the response is available
        //     console.log('enableKinderbox called success', status);
        //     //$scope.updateShow = false;
        //     //$scope.getAlbums();

        //   })
        //   .error(function(data, status, headers, config) {
        //   // called asynchronously if an error occurs
        //   // or server returns response with an error status.
        //   console.log('enableKinderbox response with an error', status);
        //   });

    }


});


kbox.controller('MatchRfidCtrl', function ($scope, myFaye, rfidService, playlistAlbumService) {

    $scope.isloading = true;

    // playlistAlbumService.getAlbums()
    //   .then(function(response) {
    //     //$scope.results = _.pluck(response.data.data, 'data');
    //     $scope.musicAlbums = response.data.data
    //     console.log("musicAlbums results: ", $scope.musicAlbums);
    //   })

    playlistAlbumService.getAlbums()
      .success(function(data, status, headers, config) {
        //$scope.musicAlbums = _.pluck(data.data, 'data');
        $scope.musicAlbums = data.data;
        console.log('musicAlbums results: ', status, data.data);
        $scope.isloading = false;


      })
      .error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        console.log('playlistAlbumService response with an error', status);
      });

     console.log('Ima here...'); 

    //this function is just for simulating the assigment of a rfid card.
    $scope.testMatchAlbum = function(rfid) {
        //$scope.selected = val;
        //alert("Matching album with rfid: " + rfid);
        //perform a XHR request to the server for updating albums with rfids
        console.log('RFID card is: ', rfid);
        $scope.rfidCard = rfid;

    };



    $scope.matchRFID2Album = function(rfid) {
        $scope.rfidCard = rfid;
    };


    //enable scan here, subscribe to faye to get rfid number pushed.

    rfidService.startRFIDScan()
      .success(function(data, status, headers, config) {
      // this callback will be called asynchronously
      // when the response is available
      console.log('rfidService called success', status);
      })
      .error(function(data, status, headers, config) {
        // called asynchronously if an error occurs
        // or server returns response with an error status.
        console.log('rfidService response with an error', status);
      });
  
    $scope.messages = [];
    // Subscribe
    myFaye.subscribe('/messages/new', function(msg) {  
      //$("#playing").text(msg);
      $scope.$apply(function() {
        var a = msg.split('-');
        $scope.messages.push(msg);
        console.log('Set rfidcard = ', msg, a); 
        $scope.rfidCard = a[0];
      });

      //$scope.messages.push(msg);
      //console.log("messages: ", $scope.messages);
    });



});

kbox.controller('ShowAlbumCtrl', function ($scope, playlistAlbumService, updateKinderboxService, kinderboxAPI) {
  // $scope.search = function() {
  //     testService.searchOne()
  //     .then(function(response) {
  //       //$scope.results = _.pluck(response.data.data, 'data');
  //       $scope.results = response.data.data
  //       console.log("results: ", $scope.results);
  //     }); 

  // };
      $scope.isloading = true;

      $scope.updateShow = false;
      $scope.results = {};

      // playlistAlbumService.getAlbums()
      // .then(function(response) {
      //   //$scope.results = _.pluck(response.data.data, 'data');
      //   $scope.results = response.data.data;
      //   console.log('results: ', $scope.results);
      // });


      $scope.getAlbums = function() {

        playlistAlbumService.getAlbums()
          .then(function(response) {
          //$scope.results = _.pluck(response.data.data, 'data');
          $scope.results = response.data.data;
          console.log('results: ', $scope.results);
          $scope.isloading = false;
        });

      };


      // this.updateKinderbox = function (argument) {
      //   // body...
      //   alert('update kinderbox');
      // };

      var tobeDeleted  = null;
      $scope.activateModal = function (idx) {
        var delAlbum = $scope.results[idx];
        tobeDeleted = idx;
        $("#myModal").modal(function(idx) {
            console.log('myModal idx:', idx);
        }); 
        //alert('barcodeid: ' + delAlbum.barcodeid);        
        $( "modalbody" ).each(function( index ) {
            //console.log( index + ": " + $( this ).text() );
            $(this).hide();
        });
        $("#"+ delAlbum.barcodeid ).toggle();
        
      };


      $scope.deleteAlbum = function () {
        //alert('Are you sure?');
        // if(!confirm('Are you sure?')) {
        //   //console.log('You want to delete me!');
        //   //if user does not confirm, return, otherwise process further.
        //   return;
        // };



        var API = kinderboxAPI;
        var delAlbum = $scope.results[tobeDeleted];
        //var delAlbum = tobeDeleted; 

        console.log('Deleteing album: ', delAlbum);
        //API.DeletePerson({ id: person.id }, function (success) {
        //**// I NEED SOME CODE HERE TO PULL THE PERSON FROM MY SCOPE**
        //});
        //console.log("deleting: ", album);
        //{ barcode: delAlbum.barcode, rfid: delAlbum.rfid }
        API.deleteAlbum( {barcodeid: delAlbum.barcodeid }, function (success) {
          console.log('What is success? ', success);
          $scope.results.splice(tobeDeleted, 1);
          console.log("After removing: ", $scope.results.length); 

        });            

      };


      $scope.remove = function(item) { 
        var index = $scope.results.indexOf(item)
        $scope.results.splice(index,1);    
        console.log("After removing: ", $scope.results.length); 
      };



      $scope.doUpdate = function() {

        $scope.updateShow = true;
        //$scope.selected = val;
        //alert('Do Update');
        //perform a XHR request to the server for updating albums with rfids
        updateKinderboxService.startUpdateKinderbox()
          .success(function(data, status, headers, config) {
          // this callback will be called asynchronously
          // when the response is available
            console.log('updateKinderboxService called success', status);
            $scope.updateShow = false;
            $scope.getAlbums();

          })
          .error(function(data, status, headers, config) {
          // called asynchronously if an error occurs
          // or server returns response with an error status.
          console.log('updateKinderboxService response with an error', status);
          });

      };


      $scope.showImg = function() {
        //$scope.selected = val;
        alert('Sho image');
        return false;

      };

      //filter for ng-repeat to filter out barcode entry with empty string
      $scope.barcodeNotEmpty = function(item) {
          if (item.barcodeid !== '') {
            return true;
        }
        return false;
      };
      
      //called to get album info and show on the page.
      $scope.getAlbums();



});

kbox.controller('PlaylistCtrl', function ($scope) {
  console.log('Enter PlaylistCtrl');
  //Upload new albums happen here

});

kbox.controller('RfidStatusCtrl', function ($scope, rfidStatusService) {
  $scope.rfidStatus = {};
  //$scope.rfidStatus = 
  $scope.rfidStatus = rfidStatusService.getRFIDStatus();
  //$scope.rfidStatus.total = 12; 

});

kbox.controller('RfidCtrl', function ($scope, myFaye, rfidService) {
  //console.log("Enter RfidCtrl", myFaye);

  // rfidService.startRFIDScan()
  // .then(function(response) {
  //   console.log("Response: ");
  // });

  rfidService.startRFIDScan()
  .success(function(data, status, headers, config) {
      // this callback will be called asynchronously
      // when the response is available
      console.log('rfidService called success', status);
    })
  .error(function(data, status, headers, config) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
      console.log('rfidService response with an error', status);
  });


  // Subscribe
  $scope.messages = [];
  $scope.duplicate = [];
  $scope.duplicateRFID = false;
  $scope.rfid = '';
  $scope.boxStyling = '';
  $scope.boxIcon = '';

  myFaye.subscribe('/messages/new', function(msg) {  
      //$("#playing").text(msg);
      $scope.$apply(function() {

        //check if msg contains the word "duplicate"
        if (msg.indexOf('duplicate') > -1) {
          $scope.rfid = msg;
          $scope.duplicate.push(msg);
          console.log('RFID is duplicated!');
          $scope.boxStyling = '';
          $scope.boxIcon = 'warning-sign';
          $scope.duplicateRFID = true;

          $('#duplicated').fadeIn();

          setTimeout(function() { $scope.duplicateRFID = false; }, 1000);

          var timerId = setTimeout(function() { 
            //alert(1);
            //$scope.duplicateRFID = false;
            $('#duplicated').fadeOut();

          }, 3000);

          //clearTimeout(timerId)


        }
        else {
          $scope.boxStyling = 'alert-success';
          $scope.boxIcon = 'ok';
          $scope.messages.push(msg);
        }
  
        
      });

      //$scope.messages.push(msg);
      //console.log("messages: ", $scope.messages);
  });


});


kbox.controller('AlbumCtrl', function ($scope, $http, $resource) {  

    $http.defaults.useXDomain = true;
    //http://www.reddit.com/search.json?q=angularjs
    //http://www.reddit.com/user/spilcm/comments/.json
    //http://www.reddit.com/r/search?q=angularjs&jsonp=JSON_CALLBACK
    $http({method: 'JSONP', url: "http://10.0.0.62/cgi-bin/getRFID.py?test=1&jsonp-JSON_CALLBACK"})
    .success(function(data, status, headers, config) {
      // this callback will be called asynchronously
      // when the response is available
      console.log('called success');
    })
    .error(function(data, status, headers, config) {
      // called asynchronously if an error occurs
      // or server returns response with an error status.
      console.log('response with an error');
    });

    //Define CreditCard class
    //http://10.0.0.54/cgi-bin/getRFID.py
    //$http.defaults.useXDomain = true;
    //var CreditCard = $resource('http://10.0.0.54/cgi-bin/getRFID.py',
    //{ userId:123, cardId:456 }, {
    //    charge: {method:'JSONP', params:{charge:true}}
    //});

  // // We can retrieve a collection from the server
  // var cards = CreditCard.query(function() {
 //   // GET: /user/123/card
 //   // server returns: [ {id:456, number:'1234', name:'Smith'} ];
 
 //   var card = cards[0];
 //   // each item is an instance of CreditCard
 //   expect(card instanceof CreditCard).toEqual(true);
 //   card.name = "J. Smith";
 //   // non GET methods are mapped onto the instances
 //   card.$save();
 //   // POST: /user/123/card/456 {id:456, number:'1234', name:'J. Smith'}
 //   // server returns: {id:456, number:'1234', name: 'J. Smith'};
 
 //   // our custom method is mapped as well.
 //   card.$charge({amount:9.99});
 //   // POST: /user/123/card/456?amount=9.99&charge=true {id:456, number:'1234', name:'J. Smith'}
  // });

});


