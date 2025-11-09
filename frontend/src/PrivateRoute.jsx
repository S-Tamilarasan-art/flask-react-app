import React from "react";
import { Navigate } from "react-router-dom";
import Dashboard from "./Dashboard";
function PrivateRoute({ }) {

    const isLoggedIn = localStorage.getItem("userEmail");

    if (!isLoggedIn) {

        return <Navigate to="/Login" />
    }
    console.log(isLoggedIn);

    return <Dashboard />;

}

export default PrivateRoute;
