import React, { FC } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import { isAuthenticated } from './services/auth';

import Login from './pages/login';
import Home from './pages/home';

const PrivateRoute: FC<any> = ({ component: Component, ...rest }) => {
  if (isAuthenticated()){
    return (<Component/>)
  }
  return (<Navigate to="/" replace={true}/>)
};

function NotFound() {
  return (<div>Not found</div>);
}

function NotFoundRedirect() {
  return (<Navigate to="/not-found" replace={true}/>);
}

const MainRoutes = () => (
  <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login/>} />
        <Route path="/home" element={<PrivateRoute component={()=>(<Home/>)} />} />
        <Route path='/not-found' element={<NotFound/>} />
        <Route path="*"element={<NotFoundRedirect/>} />
      </Routes>
  </BrowserRouter>
);

export default MainRoutes;