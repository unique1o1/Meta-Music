import React from "react";
import Card from "./card";
export default class App extends React.Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div className="card-deck">
        {this.props.totalno.map((value, index) => <Card key={index} />)}
      </div>
    );
  }
}
