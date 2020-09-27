import React from "react";
import "./App.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Main from "./Main";
import { ThemeProvider } from "@rmwc/theme";

function App() {
  return (
    <ThemeProvider
      options={{
        primary: "#88B04B",
        secondary: "#34cfff",
        error: "#ff9b34",
      }}
    >
      <Router>
        <Switch>
          <Route path="/">
            <Main />
          </Route>
        </Switch>
      </Router>
    </ThemeProvider>
  );
}

export default App;
