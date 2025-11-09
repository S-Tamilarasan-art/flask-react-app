import React, { useEffect, useState } from "react";
import "./Dashboard.css";

function Dashboard() {
    const [userData, setUserData] = useState(null);
    const [editMode, setEditMode] = useState(false);
    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const email = localStorage.getItem("userEmail"); // from login

    // Fetch user info when dashboard loads
    useEffect(() => {
        if (email) {
            fetchUserData(email);
        }
    }, [email]);

    const fetchUserData = async (email) => {
        try {
            const res = await fetch(`http://127.0.0.1:5000/dashboard/user?email=${email}`);
            const data = await res.json();
            if (res.ok) {
                setUserData(data);
            } else {
                setMessage(data.message);
            }
        } catch (err) {
            setMessage("Error fetching user data.");
        }
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        const allowedTypes = ["application/pdf", "image/png", "image/jpeg"];
        if (selectedFile && allowedTypes.includes(selectedFile.type)) {
            setFile(selectedFile);
            setMessage("");
        } else {
            setMessage("Only PDF, PNG, or JPEG files are allowed.");
            setFile(null);
        }
    };

    const handleFileUpload = async () => {
        if (!file) {
            setMessage("Please select a file.");
            return;
        }

        const formData = new FormData();
        formData.append("email", userData.email);
        formData.append("file", file);

        try {
            const response = await fetch("http://127.0.0.1:5000/dashboard/upload", {
                method: "POST",
                body: formData,
            });
            const data = await response.json();
            setMessage(data.message);
        } catch (error) {
            setMessage("Error uploading file.");
        }
    };

    const handleEditToggle = () => {
        setEditMode(!editMode);
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setUserData({ ...userData, [name]: value });
    };

    const handleSave = async () => {
        try {
            const res = await fetch(`http://127.0.0.1:5000/dashboard/update`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(userData),
            });
            const data = await res.json();
            if (res.ok) {
                setMessage(data.message);
                setEditMode(false);
            } else {
                setMessage(data.message);
            }
        } catch (err) {
            setMessage("Error updating data.");
        }
    };

    if (!userData) {
        return (
            <div className="dashboard-container">
                <h2>Loading user data...</h2>
                {message && <p className="message">{message}</p>}
            </div>
        );
    }

    return (
        <div className="dashboard-container">
            <h1 className="typing"  >Welcome, {userData.name}!</h1>

            <div className="user-details">
                <div className="header-row">
                    <h2>User Details</h2>
                    <button className="edit-btn" onClick={handleEditToggle}>
                        {editMode ? "Cancel" : "✏️ Edit"}
                    </button>
                </div>

                <div className="info">
                    <label>Name:</label>
                    {editMode ? (
                        <input
                            name="name"
                            value={userData.name}
                            onChange={handleInputChange}
                        />
                    ) : (
                        <p>{userData.name}</p>
                    )}

                    <label>Email:</label>
                    <p>{userData.email}</p> {/* Email is fixed */}

                    <label>Phone:</label>
                    {editMode ? (
                        <input
                            name="phone"
                            value={userData.phone}
                            onChange={handleInputChange}
                        />
                    ) : (
                        <p>{userData.phone}</p>
                    )}

                    <label>Address:</label>
                    {editMode ? (
                        <input
                            name="address"
                            value={userData.address}
                            onChange={handleInputChange}
                        />
                    ) : (
                        <p>{userData.address}</p>
                    )}
                </div>

                {editMode && (
                    <button className="save-btn" onClick={handleSave}>
                        💾 Save Changes
                    </button>
                )}
            </div>

            <div className="upload-section">
                <h3>Upload File</h3>
                <input
                    type="file"
                    accept=".pdf, .png, .jpeg, .jpg"
                    onChange={handleFileChange}
                />
                <button onClick={handleFileUpload}>Upload</button>
                {userData.uploaded_file && (
                    <p>Last uploaded: {userData.uploaded_file}</p>
                )}
            </div>

            {message && <p className="message">{message}</p>}
        </div>
    );
}

export default Dashboard;
