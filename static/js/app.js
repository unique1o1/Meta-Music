import React from "react";
import Card from "./card";
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

  // componentDidMount() {
  //   fetch("http://127.0.0.1:5000/fetch/" + this.props.songno)
  //     .then(response => response.json())
  //     .then(Data => {
  //       this.setState({ data: Data, loading: false });
  //     });
  // }

  render() {
    return (
      <div>
        <div
          className="skill-card"
          style={{
            lineHeight: 1.1
          }}
        >
          {/* {console.log(this.props.data)} */}
          <Card resp={this.props.data} />
        </div>
        <br />
      </div>
    );
  }
}
