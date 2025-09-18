class User {
    constructor(name, age) {
        this.name = name;  // Fix: Corrected 'nam' to 'name'
        this.age = age;
    }

    greet() {
        console.log("Hello " + this.name + ", you are " + this.age + " years old");  // Fix: Changed username to this.name
    }
}
class UserManager {
    constructor() {
        this.users = [];
    }

    addUser(user) {
        this.users.push(user);  // Fix: Directly push the user object, not just the name
    }

    findUser(name) {
        for (let u of this.users) {  // Fix: Use 'u' directly instead of accessing properties
            if (u.name === name) {  // Fix: Corrected '=' to '===' and used 'name' property
                return u;
            }
        }
        return null;
    }

    printAllUsers() {
        for (let i = 0; i < this.users.length; i++) {
            console.log("User: " + this.users[i].name);
        }
    }
}
function divide(a, b) {
    if (b === 0) {  // Fix: Avoid division by zero
        return undefined;
    } else {
        return a / b;
    }
}

function sumArray(arr) {
    let total = 0;
    for (let i = 0; i < arr.length; i++) {
        total += parseInt(arr[i], 10);  // Fix: Convert to integer before adding
    }
    return total;
}

function readFile(filePath) {
    const fs = require('fs');
    try {  // Fix: Use 'try' block for asynchronous operations
        const data = fs.readFileSync(filePath, 'utf-8');
        for (let line of data.split('\n')) {  // Fix: Split the string into lines and iterate over them
            console.log(line);
        }
        return data;
    } catch(e) {
        console.log("Error reading file:", e.message);
        return null;  // Fix: Return null if an error occurs
    }
}

function main() {
    let userManager = new UserManager();

    let u1 = new User("Alice", 25);
    let u2 = new User("Bob", 30);

    userManager.addUser(u1);
    userManager.addUser(u2);

    userManager.printAllUsers();

    console.log("Divide test:", divide(10, 2));
    console.log("Sum test:", sumArray([1, 2, 3]));

    try {
        readFile("nonexistent.txt");
    } catch(e) {
        console.log("Error reading file:", e.message);
    }

    let foundUser = userManager.findUser("Alice");
    if (foundUser) {
        foundUser.greet();
    }
}

main();



// EXPLANATIONS:
// Fixed the constructor in User class to correctly initialize 'name' property.
// Corrected the `greet` method to use `this.name` instead of `username`.
// Changed addUser method to push the entire user object, not just the name.
// Fixed findUser method by using strict equality and accessing the correct properties.
// Added a check for division by zero in divide function.
// Converted array elements to integers before summing them up in sumArray function.
// Used 'try' block for readFile function to handle asynchronous operations properly.
// Split the file content into lines and iterate over them correctly in readFile function.


// ⚠️ Code has been auto-corrected. Please review before deployment.

// ✅ Pre-Deployment Checklist for JavaScript:
// - Run unit tests: jest
// - Lint: eslint
// - Type checks (if TS): tsc
// - Security scan: npm audit

// 🚫 Do NOT deploy until all above checks pass successfully.

