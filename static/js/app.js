import React from "react";
import Card from "./card";
export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: []
    };
  }

  // delay(second) {
  //   return new Promise(resolve => {
  //     setTimeout(resolve, second * 1000);
  //   });
  // }
  shouldComponentUpdate(nextProps, nextState) {
    return false;
  }

  loaddatas(value) {
    fetch("http://127.0.0.1:5000/fetch/" + value)
      .then(response => response.json())
      .then(Data =>
        this.setState(prevState => ({
          data: [...prevState.data, Data]
        }))
      );
  }

  render() {
    return (
      <div className="card-deck">
        {Array.from(
          { length: document.getElementById("totalsongs").value },
          (x, i) => i
        ).map((value, index) => {
          this.loaddatas(value);
          // while (this.state.data[value] == null) {
          //   setTimeout(() => {
          //     console.log(this.state.data);
          //   }, 3000);
          // }

          return <Card key={index} />;
          // console.log(results);
        })}
      </div>
    );
  }
}
