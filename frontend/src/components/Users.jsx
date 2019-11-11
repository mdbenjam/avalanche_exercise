import { Component, Fragment } from 'react';
import PropTypes from 'prop-types';

export default class Users extends Component {
  render() {
    return (
      <Fragment>
        <Typography variant="h4" component="h2">Users</Typography>
        <Typography variant="h5" component="h3">Current Users</Typography>
        <ul>
          {this.props.profiles.map(profile => (
            <li>
              <Typography variant="subtitle1" component="li">
                {`${profile.user.first_name} ${profile.user.last_name}`}
              </Typography>
            </li>
          ))}
        </ul>
      </Fragment>
    );
  }
}

Users.defaultProps = {
  profiles: null,
};

Users.propTypes = {
  profiles: PropTypes.arrayOf(PropTypes.shape({
    user: PropTypes.shape({
      first_name: PropTypes.string,
      last_name: PropTypes.string,
    }),
  })),
};
