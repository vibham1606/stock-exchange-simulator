import { useEffect, useState } from "react";


function App() {

  const [users, setUsers] = useState([]);

  useEffect(() => {

    fetch("http://127.0.0.1:8000/users")
      .then((response) => response.json())
      .then((data) => {
        setUsers(data);
      });

  }, []);

  return (
  <div>
    <h1>Stock Exchange Simulator</h1>

    <h2>Users</h2>

    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Balance</th>
          <th>Shares</th>
        </tr>
      </thead>

      <tbody>
        {users.map((user) => (
          <tr key={user.user_id}>
            <td>{user.user_id}</td>
            <td>{user.name}</td>
            <td>{user.balance}</td>
            <td>{user.shares}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);
}

export default App;