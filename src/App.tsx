import { BrowserRouter, Switch, Redirect, Route, Link } from 'react-router-dom';

export const App = () => (
  <BrowserRouter>
    <div>
      <Switch>
        <Route path="/" component={HomeComponent} />
      </Switch>
    </div>
  </BrowserRouter>
)

const HomeComponent = () => (
  <h1> Hello World </h1>
)
