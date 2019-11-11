import { Component } from 'react';
import axios from 'axios';
import Container from '@material-ui/core/Container';
import Button from '@material-ui/core/Button';
import Grid from '@material-ui/core/Grid';
import Companies from './components/Companies';
import Projects from './components/Projects';

export default class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      page: 'projects',
      projects: [],
    };
  }

  componentDidMount() {
    axios.get('customer_data/projects').then((response) => {
      this.setState({ projects: response.data });
    });
  }

  togglePage(page) {
    return () => {
      this.setState({ page });
    };
  }

  render() {
    return (
      <Container maxWidth="md">
        <Grid container justify="center" spacing={2}>
          <Grid justify="center" item xs={4}>
            <div style={{ textAlign: 'center' }}>
              <Button variant="contained" color="primary" onClick={this.togglePage('projects')}>
                Show Projects
              </Button>
            </div>
          </Grid>
          <Grid justify="center" item xs={4}>
            <div style={{ textAlign: 'center' }}>
              <Button variant="contained" color="primary" onClick={this.togglePage('companies')}>
                Show Companies
              </Button>
            </div>
          </Grid>
        </Grid>
        {this.state.page === 'companies' && <Companies /> }
        {this.state.page === 'projects' && <Projects projects={this.state.projects} /> }
      </Container>
    );
  }
}
