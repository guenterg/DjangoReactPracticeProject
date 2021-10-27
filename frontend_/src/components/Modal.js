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
                weights should be in US ounces or grams
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

  render() {
    const { toggle} = this.props;
    console.log("title : "+this.state.activeItem.title)
    return (
      <Modal isOpen={true} toggle={toggle}>
        <ModalHeader toggle={toggle}></ModalHeader>
        <ModalBody>
          <Form>
            <FormGroup>
              <Label for="recipe-title"  >{this.state.activeItem.title}</Label>
            </FormGroup>
            <FormGroup>
              <Label for="recipe-description">Ingredients</Label>
              <Input
                type="textarea"
                id="recipe-description"
                name="description"
                value={this.state.activeItem.description}
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
                title: 'Calorie Breakdown',
              }}
              rootProps={{ 'data-testid': '1' }}
            />
          </Form>
        </ModalBody>
      </Modal>
    );
  }
}

