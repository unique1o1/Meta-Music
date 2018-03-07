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
