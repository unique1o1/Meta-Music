import React from "react";
import ReactDOM from "react-dom";
import App from "./app";

// ReactDOM.render(<App />, document.getElementById("content"));
var theclass = document.getElementsByClassName("card-deck")[0];
for (let i = 0; i < document.getElementById("totalsongs").value; i++) {
  const id = "id" + i; //or some such identifier
  const d = document.createElement("div");
  d.className = "col-sm-3";
  d.id = id;
  theclass.appendChild(d);
  ReactDOM.render(<App songno={i} />, document.getElementById(id));
}
