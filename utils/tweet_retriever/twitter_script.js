import { Rettiwt, Tweet } from 'rettiwt-api';

// Creating a new Rettiwt instance using the given 'API_KEY'
var token = 'a2R0PWgwUEVmbEtRTk05MVlDOElIbXJEM0dBRzJabkhtaEM1V2gyRGRUNU87dHdpZD0idT0xNzcxNzYxOTQzMzAyMzE2MDMyIjtjdDA9OWEwNDQ0NTE4YmQ1YTVjMTgyYzU5YWVhZTAzMTI0MTI7YXV0aF90b2tlbj0xYWU4ZmRmNWI5M2Y3NGU0Y2QxNjY3NzkxYzA3ZjQxMWQxMzFiMDhmOw=='
const rettiwt = new Rettiwt({ apiKey: token });
// the reason Im storing cappers ids instead of names is that in the case they change twitter handles, there will be no need to update the array with it. Permanence.
// austinsprops, DoctorProfit, AlexCaruso
// let capper_ids = ["1426243706491871232"];
let capper_ids = ["1426243706491871232", "1474155823651827724", "1287093476757319680"];

let all_tweets = [];
for(let id of capper_ids) {
     // get last 5 tweets, pipe entire output into json.
     // json can then be passed into google bucket
     // should everything be 1 temp file? I would like to think so
     var last_5_tweets = [];
    try {
        const res = await rettiwt.user.timeline(id, 5);
        last_5_tweets = res.list;
        console.log(last_5_tweets.length)
        // Code that relies on last_5_tweets being updated goes here
    } catch (error) {
        console.log(error);
    }
    // console.log(last_5_tweets)
    let last_5_parsed_tweet_data = []
    //  console.log(last_5_tweets.length)
    // console.log(last_5_tweets[0])
     for(let i = 0; i < 5; i++) {
        // console.log(i)
        let twt = last_5_tweets[i]
        // console.log(last_5_tweets[i])
        let parsed_twt = []
        parsed_twt.push(twt.id)
        parsed_twt.push(twt.createdAt)
        parsed_twt.push(twt.fullText)
        last_5_parsed_tweet_data.push(parsed_twt)
     }
     let id_and_last_5_tweets = [id, last_5_parsed_tweet_data]
     all_tweets.push(id_and_last_5_tweets)
}
// console.log("all tweets")
console.log(all_tweets)