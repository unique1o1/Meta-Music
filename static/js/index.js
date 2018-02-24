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

console.log("called");

myworker.onmessage = function(Data) {
  const id = "id" + Data.data.uid; //or some such identifier
  const d = document.createElement("div");
  d.className = "col-sm-3";
  d.id = id;
  theclass.appendChild(d);

  console.log(Data.data.uid);

  ReactDOM.render(
    <App songno={Data.data.uid} data={Data.data} />,
    document.getElementById(id)
  );
};

//************************************************ */

// var theclass = document.getElementsByClassName("card-deck")[0];
// (async function renderDOM() {
//   for (let i = 0; i <= document.getElementById("totalsongs").value; i++) {
//     const id = "id" + i; //or some such identifier
//     const d = document.createElement("div");
//     d.className = "col-sm-3";
//     d.id = id;
//     theclass.appendChild(d);

//     // jQuery.ajax({
//     //   url: "127.0.0.1:5000/fetch/0",
//     //   success: function(s) {
//     //     alert(s.trackname);
//     //   },
//     //   async: false
//     // });
//     fetch("http://127.0.0.1:5000/fetch/0")
//       .then(response => response.json())
//       .then(Data => {
//         console.log("asdf");
//       });
//     console.log("ssss");

//     await ReactDOM.render(<App songno={i} />, document.getElementById(id));
//   }
// })();
