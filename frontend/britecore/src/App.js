import React from 'react';
import './App.css';
import RiskModels from './Scripts/RiskModels/RiskModels';
import RiskModel from './Scripts/RiskModels/RiskModel';
import { Switch, Route } from 'react-router-dom';
import AppBar from 'material-ui/AppBar';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import Paper from 'material-ui/Paper';

const style = {
  height: '100%',
  minHeight: 756,
  width: '80%',
  margin: 10,
  padding: 50,
  textAlign: 'left',
  display: 'inline-block',

};


function onTitleClick() {
  window.location.assign('/risk-models/');

}

const AppBarExampleIcon = () => (
  <AppBar
    title="RiskModels"
    iconClassNameRight="muidocs-icon-navigation-expand-more"
    showMenuIconButton={false}
    onTitleClick= {onTitleClick}
  />
);

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={RiskModels}/>
      <Route exact path='/risk-models' component={RiskModels}/>
      <Route path='/risk-models/:pk' component={RiskModel}/>
    </Switch>
  </main>
)

const App = () => (
  <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
  <div>
    <AppBarExampleIcon />
    <Paper style={style} zDepth={1}>
      <Main />
    </Paper>
  </div>
  </MuiThemeProvider>
)

export default App;