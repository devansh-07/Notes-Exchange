import React, { Component } from "react"
import About from "./About";
import Navbar from "./Navbar";
import Home from "./Home";
import { Switch, Route, Redirect } from "react-router-dom";
import './App.css';

function App() {
  return (
    <>
      <Navbar />
      <Switch>
        <Route exact path="/" component={Home} />
        <Route exact path="/about" component={About} />
        <Redirect to="/" />
      </Switch>
    </>
  );
}

export default App;
