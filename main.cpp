#include <iostream>
#include <queue>
#include <vector>
#include <string>

using namespace std;

struct User {
    int userId;
    string name;
    int balance;
    int shares;
};

struct Order {
    int orderId;
    int userId;
    bool isBuy;
    int price;
    int quantity;
};

struct BuyCompare {
    bool operator()(Order a, Order b) {
        return a.price < b.price;
    }
};

struct SellCompare {
    bool operator()(Order a, Order b) {
        return a.price > b.price;
    }
};

User* findUser(vector<User>& users, int userId) {
    for (auto &u : users) {
        if (u.userId == userId) {
            return &u;
        }
    }
    return nullptr;
}

void viewUsers(vector<User>& users) {

    cout << "\n===== USERS =====\n";

    if(users.empty()) {
        cout << "No Users Found\n";
        return;
    }

    for(auto &u : users) {

        cout << "\nUser ID : " << u.userId << endl;
        cout << "Name    : " << u.name << endl;
        cout << "Balance : " << u.balance << endl;
        cout << "Shares  : " << u.shares << endl;
    }
}

void runMatching(
    priority_queue<Order, vector<Order>, BuyCompare>& buyOrders,
    priority_queue<Order, vector<Order>, SellCompare>& sellOrders,
    vector<User>& users
) {

    cout << "\n===== MATCHING ENGINE =====\n";

    while(!buyOrders.empty() && !sellOrders.empty()) {

        Order buyer = buyOrders.top();
        Order seller = sellOrders.top();

        if(buyer.price >= seller.price) {

            buyOrders.pop();
            sellOrders.pop();

            User* buyerUser =
                findUser(users, buyer.userId);

            User* sellerUser =
                findUser(users, seller.userId);

            if(buyerUser == nullptr ||
               sellerUser == nullptr) {

                cout << "Invalid User Found\n";
                continue;
            }

            int tradedQty =
                min(buyer.quantity,
                    seller.quantity);

            int tradePrice =
                seller.price;

            int tradeValue =
                tradedQty * tradePrice;

            buyerUser->balance -= tradeValue;
            buyerUser->shares += tradedQty;

            sellerUser->balance += tradeValue;
            sellerUser->shares -= tradedQty;

            cout << "\nTRADE EXECUTED\n";

            cout << "Buyer : "
                 << buyerUser->name
                 << endl;

            cout << "Seller : "
                 << sellerUser->name
                 << endl;

            cout << "Price : "
                 << tradePrice
                 << endl;

            cout << "Quantity : "
                 << tradedQty
                 << endl;

            buyer.quantity -= tradedQty;
            seller.quantity -= tradedQty;

            if(buyer.quantity > 0)
                buyOrders.push(buyer);

            if(seller.quantity > 0)
                sellOrders.push(seller);

            cout << "\n----------------------\n";
        }
        else {
            cout << "\nNo More Matches Possible\n";
            break;
        }
    }
}

int main() {

    vector<User> users;

    priority_queue<Order,
                   vector<Order>,
                   BuyCompare> buyOrders;

    priority_queue<Order,
                   vector<Order>,
                   SellCompare> sellOrders;

    int nextOrderId = 1;

    while(true) {

        int choice;

        cout << "\n===== STOCK EXCHANGE =====\n";
        cout << "1. Create User\n";
        cout << "2. Add Buy Order\n";
        cout << "3. Add Sell Order\n";
        cout << "4. Run Matching Engine\n";
        cout << "5. View Users\n";
        cout << "6. Exit\n";

        cout << "Enter Choice : ";
        cin >> choice;

        if(choice == 1) {

            User u;

            cout << "Enter User ID : ";
            cin >> u.userId;

            cout << "Enter Name : ";
            cin >> u.name;

            cout << "Enter Balance : ";
            cin >> u.balance;

            cout << "Enter Shares : ";
            cin >> u.shares;

            users.push_back(u);

            cout << "User Created Successfully\n";
        }

        else if(choice == 2) {

            Order o;

            cout << "Enter User ID : ";
            cin >> o.userId;

            User* user =
                findUser(users,
                         o.userId);

            if(user == nullptr) {

                cout << "User Not Found\n";
                continue;
            }

            cout << "Enter Buy Price : ";
            cin >> o.price;

            cout << "Enter Quantity : ";
            cin >> o.quantity;

            int requiredMoney =
                o.price * o.quantity;

            if(user->balance <
               requiredMoney) {

                cout << "Insufficient Balance\n";
                continue;
            }

            o.orderId = nextOrderId++;
            o.isBuy = true;

            buyOrders.push(o);

            cout << "Buy Order Added\n";
        }

        else if(choice == 3) {

            Order o;

            cout << "Enter User ID : ";
            cin >> o.userId;

            User* user =
                findUser(users,
                         o.userId);

            if(user == nullptr) {

                cout << "User Not Found\n";
                continue;
            }

            cout << "Enter Sell Price : ";
            cin >> o.price;

            cout << "Enter Quantity : ";
            cin >> o.quantity;

            if(user->shares <
               o.quantity) {

                cout << "Insufficient Shares\n";
                continue;
            }

            o.orderId = nextOrderId++;
            o.isBuy = false;

            sellOrders.push(o);

            cout << "Sell Order Added\n";
        }

        else if(choice == 4) {

            runMatching(
                buyOrders,
                sellOrders,
                users
            );
        }

        else if(choice == 5) {

            viewUsers(users);
        }

        else if(choice == 6) {

            cout << "Exiting...\n";
            break;
        }

        else {

            cout << "Invalid Choice\n";
        }
    }

    return 0;
}