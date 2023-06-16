var data = fetch('http://localhost:8000/api/user/get_all_users')

.then(function (response) {
    return response.json();
})

.then(function (text) {
    console.log('GET response text:');
    return text; 
})

console.log('data from python api :', data);

typeof(data)