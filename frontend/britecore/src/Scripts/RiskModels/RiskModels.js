import React from 'react';
import axios from 'axios';
import * as ApiConfig from '../ApiConfig';
import getHeader from '../helper';
import { Link } from 'react-router-dom';

class RiskModels extends React.Component {
  constructor(props) {
    super(props);
    this.state = {riskModels: []};
  }


  componentDidMount(props) {
    var _this = this;
    let url = ApiConfig.HOST_URL + ApiConfig.RISK_MODEL;
    console.log(url);
    this.serverRequest =
      axios({
        method: "GET",
        url: url,
        headers: getHeader()
      }).then(function(result) {
          console.log(result);
          _this.setState({
            riskModels: result.data
          });
        })
  }


  render() {
    return (
      <div>
        <ul className="RiskModels">
            {
                this.state.riskModels.map(function(rm) {
                    let to = '/risk-models/' + rm.id;
                    return <li key={rm.id}><Link to={to}>{rm.name}</Link></li>
                })
            }
            </ul>
      </div>
    );
  }
}
export default RiskModels;
