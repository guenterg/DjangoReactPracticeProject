import React, { Component } from "react";
import {SaveEditModal, DetailedViewModal} from "./components/Modal";
import axios from "axios";
import jQuery from "jquery";
axios.defaults.xsrfHeaderName = "X-CSRFToken";
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.withCredentials = true;

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      recipeList: [],
      ingredientInfo: null,
      chartData: null,
      modal: false,
      detailModal: false,
      activeItem: {
        title: "",
        description: ""
      },
    };
  }


  

  componentDidMount() {
    this.refreshList();
  }

  getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
  }

  refreshList = () => {
    axios
      .get("/api/recipes/", 
      )
      .then((res) => this.setState({ recipeList: res.data }))
      .catch((err) => console.log(err));
  };

  toggle = () => {
    this.setState({ modal: !this.state.modal });
  };

  toggleDetail = () =>{
    this.setState({ detailModal: !this.state.detailModal });
  }

  handleSubmit = (item) => {
    this.toggle();

    if (item.id) {
      axios
        .put(`/api/recipes/${item.id}/`, item,
        )
        .then((res) => this.refreshList());
      return;
    }
    axios
      .post("/api/recipes/", item,
      )
      .then((res) => this.refreshList());
  };

  handleDelete = (item) => {
    axios
      .delete(`/api/recipes/${item.id}/`,
      )
      .then((res) => this.refreshList());
  };

  createItem = () => {
    const item = { title: "", description: ""};

    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  toggleDetail = () =>{
    this.setState({ detailModal: !this.state.detailModal });
  } 
  viewItem = (item) => {
    
    axios
      .get(`/api/calorie_contribution/${item.id}`)
      .then((res) => this.setState({ingredientInfo: res.data}))
      .then(() => this.setState({chartData : this.processIngredientInfo(this.state.ingredientInfo)}))
      .catch((err) => console.log(err))
      .finally(() => this.setState({ activeItem: item, detailModal: !this.state.detailModal }))
    
  };

  processIngredientInfo(ingredientInfo)
  {
    let pieInfo = [['Ingredient', 'Calories']]
    console.log(ingredientInfo)
    for (const [key, value] of Object.entries(ingredientInfo)) {
      pieInfo.push([key,value[0]])
    }
    return pieInfo;
  }

  editItem = (item) => {
    this.setState({ activeItem: item, modal: !this.state.modal });
  };

  renderItems = () => {
    const newItems = this.state.recipeList;

    return newItems.map((item) => (
      <li
        key={item.id}
        className="list-group-item d-flex justify-content-between align-items-center"
      >
        <span
          title={item.description}
        >
          {item.title}
        </span>
        <span>
        <button
            className="btn btn-secondary mr-2"
            onClick={() => this.viewItem(item)}
          >
            Full Information
          </button>
          <button
            className="btn btn-secondary mr-2"
            onClick={() => this.editItem(item)}
          >
            Edit
          </button>
          <button
            className="btn btn-danger"
            onClick={() => this.handleDelete(item)}
          >
            Delete
          </button>
        </span>
      </li>
    ));
  };

  render() {
    console.log("active item: "+this.activeItem)
    return (
      <main className="container">
        <h1 className="text-white text-uppercase text-center my-4">Recipe app</h1>
        <div className="row">
          <div className="col-md-6 col-sm-10 mx-auto p-0">
            <div className="card p-3">
              <div className="mb-4">
                <button
                  className="btn btn-primary"
                  onClick={this.createItem}
                >
                  Add Recipe
                </button>
              </div>
              <ul className="list-group list-group-flush border-top-0">
                {this.renderItems()}
              </ul>
            </div>
          </div>
        </div>
        {this.state.modal ? (
          <SaveEditModal
            activeItem={this.state.activeItem}
            toggle={this.toggle}
            onSave={this.handleSubmit}
          />
        ) : null}
         {this.state.detailModal ? (
          <DetailedViewModal
            activeItem={this.state.activeItem}
            toggle={this.toggleDetail}
            chartData = {this.state.chartData}
          />
        ) : null}
      </main>
    );
  }
}

export default App;