import { useState, useEffect } from "react";
function App() {
  const [page, setPage] = useState("users");
  const [orders, setOrders] = useState([]);
  const [trades, setTrades] = useState([]);
  const [users, setUsers] = useState([]);
  const [portfolio, setPortfolio] = useState([]);
  const [portfolioUserId, setPortfolioUserId] = useState("");
  const [order, setOrder] = useState({
  order_id: "",
  user_id: "",
  order_type: "BUY",
  price: "",
  quantity: "",
  stock_id: ""
});

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
    <div>

      <h1>Stock Exchange Simulator</h1>
      <button onClick={() => setPage("dashboard")}>
        Dashboard
      </button>

      <button onClick={() => setPage("users")}>
        Users
      </button>

      <button onClick={() => setPage("orders")}>
        Orders
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

      <button onClick={runMatching}>
        Run Matching Engine
      </button>

      <hr />

      {page === "dashboard" && (

        <div>

          <h2>Dashboard</h2>

          <p>Total Users: {users.length}</p>

          <p>Total Orders: {orders.length}</p>

          <p>Total Trades: {trades.length}</p>

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

  <div>

    <h2>Portfolio</h2>

    <input
      placeholder="Enter User ID"
      onChange={(e) =>
        setPortfolioUserId(e.target.value)
      }
    />

    <button onClick={getPortfolio}>
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

<div>

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