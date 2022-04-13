'use strict';

// Declare Variables
var remoteConnection;
var sendChannel; // Local text
var receiveChannel; // Remote text
var localStream; // Local video + audio
var remoteStream; // Remote video + audio
// Variables for counting / making sure something doesn't happen twice
var connectedCount = 0;
var runOutCount = 0;
var callStarted = false;
var callInProgress = false;
var alreadyEnded = false;
var duplicateCatch = false;
var iceClose = false;
// Document Elements
const messageInput = document.querySelector('input#message');
const messageDisplay = document.querySelector('tbody#text_chat');
const sendButton = document.querySelector('button#send');
const dictText = document.querySelector('input#search');
const dictButton = document.querySelector('button#lookup');
const dictResult = document.querySelector('p#definition');
const closeButton = document.querySelector('button#disconnect');
const localVideo = document.querySelector('video#localVideo');
const remoteVideo = document.querySelector('video#remoteVideo');
const deviceModal = document.querySelector('div#deviceNotif');
const reportModal = document.querySelector('div#userReport');
const leaveButton = document.querySelector('button#endCall');
// Bind Buttons to functions
//closeButton.onclick = terminateConnection; <- Needs function implemented first
sendButton.onclick = sendMessage;
dictButton.onclick = dictSearch;
leaveButton.onclick = closeCall;

// Media Constraints

const constraints ={
  'video': {
    "width": 1280,
    "height": 720
  },
  'audio': true
}

async function getMicAndCam(){
  navigator.mediaDevices.enumerateDevices()
    .then(devices => {
      // Get both device kinds
      const audioDevices = devices.filter(device => device.kind === 'audioinput');
      const videoDevices = devices.filter(device => device.kind === 'videoinput');
      // If there's at least one of each, go ahead
      if(audioDevices.length != 0 && videoDevices.length != 0){
        console.log(videoDevices);
        deviceModal.style.display = "none"; // Clear Popup
        if(!duplicateCatch){ // Make sure room not already joined before joining
          preCallSetup();
        }
        duplicateCatch = true;
      }
      else{
        deviceModal.style.display = "block"; // Display Error Popup
      }
    })
}

// Listener for connecting new devices
navigator.mediaDevices.addEventListener('devicechange', event => {
  if(!callStarted){
    getMicAndCam();
  }
});

// Signaling-server socket listener:
socket.on('Message', async function(message){
  if(message.from == username){return}
  console.log("Recieved Message: ", message);
  if (message.answer) {
      console.log("Got an answer");
      const remoteDesc = new RTCSessionDescription(message.answer);
      await remoteConnection.setRemoteDescription(remoteDesc);
  }
  else if (message.offer) {
      console.log("Got an offer");
      remoteConnection.setRemoteDescription(new RTCSessionDescription(message.offer));
      const answer = await remoteConnection.createAnswer();
      await remoteConnection.setLocalDescription(answer);
      socket.emit('Message', {'answer': answer, 'room':room_ID, 'from':username});
      console.log("Just sent answer");
  }
  else if (message.new_ice_candidate) {
    console.log("Ice Candidate passed");
      try {
          await remoteConnection.addIceCandidate(message.new_ice_candidate);
      } catch (e) {
          console.error('Error adding received ice candidate', e);
      }
  }
});

// Set up things in advance to avoid things not being defined once the call starts
function preCallSetup(){
  callStarted = true;
  console.log("Setting up before call")
  const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]}
  remoteConnection = new RTCPeerConnection(configuration);
  // Text Channel
  sendChannel = remoteConnection.createDataChannel("from_" + username);
  // Set up listeners
  setupListeners();
  //Need to make sure this finishes before we start to set up call, so format as async=>then
  navigator.mediaDevices.getUserMedia(constraints)
    .then(media=>{
      // All Video/Audio related setup
      localStream = media;
      localVideo.srcObject = localStream; // Set up local video
      localStream.getTracks().forEach(track => {
        remoteConnection.addTrack(track, localStream);
      });
      //Join the room and tell everyone we're ready to connect
      socket.emit('joinCallRoom', {room: (room_ID), initiator: (initiator)});
    });
}

// Function to set up connection
async function makeCall(){
  console.log("Initiating");
  if(initiator){
    console.log("Entering as initiator");
    const offer = await remoteConnection.createOffer();
    await remoteConnection.setLocalDescription(offer);
    socket.emit('Message', {'offer': offer, 'room':room_ID, 'from':username});
    console.log("Just sent offer");
  }
  else{
    console.log("Entering as reciever");
  }
  console.log("Finished Passing Connection Offers");
}

// Event Listener Setup
function setupListeners(){
 // Trickle-Ice Candidate Passing:
  remoteConnection.addEventListener('icecandidate', event => {
      if (event.candidate) {
        socket.emit('Message', {'new_ice_candidate': event.candidate, 'room':room_ID, 'from':username});
      }
      else{
        console.log("we have run out of options");
        socket.emit('outOfIce', {room: (room_ID)});
      }
  });

  remoteConnection.addEventListener('connectionstatechange', event => {
      if (remoteConnection.connectionState === 'connected') {
        leaveButton.disabled=false;
        callInProgress = true;
      }
      else if (remoteConnection.connectionState === 'disconnected'){
        uncleanClose = true;
        closeCall();
      }
  });

  remoteConnection.addEventListener('datachannel', event => {
    receiveChannel = event.channel;
    setupReceiveListeners();
  });

  remoteConnection.addEventListener('track', async (event) => {
    remoteStream = event.streams;
    remoteVideo.srcObject = remoteStream[0];
  });

  // Enable textarea and button when channel opened
  sendChannel.addEventListener('open', event => {
      messageInput.disabled = false;
      sendButton.disabled = false;
  });

  // Disable input when channel closed
  sendChannel.addEventListener('close', event => {
      messageInput.disabled = true;
      sendButton.disabled = true;
  });

  console.log("setup listeners");
}

function setupReceiveListeners(){
  receiveChannel.addEventListener('message', event => {
    console.log("Recieved Message");
    var message = event.data;
    // Not sure about code injection, but may need to change implementation
    messageDisplay.innerHTML += "<tr><td>" + target + ": " + message + "</td></tr>";
    messageDisplay.scrollTop = messageDisplay.scrollHeight;
  });
}

// Users Passing Messages:
function sendMessage(){
  console.log("Sending Message");
  var message = messageInput.value;
  message = message.replace(/</g, "&lt;").replace(/>/g, "&gt;"); // Prevent injection attacks
    if(message != ''){
    // Log message Locally + Send
    messageDisplay.innerHTML += "<tr><td>" + username + ": " + message + "</td></tr>";
    sendChannel.send(message);
    // QOL Stuff
    messageInput.value="";
    messageDisplay.scrollTop = messageDisplay.scrollHeight;
  }
}

// Looking something up from the dictionary
function dictSearch(){
  console.log("Searching Term");
  var value = dictText.value;
  value = value.toLowerCase();
  if(value != '' && !value.includes(' ')){
    dictText.value = '';
    dictText.disabled = true;
    dictButton.disabled = true;
    dictResult.innerHTML = value + ": ";
    socket.emit('Dictionary', {'text': value, 'language': language});
  }
}

// Dictionary Response listener
socket.on('Dictionary-Response', function(data){
  dictResult.innerHTML += data.text;
  dictText.disabled = false;
  dictButton.disabled = false;
});

// Function to execute once the call is closed
function closeCall(){
  console.log("They left D:<");
  leaveButton.disabled=true;
  remoteConnection.close();
  if(iceClose){ //If closed from ice, we don't want to show option to Report
    window.location.replace("./msg");
  }
  else{
    reportModal.style.display = "block"; // Display report Modal
  }
}
