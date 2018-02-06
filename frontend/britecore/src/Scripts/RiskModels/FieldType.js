import React from 'react';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import TextField from 'material-ui/TextField';
import DatePicker from 'material-ui/DatePicker';


/**
 * With the `maxHeight` property set, the Select Field will be scrollable
 * if the number of items causes the height to exceed this limit.
 */

class EnumType extends React.Component {
  state = {
    items: []
  };

  getItems(validators) {
    let items = [];
    if (!validators.oneOf) {
      return;
    }
    let oneOf = validators.oneOf;
    for (let i = 0; i < oneOf.length; i++) {
      items.push(<MenuItem value={oneOf[i]} key={i} primaryText={`${oneOf[i]}`} />);
    }
    return items;
  }
  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      items: this.getItems(props.validators),
      hintText: props.hintText,
      floatingLabelText: props.floatingLabelText,
      floatingLabelFixed: props.floatingLabelFixed,
    };
  }


  handleChange = (event, index, value) => {
    this.setState({
      value
    });
  };

  render() {
    return (
      <SelectField
        floatingLabelText={this.state.hintText}
        floatingLabelFixed={true}
        value={this.state.value}
        onChange={this.handleChange}
        maxHeight={200}
      >
        {this.state.items}
      </SelectField>
    );
  }
}

class FieldType extends React.Component {
  constructor(props) {
    super(props);
    console.log(props);
    this.state = {
      ft: this.props.ft
    };
  }

  renderFieldType(ft) {
    console.log(ft);
    let fieldType = ft.field_type;
    if (fieldType === "text") {
      return (<TextField
              hintText={ft.name} />);
    } else if (fieldType === "number") {
      return (<TextField  type="number"
              hintText={ft.name} />);
    } else if (fieldType === "date") {
      return (<DatePicker
              hintText={ft.name}
              mode="landscape" />);
    } else if (fieldType === "enum") {
      return (<EnumType
              validators={ft.validators}
              hintText={ft.name}/>);
    }
  }

  render() {
    var renderedFt = this.renderFieldType(this.state.ft);
    return (
      <div>
        <label>{this.state.ft.name}</label>
        <div>
          {renderedFt}
        </div>
        <br/>
      </div>
    )
  }

}
export default FieldType;