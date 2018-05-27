import React from "react";
import ReactDOM from "react-dom";
import App from "./app";

// import Worker from "worker-loader!./Worker.js";
var songs = document.getElementById("totalsongs").value;
var theclass = document.getElementsByClassName("card-deck")[0];
// import Worker from "./file.worker.js";
window.onload = function me() {
  var elem = document.getElementById("vis");

  elem.style.top = "50%";
  elem.style.left = "50%";
  elem.style.width = "0%";
  elem.style.height = "0%";
  elem.style.borderRadius = "25px";

};
var myworker = new Worker("dist/Worker.js");

myworker.postMessage(songs);
console.log(myworker);

myworker.onmessage = function (Data) {
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
