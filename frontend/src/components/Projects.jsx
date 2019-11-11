import { Component, Fragment } from 'react';
import PropTypes from 'prop-types';
import { VictoryBar, VictoryChart, VictoryAxis, VictoryTheme } from 'victory';
import Grid from '@material-ui/core/Grid';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Typography from '@material-ui/core/Typography';

export default class Projects extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showProject: null,
    };

    this.setProject = this.setProject.bind(this);
  }

  setProject(value) {
    return () => {
      this.setState({ showProject: value });
    };
  }

  showProject() {
    if (this.state.showProject !== null) {
      return (
        <Fragment>
          <div style={{ textAlign: 'center' }}>
            <Typography variant="h5" component="h2">
              {`${this.props.projects[this.state.showProject].name} Chart`}
            </Typography>
          </div>
          <VictoryChart
            // adding the material theme provided with Victory
            theme={VictoryTheme.material}
            domainPadding={20}
          >
            <VictoryAxis
              tickValues={[1, 2, 3, 4]}
              tickFormat={['Year 1', 'Year 2', 'Year 3', 'Year 4']}
            />
            <VictoryAxis
              dependentAxis
              tickFormat={x => (`$${x}`)}
            />
            <VictoryBar
              data={this.props.projects[this.state.showProject].data}
              x="year"
              y="revenue"
            />
          </VictoryChart>
        </Fragment>);
    }

    return null;
  }

  render() {
    return (
      <Grid container justify="space-between" spacing={3}>
        <Grid item xs={3}>
          <List>
            {this.props.projects.map((project, index) =>
              (
                <ListItem
                  button
                  selected={index === this.state.showProject}
                  onClick={this.setProject(index)}
                >
                  <Typography variant="button" component="span">{project.name}</Typography>
                </ListItem>
              ))}
          </List>
        </Grid>
        <Grid item xs={6}>
          {this.showProject()}
        </Grid>
      </Grid>
    );
  }
}

Projects.defaultProps = {
  projects: null,
};

Projects.propTypes = {
  projects: PropTypes.arrayOf(PropTypes.shape({
    name: PropTypes.string,
    data: PropTypes.object,
  })),
};
