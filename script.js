const userCardTemplate = document.querySelector("[data-user-template]")
const userCardContainer = document.querySelector("[data-user-cards-container]")
const searchInput = document.querySelector("[data-search]")

let users = []

searchInput.addEventListener("input", e => {
  const value = e.target.value.toLowerCase()
  users.forEach(user => {
    const isVisible =
      user.name.toLowerCase().includes(value) ||
      user.email.toLowerCase().includes(value)
    user.element.classList.toggle("hide", !isVisible)
  })
})

fetch("https://jsonplaceholder.typicode.com/users")
  .then((result) => {
    let myData = result.json();
    return myData;
  })
  .then((ten) => {
      let currentIndex = Math.floor(Math.random() * ten.length);
      // Iterate through 8 elements in a circular way
      for (let i = 0; i < 8; i++) {
        const currentElement = ten[currentIndex];
        const card = userCardTemplate.content.cloneNode(true).children[0]
        const header = card.querySelector("[data-header]")
        const body = card.querySelector("[data-body]")
        header.textContent = ten[currentIndex].name
        body.textContent = ten[currentIndex].email
        userCardContainer.append(card)
        users.push(ten[currentIndex])  //there an prblem here
        // Move to the next index in a circular manner
        currentIndex = (currentIndex + 1) % ten.length;
      }
  });
