function getInputField() {
	return document.getElementById('inputField');
}
function focusInput() {
	var input = getInputField();
	if (input.value == "") {
		input.focus();
	}
}
function validateForm() {
	return getInputField().value != "";
}
function embed(videoURL) {
	if (videoURL && videoURL != '') {
		swfobject.embedSWF(videoURL + "&enablejsapi=1", "apiplayer", "425", "356", "8", null, null, {allowScriptAccess : "always"}, {id : "player", name : "player"});
		displayTime(0, 0);
	}
}
function getplayer() {
	return swfobject.getObjectById("player");
}
function onYouTubePlayerReady() {
	var player = getplayer();
	if (player) {
		player.addEventListener("onStateChange", "onPlayerStateChange");
		player.playVideo();
		updateTimeDisplay();
	}
}
function onPlayerStateChange(newState) {
	// unstarted (-1), ended (0), playing (1), paused (2), buffering (3), video
	// cued (5).
	if (Number(newState) == 0) {
		document.getElementById('message').innerHTML = "{{ messageDefault }}";
		document.getElementById('time').innerHTML = "";
	}
}
function updateTimeDisplay() {
	var player = getplayer();
	if (player) {
		displayTime(player.getCurrentTime(), player.getDuration());
		setTimeout(updateTimeDisplay, 100);
	}
}
function displayTime(current, duration) {
	document.getElementById('time').innerHTML = timeCode(current) + ' / ' + timeCode(duration);
}
function timeCode(sec) {
	var m = Math.floor((sec % 3600) / 60);
	var s = Math.floor((sec % 3600) % 60);
	var t = "";
	if (m < 10)
		t += "0";
	t += m.toString() + ":";
	if (s < 10)
		t += "0";
	t += s.toString();
	return t;
}