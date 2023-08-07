const userCardTemplate = document.querySelector("[engineer-profiles-template]");
const userCardContainer = document.querySelector("[engineer-profiles-container]");
const profileSearch = document.querySelector("[profile-search]");

let users = [];

const refreshButton = document.getElementById('refreshButton');
// Reload the page when the button is clicked
refreshButton.addEventListener('click', () => {
  location.reload();
});

// Save data to local storage
const saveDataLocally = () => {
  localStorage.setItem('users', JSON.stringify(users));
};

// Load data from local storage
const loadDataLocally = () => {
  const savedUsers = localStorage.getItem('users');
  users = savedUsers ? JSON.parse(savedUsers) : [];
};

// Create a user profile
const createUserCardElement = (user) => {
  const profile = userCardTemplate.content.cloneNode(true).children[0];
  profile.querySelector("[mini-profile-header]").textContent = user.name;
  profile.querySelector("[mini-profile-body]").textContent = user.email;
  profile.querySelector("#pushButton").addEventListener('click', () => {
    showFullProfile(user);
  });
  return profile;
};

// Filter and display matching engineers sorted alphabetically
const filterAndDisplayMatchingEngineers = (value) => {
  userCardContainer.innerHTML = '';

  let filteredUsers = users;

  if (value) {
    const searchValue = value.toLowerCase();
    filteredUsers = users.filter(user => user.name.toLowerCase().includes(searchValue));
  }

  filteredUsers.sort((a, b) =>
    a.name.localeCompare(b.name, 'en', { sensitivity: 'base' })
  );

  filteredUsers.forEach(user => {
    userCardContainer.appendChild(user.element);
  });
};


// Display the full data in new window
const showFullProfile = (user) => {
  const popupContent = `
    <div class="full-profile-popup">
      <h2>${user.name}</h2>
      <p>Email: ${user.email}</p>
      <p>Phone: ${user.phone}</p>
      <p>Address: ${user.address.street}, ${user.address.suite}, ${user.address.city}, ${user.address.zipcode}</p>
    </div>
  `;

  const popupWindow = window.open('', 'Engineer Profile', 'width=400,height=300');
  popupWindow.document.body.innerHTML = popupContent;
};

// Choose and display 8 random engineers and then sort them alphabetically
const chooseAndDisplayRandomEngineers = () => {
  const numberOfEngineers = 8;

  const shuffledUsers = users.sort(() => Math.random() - 0.5);
  const randomEngineers = shuffledUsers.slice(0, numberOfEngineers);

  randomEngineers.sort((a, b) =>
    a.name.localeCompare(b.name, 'en', { sensitivity: 'base' })
  );

  userCardContainer.innerHTML = '';
  randomEngineers.forEach(user => {
    userCardContainer.appendChild(user.element);
  });
};

// Listener for search input
profileSearch.addEventListener("input", (event) => {
  const value = event.target.value.toLowerCase();
  filterAndDisplayMatchingEngineers(value);
});

// Populate the users array from localStorage when refresh
document.addEventListener('DOMContentLoaded', () => {
  loadDataLocally();

  if (userCardContainer.children.length === 0) {
    fetch("https://jsonplaceholder.typicode.com/users")
      .then(response => {
        if (!response.ok) {
          throw new Error("Failed to fetch data");
        }
        return response.json();
      })
      .then(data => {
        users = data.map(user => {
          const card = createUserCardElement(user);
          userCardContainer.appendChild(card);
          return { ...user, element: card };
        });

        saveDataLocally();
        chooseAndDisplayRandomEngineers();
      })
      .catch(error => {
        console.error(error);
      });
  } else {
    chooseAndDisplayRandomEngineers();
  }
});