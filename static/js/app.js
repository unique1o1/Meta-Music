import React from "react";
import Card from "./card";
import * as randomMC from "random-material-color";
export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: {},
      loading: true
    };
  }

  // delay(second) {
  //   return new Promise(resolve => {
  //     setTimeout(resolve, second * 1000);
  //   });
  // }
  // shouldComponentUpdate(nextProps, nextState) {
  //   return false;
  // }

  componentDidMount() {
    fetch("http://127.0.0.1:5000/fetch/" + this.props.songno)
      .then(response => response.json())
      .then(Data => {
        this.setState({ data: Data, loading: false });
      });
  }

  render() {
    return this.state.loading ? (
      <div>dsf</div>
    ) : (
      <div
        className="card"
        style={{
          width: "18rem",
          backgroundColor: randomMC.getColor(),
          lineHeight: 1.1,
          borderBottomRightRadius: "15px",

          borderBottomLeftRadius: "15px"
        }}
      >
        {console.log(this.state.data.uid)}
        <Card resp={this.state.data} />
      </div>
    );
  }
}
