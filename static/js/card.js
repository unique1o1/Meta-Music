import React from "react";

import * as randomMC from "random-material-color";
export default class Card extends React.Component {
  render() {
    return (
      <div>
        <header
          className="skill-card__header"
          style={{ backgroundColor: randomMC.getColor() }}
        >
          <img
            className="skill-card__icon "
            src={this.props.resp.image_url}
            alt="HTML5 Logo "
          />
        </header>
        <section className="skill-card__body ">
          <p className="skill-card__title ">
            {this.props.resp.trackname.slice(0, 18)}
          </p>
          <p> {this.props.resp.artistname}</p>

          <span className="skill-card__duration">
            {this.props.resp.albumname.length > 21
              ? this.props.resp.albumname.slice(0, 21) + "..."
              : this.props.resp.albumname}
          </span>
          <ul className="skill-card__knowledge ">
            <li> {this.props.resp.tracknumber}</li>
            <li> {this.props.resp.releasedate.slice(0, 16)}</li>
            <li> {this.props.resp.genre}</li>
          </ul>
        </section>
      </div>
    );
  }
}
