import { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [page, setPage] = useState("users");
  const [orders, setOrders] = useState([]);
  const [trades, setTrades] = useState([]);
  const [users, setUsers] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [orderBook, setOrderBook] = useState({
  buy_orders: [],
  sell_orders: []
    });
  const [portfolioUserId, setPortfolioUserId] = useState("");
  const [order, setOrder] = useState({
  order_id: "",
  user_id: "",
  order_type: "BUY",
  price: "",
  quantity: "",
  stock_id: ""
});

const [createUser, setCreateUser] = useState({
  user_id: "",
  name: "",
  balance: ""
});



  useEffect(() => {

  fetch("http://127.0.0.1:8000/orderbook")
    .then((response) => response.json())
    .then((data) => {
      setOrderBook(data);
    });

}, []);
  useEffect(() => {

  fetch("http://127.0.0.1:8000/orders")
    .then((response) => response.json())
    .then((data) => {
      setOrders(data);
    });

}, []);
useEffect(() => {

  fetch("http://127.0.0.1:8000/trades")
    .then((response) => response.json())
    .then((data) => {
      setTrades(data);
    });

}, []);

useEffect(() => {

  fetch("http://127.0.0.1:8000/users")
    .then((response) => response.json())
    .then((data) => {
      setUsers(data);
    });

}, []);


const addUser = async () => {

  await fetch("http://127.0.0.1:8000/user", {

    method: "POST",

    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify(createUser)

  });

  alert("User Created");

};
const deleteOrder = async (orderId) => {

  await fetch(
    `http://127.0.0.1:8000/order/${orderId}`,
    {
      method: "DELETE"
    }
  );

  alert("Order Deleted");

};

 const placeOrder = async () => {

  await fetch("http://127.0.0.1:8000/order", {

    method: "POST",

    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify(order)

  });

  alert("Order Placed Successfully");

};

const runMatching = async () => {

  await fetch("http://127.0.0.1:8000/match", {

    method: "POST"

  });

  alert("Matching Engine Executed");

};

const getPortfolio = async () => {

  const response = await fetch(
    `http://127.0.0.1:8000/portfolio/${portfolioUserId}`
  );

  const data = await response.json();

  setPortfolio(data);

};
  return (
  <div className="container">

      <div className="header">

  <h1 className="title">
    Stock Exchange Simulator
  </h1>

  <p className="subtitle">
     NSE / BSE Trading Administration Panel
  </p>


</div>
      <div className="navbar"> 
      <button onClick={() => setPage("dashboard")}>
        Dashboard
      </button>

      <button onClick={() => setPage("users")}>
        Users
      </button>

      <button onClick={() => setPage("orders")}>
        Orders
      </button>

      <button onClick={() => setPage("orderbook")}>
      Order Book
      </button>

      <button onClick={() => setPage("trades")}>
        Trades
      </button>

      <button onClick={() => setPage("portfolio")}>
        Portfolio
      </button>

      <button onClick={() => setPage("placeorder")}>
      Place Order
      </button>

      <button onClick={() => setPage("createuser")}>
      Create User
      </button>


      <button onClick={runMatching}>
        Run Matching Engine
      </button>

      </div>

      <hr />

      {page === "dashboard" && (

        <div>

          <h2>Dashboard</h2>

          <div className="cards">

  <div className="card">
    <h3>Users</h3>
    <p>{users.length}</p>
  </div>

  <div className="card">
    <h3>Orders</h3>
    <p>{orders.length}</p>
  </div>

  <div className="card">
    <h3>Trades</h3>
    <p>{trades.length}</p>
  </div>

</div>

        </div>

      )}

      {page === "createuser" && (

<div>

<h2>Create User</h2>

<input
placeholder="User ID"
onChange={(e) =>
setCreateUser({
  ...createUser,
  user_id: Number(e.target.value)
})
}
/>

<br /><br />

<input
placeholder="Name"
onChange={(e) =>
setCreateUser({
  ...createUser,
  name: e.target.value
})
}
/>

<br /><br />

<input
placeholder="Balance"
onChange={(e) =>
setCreateUser({
  ...createUser,
  balance: Number(e.target.value)
})
}
/>

<br /><br />

<button onClick={addUser}>
Create User
</button>

</div>

)}


     {page === "users" && (

  <div>

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

)}

      {page === "orders" && (

  <div>

    <h2>Orders</h2>

    <table border="1">

      <thead>
        <tr>
          <th>Order ID</th>
          <th>User ID</th>
          <th>Type</th>
          <th>Price</th>
          <th>Quantity</th>
          <th>Stock ID</th>
          <th>Delete</th>
        </tr>
      </thead>

      <tbody>

        {orders.map((order) => (

<tr key={order.order_id}>

  <td>{order.order_id}</td>
  <td>{order.user_id}</td>
  <td>{order.order_type}</td>
  <td>{order.price}</td>
  <td>{order.quantity}</td>
  <td>{order.stock_id}</td>

  <td>
    <button
      onClick={() => deleteOrder(order.order_id)}
    >
      Delete
    </button>
  </td>

</tr>

        ))}

      </tbody>

    </table>

  </div>

)}

{page === "orderbook" && (

<div>

<h2>Order Book</h2>

<h3>Buy Orders</h3>

<table border="1">

<thead>
<tr>
<th>ID</th>
<th>User</th>
<th>Stock</th>
<th>Price</th>
<th>Qty</th>
</tr>
</thead>

<tbody>

{orderBook.buy_orders.map((order) => (

<tr key={order.order_id}>
<td>{order.order_id}</td>
<td>{order.user}</td>
<td>{order.stock}</td>
<td>{order.price}</td>
<td>{order.quantity}</td>
</tr>

))}

</tbody>

</table>

<br />

<h3>Sell Orders</h3>

<table border="1">

<thead>
<tr>
<th>ID</th>
<th>User</th>
<th>Stock</th>
<th>Price</th>
<th>Qty</th>
</tr>
</thead>

<tbody>

{orderBook.sell_orders.map((order) => (

<tr key={order.order_id}>
<td>{order.order_id}</td>
<td>{order.user}</td>
<td>{order.stock}</td>
<td>{order.price}</td>
<td>{order.quantity}</td>
</tr>

))}

</tbody>

</table>

</div>

)}

      {page === "trades" && (

  <div>

    <h2>Trades</h2>

    <table border="1">

      <thead>
        <tr>
          <th>Trade ID</th>
          <th>Buyer</th>
          <th>Seller</th>
          <th>Price</th>
          <th>Quantity</th>
        </tr>
      </thead>

      <tbody>

        {trades.map((trade) => (

          <tr key={trade.trade_id}>

            <td>{trade.trade_id}</td>
            <td>{trade.buyer_id}</td>
            <td>{trade.seller_id}</td>
            <td>{trade.trade_price}</td>
            <td>{trade.quantity}</td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>

)}

      {page === "portfolio" && (

   <div className="form-card">

    <h2>Portfolio</h2>

    <h2>Portfolio</h2>

    <input
      placeholder="Enter User ID"
      onChange={(e) =>
        setPortfolioUserId(e.target.value)
      }
    />

    <button
  className="portfolio-btn"
  onClick={getPortfolio}
>
  View Portfolio
</button>

    <br /><br />

    <table border="1">

      <thead>
        <tr>
          <th>Stock</th>
          <th>Quantity</th>
        </tr>
      </thead>

      <tbody>

        {portfolio.map((item, index) => (

          <tr key={index}>

            <td>{item.stock}</td>
            <td>{item.quantity}</td>

          </tr>

        ))}

      </tbody>

    </table>

  </div>

)}


      {page === "placeorder" && (

<div className="form-card">

<h2>Place Order</h2>

<input
placeholder="Order ID"
onChange={(e) =>
setOrder({...order, order_id: Number(e.target.value)})
}
/>

<br /><br />

<input
placeholder="User ID"
onChange={(e) =>
setOrder({...order, user_id: Number(e.target.value)})
}
/>

<br /><br />

<select
onChange={(e) =>
setOrder({...order, order_type: e.target.value})
}
>

<option>BUY</option>
<option>SELL</option>

</select>

<br /><br />

<input
placeholder="Price"
onChange={(e) =>
setOrder({...order, price: Number(e.target.value)})
}
/>

<br /><br />

<input
placeholder="Quantity"
onChange={(e) =>
setOrder({...order, quantity: Number(e.target.value)})
}
/>

<br /><br />

<input
placeholder="Stock ID"
onChange={(e) =>
setOrder({...order, stock_id: Number(e.target.value)})
}
/>

<br /><br />

<button onClick={placeOrder}>
Submit Order
</button>

</div>

)}

    </div>
  );
}


export default App;