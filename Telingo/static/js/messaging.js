'use strict';

// Declare Variables
var remoteConnection;
var sendChannel;
var receiveChannel;
var connectedCount = 0;
// Document Elements
const messageInput = document.querySelector('input#message');
const messageDisplay = document.querySelector('div#text_chat');
const sendButton = document.querySelector('button#send');
const closeButton = document.querySelector('button#disconnect');

// Bind Buttons to functions
//closeButton.onclick = terminateConnection; <- Needs function implemented first
sendButton.onclick = sendMessage;

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
  remoteConnection = new RTCPeerConnection(configuration);
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
    messageDisplay.innerHTML += target + ": " + message + "<br>";
  });
}

// Users Passing Messages:
function sendMessage(){
  console.log("Sending Message");
  var message = messageInput.value;
  // Log message Locally + Send
  messageDisplay.innerHTML += username + ": " + message + "<br>";
  sendChannel.send(message);
  // QOL Stuff
  messageInput.value="";
  messageDisplay.scrollTop = messageDisplay.scrollHeight;
}