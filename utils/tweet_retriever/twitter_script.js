import { Rettiwt } from 'rettiwt-api';

// Creating a new Rettiwt instance using the given 'API_KEY'
var token = 'a2R0PWgwUEVmbEtRTk05MVlDOElIbXJEM0dBRzJabkhtaEM1V2gyRGRUNU87dHdpZD0idT0xNzcxNzYxOTQzMzAyMzE2MDMyIjtjdDA9OWEwNDQ0NTE4YmQ1YTVjMTgyYzU5YWVhZTAzMTI0MTI7YXV0aF90b2tlbj0xYWU4ZmRmNWI5M2Y3NGU0Y2QxNjY3NzkxYzA3ZjQxMWQxMzFiMDhmOw=='
const rettiwt = new Rettiwt({ apiKey: token });

// Fetching the most recent 100 tweets of the Twitter list with id '12345678'
rettiwt.user.timeline('1426243706491871232')
.then(res => {
    console.log(res);
})
.catch(err => {
    console.log(err);
});