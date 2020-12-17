(function() {
  // This javascript is used for the open camera function and allows the 
  //page to access the camera locally. See "project addition" tag for sections
  //added for our project.
  //adapted from: https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API/Taking_still_photos

  var width = 320;    // scale the photo width to this
  var height = 0;     // This will be computed based on the input stream

  // |streaming| indicates whether or not we're currently streaming
  // video from the camera. Obviously, we start at false.

  var streaming = false;

  // The various HTML elements we need to configure or control. These
  // will be set by the startup() function.

  var video = null;
  var canvas = null;
  var photo = null;
  var startbutton = null;
  var capbutton = null;
  var filename = null;

  function startup() {
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    photo = document.getElementById('photo');
    startbutton = document.getElementById('startbutton');
    capbutton = document.getElementById('capbutton');
    filename = document.getElementById('file');

    navigator.mediaDevices.getUserMedia({video: true, audio: false})
    .then(function(stream) {
      video.srcObject = stream;
      video.play();
    })
    .catch(function(err) {
      console.log("An error occurred: " + err);
    });

    video.addEventListener('canplay', function(ev){
      if (!streaming) {
        height = video.videoHeight / (video.videoWidth/width);
      
        // Firefox currently has a bug where the height can't be read from
        // the video, so we will make assumptions if this happens.
      
        if (isNaN(height)) {
          height = width / (4/3);
        }
      
        video.setAttribute('width', width);
        video.setAttribute('height', height);
        canvas.setAttribute('width', width);
        canvas.setAttribute('height', height);
        streaming = true;
      }
    }, false);
    
    //button to take photo
    startbutton.addEventListener('click', function(ev){
      takepicture();
      ev.preventDefault();
    }, false);
    
    //button to select photo - project addition
    capbutton.addEventListener('click', function(ev){
      var imagename1 = imageupload();
      document.getElementById('file').value = imagename1;
      ev.preventDefault();
    }, false);

    clearphoto();
  }

  // Fill the photo with an indication that none has been
  // captured.

  function clearphoto() {
    var context = canvas.getContext('2d');
    context.fillStyle = "#AAA";
    context.fillRect(0, 0, canvas.width, canvas.height);

    var data = canvas.toDataURL('image/png');
    photo.setAttribute('src', data);
  }
  
  // Capture a photo by fetching the current contents of the video
  // and drawing it into a canvas, then converting that to a PNG
  // format data URL. By drawing it on an offscreen canvas and then
  // drawing that to the screen, we can change its size and/or apply
  // other changes before drawing it.

  function takepicture() {
    var context = canvas.getContext('2d');
    if (width && height) {
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);
    
      var data = canvas.toDataURL('image/png');
      photo.setAttribute('src', data);
    } else {
      clearphoto();
    }
  }
//in order for image to be captured as DataURL, we save the image to disk 
//as type blob - project addition
  function dataURItoBlob( dataURI ) {

    var byteString = atob( dataURI.split( ',' )[ 1 ] );
    var mimeString = dataURI.split( ',' )[ 0 ].split( ':' )[ 1 ].split( ';' )[ 0 ];
    
    var buffer	= new ArrayBuffer( byteString.length );
    var data	= new DataView( buffer );
    
    for( var i = 0; i < byteString.length; i++ ) {
    
      data.setUint8( i, byteString.charCodeAt( i ) );
    }
    
    return new Blob( [ buffer ], { type: mimeString } );
  }
//added an upload function to the java script using a built in 
//function XMLHttpRequest in order to return the image for use with model
//-project addition
  function imageupload() {
    var request = new XMLHttpRequest();

    request.open( "POST", "/upload", false );
 
    var pdata	= new FormData();
    var dataURI	= photo.getAttribute( "src" );
    var imageData   = dataURItoBlob( dataURI );
    var imageName = "image"+Date.now()+".png"
    pdata.append( "file", imageData, imageName );

    request.send( pdata );
    console.log(request.responseURL);  
    return imageName
  }

  // Set up event listener to run the startup process
  window.addEventListener('load', startup, false);
})();
