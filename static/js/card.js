import React from "react";
export default class Card extends React.Component {
  render() {
    return (
      <div style={{ lineHeight: 0.8 }}>
        <img
          className="card-img-top"
          src={this.props.resp.image_url}
          alt="Card image cap"
        />

        <div
          className="card-body"
          style={{ display: "block", height: "120px", lineHeight: "1px" }}
        >
          <p
            className="card-title"
            style={{ padding: "5px 0", fontSize: "18px" }}
          >
            <b>
              {this.props.resp.trackname.length > 21
                ? this.props.resp.trackname.slice(0, 21) + "..."
                : this.props.resp.trackname}
            </b>
          </p>
          <p
            className="card-title"
            style={{ padding: "5px 0", fontSize: "16px" }}
          >
            {this.props.resp.artistname}
          </p>
          <p
            className="card-title"
            style={{ padding: "5px 0", fontSize: "16px" }}
          >
            {" "}
            {this.props.resp.albumname.length > 21
              ? this.props.resp.albumname.slice(0, 21) + "..."
              : this.props.resp.albumname}
          </p>
          <p className="card-text" />
          {this.props.resp.tracknumber},{" "}
          {this.props.resp.releasedate.slice(0, 16)}, {this.props.resp.genre}
        </div>
      </div>
    );
  }
}
