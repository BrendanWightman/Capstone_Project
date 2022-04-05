'use strict';

// Declare Variables
var remoteConnection;
var sendChannel; // Local text
var receiveChannel; // Remote text
var localStream; // Local video + audio
var remoteStream; // Remote video + audio
var connectedCount = 0;
// Document Elements
const messageInput = document.querySelector('input#message');
const messageDisplay = document.querySelector('tbody#text_chat');
const sendButton = document.querySelector('button#send');
const closeButton = document.querySelector('button#disconnect');
const remoteVideo = document.querySelector('video#remoteVideo');

// Bind Buttons to functions
//closeButton.onclick = terminateConnection; <- Needs function implemented first
sendButton.onclick = sendMessage;

// Media Constraints

const constraints ={
  'video': {
    "width": 500,
    "height": 281.25
  },
  'audio': true
}
navigator.mediaDevices.getUserMedia(constraints)
  .then(stream => {
      console.log('Got MediaStream:', stream);
      // Once we get the stream, join room for call
      socket.emit('joinCallRoom', {room: (room_ID), initiator: (initiator)});
  })
  .catch(error => {
      //Add troubleshooting here, will require active listening and more code
      console.error('Error accessing media devices.', error);
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

// Function to set up connection
async function makeCall(){
  console.log("Initiating");
  const configuration = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]}
  // Set up local streams and channels in advance
  localStream = await navigator.mediaDevices.getUserMedia(constraints);
  remoteConnection = new RTCPeerConnection(configuration);
  localStream.getTracks().forEach(track => {
    remoteConnection.addTrack(track, localStream);
  });
  sendChannel = remoteConnection.createDataChannel("from_" + username);
  setupListeners();
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
  console.log("Finished making call");
}

// Event Listener Setup
function setupListeners(){
 // Trickle-Ice Candidate Passing:
  remoteConnection.addEventListener('icecandidate', event => {
      if (event.candidate) {
        socket.emit('Message', {'new_ice_candidate': event.candidate, 'room':room_ID, 'from':username});
      }
  });

  remoteConnection.addEventListener('connectionstatechange', event => {
      if (remoteConnection.connectionState === 'connected') {
        // Insert any code that needs to execute on connection here
        console.log("We're connected!");
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
