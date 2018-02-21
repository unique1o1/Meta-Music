import React from "react";
export default class Card extends React.Component {
  render() {
    return (
      <div>
        <img
          className="card-img-top"
          src={this.props.resp.image_url}
          alt="Card image cap"
        />
        {console.log(this.props.resp.uid)}
        <div className="card-body">
          <h4 className="card-title">{this.props.resp.trackname}</h4>
          <h5 className="card-title">{this.props.resp.artistname}</h5>
          <h6 className="card-title">{this.props.resp.albumname}</h6>
          <p className="card-text" />
          {this.props.resp.releasedate}
          {this.props.resp.tracknumber}

          {this.props.resp.gerne}
          <a href="#" className="btn btn-primary">
            Go somewhere
          </a>
        </div>
      </div>
    );
  }
}
