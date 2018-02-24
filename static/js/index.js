import React from "react";
import ReactDOM from "react-dom";
import App from "./app";

// import Worker from "worker-loader!./Worker.js";
var songs = document.getElementById("totalsongs").value;
var theclass = document.getElementsByClassName("card-deck")[0];
// import Worker from "./file.worker.js";

var myworker = new Worker("dist/Worker.js");
console.log(myworker);

myworker.postMessage(songs);

myworker.onmessage = function(Data) {
  const song_count = document.getElementById("totalsongs").value;
  const id = "id" + Data.data.uid; //or some such identifier
  const d = document.createElement("div");
  d.className = "col-sm-3";
  d.id = id;
  d.className = "fadein_slowly";
  theclass.appendChild(d);

  console.log(Data.data.uid);
  console.log("songcount");
  ReactDOM.render(
    <App songno={Data.data.uid} data={Data.data} />,
    document.getElementById(id)
  );

  ReactDOM.render(
    <span style={{ fontSize: 15 }}>
      {Data.data.uid + 1} of <b>{song_count}</b>
    </span>,
    document.getElementById("index_count")
  );
};
