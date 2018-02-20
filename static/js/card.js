import React from "react";
export default class Card extends React.Component {
  render() {
    return (
      <div className="col-sm-3">
        <div className="card" style={{ width: "18rem" }}>
          <img
            className="card-img-top"
            src="dist/img/1.jpg"
            alt="Card image cap"
          />
          <div className="card-body">
            <h5 className="card-title">Card title</h5>
            <p className="card-text">
              Some quick example text to build on the card title and make up the
              bulk of the card's content.
            </p>
            <a href="#" className="btn btn-primary">
              Go somewhere
            </a>
          </div>
        </div>
      </div>
    );
  }
}
