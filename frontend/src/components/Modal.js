import React, { Component } from "react";
import Chart from "react-google-charts";
import {
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Form,
  FormGroup,
  Input,
  Label,
} from "reactstrap";

export class SaveEditModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      ingredientInfo: this.props.ingredientInfo
    };
  }

  handleChange = (e) => {
    let { name, value } = e.target;

    if (e.target.type === "checkbox") {
      value = e.target.checked;
    }

    const activeItem = { ...this.state.activeItem, [name]: value };

    this.setState({ activeItem });
  };

  render() {
    const { toggle, onSave } = this.props;

    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}>Recipe Item</ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="recipe-title">Title</Label>
              <Input
                type="text"
                id="recipe-title"
                name="title"
                value={this.state.activeItem.title}
                onChange={this.handleChange}
                placeholder="Enter Recipe Title"
              />
            </FormGroup>
            <FormGroup>
              <Label for="recipe-description">Description</Label>
              <Input
                type="textarea"
                id="recipe-description"
                name="description"
                value={this.state.activeItem.description}
                onChange={this.handleChange}
                placeholder="Enter Recipe ingredients in format below
                weights should be in grams  (ex. 215g)
                &quot; ingredient name, weight of ingredient &quot; 
                One line per ingredient."
              />
            </FormGroup>

          </Form>
        </ModalBody>
        <ModalFooter>
          <Button
            color="success"
            onClick={() => onSave(this.state.activeItem)}
          >
            Save
          </Button>
        </ModalFooter>
      </Modal>
    );
  }
}

export class DetailedViewModal extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeItem: this.props.activeItem,
      chartData: this.props.chartData,
    };
    
  }

  makeChartTitle() {
    var total;
    for(const entry of this.state.chartData){
      console.log(entry[1])
      total  = (total || 0) + parseInt(entry[1])
    }
    return "Calorie Breakdown: "+ total + " Calories Total";
  }
  
  render() {
    const { toggle} = this.props;
    console.log("title : "+this.state.activeItem.title)
    const chartTitle = this.makeChartTitle();
    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle} cssModule={{'modal-title': 'w-100 text-center'}}> <Label for="recipe-title"  >{this.state.activeItem.title}</Label></ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="recipe-description">Ingredients</Label>
              <Input
                type="textarea"
                id="recipe-description"
                name="description"
                value={this.state.activeItem.description}
                rows = "5"
                readOnly
              />

            </FormGroup>
              <Chart   //shamelessly stolen from https://react-google-charts.com/
                width={'350px'}
                height={'300px'}
                chartType="PieChart"
                loader={<div>Loading Chart</div>}
                data={this.state.chartData}
                options={{
                title: chartTitle,
                pieSliceText: 'value',
              }}
              rootProps={{ 'data-testid': '1' }}
            />
          </Form>
        </ModalBody>
      </Modal>
    );
  }
}

