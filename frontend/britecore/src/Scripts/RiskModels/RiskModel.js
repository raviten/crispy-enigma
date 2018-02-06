import React from 'react';
import axios from 'axios';
import * as ApiConfig from '../ApiConfig';
import getHeader from '../helper';
import FieldType from './FieldType';
import RaisedButton from 'material-ui/RaisedButton';

const style = {
  margin: 12,
};
class RiskModel extends React.Component {
  constructor(props) {
    super(props);
    let riskModelId = props.match.params.pk;
    this.state = {
      riskModelId: riskModelId,
      riskModel: {
        field_types: []
      }
    };
  }


  componentDidMount(props) {
    var _this = this;
    let url = ApiConfig.HOST_URL + ApiConfig.RISK_MODEL + this.state.riskModelId;
    this.serverRequest =
      axios({
        method: "GET",
        url: url,
        headers: getHeader()
      }).then(function(result) {
        console.log(result);
        _this.setState({
          riskModel: result.data
        });
      })
  }

  render() {
    let self = this;
    return (
      <div>
        <form>
        {
          this.state.riskModel.field_types.map(function(ft) {
              return (
                <FieldType key={ft.id} ft={ft}/>
                );
          })
        }
        <RaisedButton label="Submit" primary={true} style={style} />
        </form>
      </div>
    );
  }
}
export default RiskModel;