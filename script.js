const profilesTemplate = document.querySelector("[engineer-profiles-template]");
const profilesContainer = document.querySelector("[engineer-profiles-container]");
const profileSearch = document.querySelector("[profile-search]");

const numberOfProfiles = 8;

// let profilesObj = [
//     {name: "Sara Smith", age: 30, email: "sara.smith@example.com", phone: "1234567890", city: "New York", hired: true},
//     {name: "John Doe", age: 28, email: "john.doe@email.com", phone: "9876543210", city: "Los Angeles", hired: false},
//     {name: "Emily Johnson", age: 22, email: "emily.j@example.net", phone: "5551234567", city: "Chicago", hired: true},
//     {name: "Michael Brown", age: 35, email: "michael_b@example.org", phone: "4567890123", city: "Houston", hired: true},
//     {name: "Jessica Williams", age: 29, email: "jessica.w@example.com", phone: "3216549870", city: "Miami", hired: false},
//     {name: "Daniel Lee", age: 31, email: "d.lee@example.net", phone: "7890123456", city: "San Francisco", hired: true},
//     {name: "Ashley Martinez", age: 27, email: "ashley.m@example.org", phone: "2345678901", city: "Seattle", hired: false},
//     {name: "Benjamin Turner", age: 26, email: "benjamin.t@example.net", phone: "8765432109", city: "Chicago", hired: false},
//     {name: "Avery Foster", age: 31, email: "avery.f@example.org", phone: "2109876543", city: "Miami", hired: true},
//     {name: "Ethan Cox", age: 28, email: "ethan.c@email.com", phone: "5432109876", city: "New York", hired: false},
//     {name: "Lina Ahmed", age: 28, email: "lina82@hotmail.com", phone: "056712345", city: "Amman", hired: true},
//     {name: "Ali Khalid", age: 30, email: "ali.khalid@email.com", phone: "050987654", city: "Cairo", hired: true},
//     {name: "Yasmin Hassan", age: 22, email: "yasmin33@gmail.com", phone: "053456789", city: "Dubai", hired: false},
//     {name: "Mohammed Saed", age: 27, email: "mohammed.saed@email.com", phone: "055783421", city: "Riyadh", hired: true},
//     {name: "Yazan Mahmoud", age: 29, email: "ahmed.mahmoud@email.com", phone: "058612345", city: "Cairo", hired: false},
//     {name: "Raghad Abdullah", age: 26, email: "sara.abdullah@email.com", phone: "054998877", city: "Jeddah", hired: true},
//     {name: "Omar Saleh", age: 31, email: "omar.saleh@gmail.com", phone: "051234567", city: "Riyadh", hired: true},
//     {name: "Layla Hussein", age: 23, email: "layla.hussein@email.com", phone: "057712345", city: "Baghdad", hired: false},
//     {name: "Nour Ali", age: 25, email: "nour_ali@hotmail.com", phone: "052344321", city: "Kuwait City", hired: true}
// ]

// Save data to local Storage
//localStorage.setItem('profiles', JSON.stringify(profilesObj));

// Load data from local Storage
const savedProfiles = JSON.parse(localStorage.getItem('profiles'));

// Sort the data
savedProfiles.sort((a, b) => {
    const nameA = a.name.toLowerCase();
    const nameB = b.name.toLowerCase();
    if (nameA < nameB) {
        return -1;
    }
    if (nameA > nameB) {
        return 1;
    }
    return 0;
});

// Refresh button action
document.getElementById('refreshButton')
    .addEventListener('click', () => {
    location.reload();
});

let allProfiles = [] // To save all profiles

// Add the prfiles on the prfiles Container
for( let i=0 ; i<savedProfiles.length ; i++){
    const profile = profilesTemplate.content.cloneNode(true).children[0];
    profile.querySelector("[mini-profile-header]").textContent = savedProfiles[i].name;
    profile.querySelector("[mini-profile-body]").textContent = savedProfiles[i].city;
    profile.querySelector("#pushButton").addEventListener('click', () => {showFullProfile(savedProfiles[i]);});
    allProfiles.push(profile)
}

// Random number with out repeat
function getRandomNoRepeat(min, max) {
    let randomNum = [];
    for( let i=0 ; i < numberOfProfiles ; i++){
        if (min >= max) {
            throw new Error("min must be less than max");
        }
        if (!getRandomNoRepeat.numbers || getRandomNoRepeat.numbers.length === 0) {
            getRandomNoRepeat.numbers = Array.from({ length: max - min + 1 }, (_, i) => i + min);
        }
        const index = Math.floor(Math.random() * getRandomNoRepeat.numbers.length);
        const randomNumber = getRandomNoRepeat.numbers[index];
        getRandomNoRepeat.numbers.splice(index, 1);
        randomNum.push(randomNumber);
    }
    randomNum.sort(function(a, b){return a - b});

    return randomNum;
}

// Display 8 (randomized and sorted by name) Engineers by default at every refresh 
const random = getRandomNoRepeat(0, allProfiles.length-1);
for( let i=0 ; i < numberOfProfiles ; i++){
    profilesContainer.append(allProfiles[random[i]])
}

// Search function
profileSearch.addEventListener("input", (event) => {
    const value = event.target.value.toLowerCase();
    profilesContainer.innerHTML = '';
    let filteredProfiles = [];

    for( let i=0 ; i < allProfiles.length ; i++){
        if(allProfiles[i].querySelector("[mini-profile-header]").textContent.toLowerCase().includes(value)){
            filteredProfiles.push(allProfiles[i])
        }
    }

    filteredProfiles.sort((a, b) => {
        const nameA = a.querySelector("[mini-profile-header]").textContent.toLowerCase();
        const nameB = b.querySelector("[mini-profile-header]").textContent.toLowerCase();
        if (nameA < nameB) {
            return -1;
        }
        if (nameA > nameB) {
            return 1;
        }
        return 0;
    });
    
    filteredProfiles.forEach(profile => {
        profilesContainer.appendChild(profile);
    });  
});
    
// Display full data (Popup)
const showFullProfile = (profile) => {
    let hiredColor = 'red'
    if (profile.hired){
        hiredColor = 'green'
    }

    const popupContent = `
        <title>Engineer's Full Profiles</title>

        <div class="full-profile-popup">
            <h2>${profile.name}</h2>
            <p>Age: ${profile.age}</p>
            <p>Email: ${profile.email}</p>
            <p>Phone: ${profile.phone}</p>
            <p>City: ${profile.city}</p>
            <h1>Hired: ${profile.hired}</p>
        </div>

        <style>
        h2 {
            color: black;
            text-align: center;
        }

        p{
            text-align: center;
        }

        h1 {
            text-align: center;
            color: ${hiredColor};
        }
        </style>
    `;

    const popupWindow = window.open('', 'Engineer Profile', 'width=400,height=300');
    popupWindow.document.body.innerHTML = popupContent;
}