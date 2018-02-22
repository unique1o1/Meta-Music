import React from "react";
import ReactDOM from "react-dom";
import App from "./app";

var theclass = document.getElementsByClassName("card-deck")[0];
(async function renderDOM() {
  for (let i = 0; i < document.getElementById("totalsongs").value; i++) {
    const id = "id" + i; //or some such identifier
    const d = document.createElement("div");
    d.className = "col-sm-3";
    d.id = id;
    theclass.appendChild(d);

    await ReactDOM.render(<App songno={i} />, document.getElementById(id));

    console.log("aaaaa");
  }
})();
