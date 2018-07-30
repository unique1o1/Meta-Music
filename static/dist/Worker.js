console.log("aaaaa");

this.onmessage = function(songs) {
  for (var i = 0; i < songs.data; i++) {
    var request = new XMLHttpRequest();
    request.open("GET", "http://127.0.0.1:5000/fetch/" + i, false); // `false` makes the request synchronous

    request.send(null);

    if (request.status === 200) {
      // console.log(JSON.parse(request.responseText));
      this.postMessage(JSON.parse(request.responseText));
    } else {
      console.log("no data for " + i + 1);
    }
  }
};
