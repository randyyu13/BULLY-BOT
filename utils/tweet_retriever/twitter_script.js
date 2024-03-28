import { Rettiwt } from 'rettiwt-api';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { Storage } from '@google-cloud/storage'

// Initialize Rettiwt instance with API key
const apiKey = 'a2R0PWgwUEVmbEtRTk05MVlDOElIbXJEM0dBRzJabkhtaEM1V2gyRGRUNU87dHdpZD0idT0xNzcxNzYxOTQzMzAyMzE2MDMyIjtjdDA9OWEwNDQ0NTE4YmQ1YTVjMTgyYzU5YWVhZTAzMTI0MTI7YXV0aF90b2tlbj0xYWU4ZmRmNWI5M2Y3NGU0Y2QxNjY3NzkxYzA3ZjQxMWQxMzFiMDhmOw==';
const rettiwt = new Rettiwt({ apiKey });

// Array of capper IDs
const capperIds = ["1426243706491871232", "1474155823651827724", "1287093476757319680"];

// Function to process tweets
async function processTweets(capperIds) {
    const allTweets = [];
    
    for (const id of capperIds) {
        try {
            const res = await rettiwt.user.timeline(id, 5);
            const last5Tweets = res.list.slice(0, 5);

            const parsedTweets = last5Tweets.map(twt => ({
                capper_name: twt.tweetBy.userName,
                tweet_id: twt.id,
                time_created: twt.createdAt,
                content: twt.fullText
            }));

            allTweets.push([id, parsedTweets]);
        } catch (error) {
            console.log(`Error fetching tweets for capper with ID ${id}:`, error);
        }
    }

    return allTweets;
}

// Function to write JSON files
async function writeJsonFiles(allTweets) {
    const __dirname = path.dirname(fileURLToPath(import.meta.url));

    for (const [id, tweets] of allTweets) {
        const fileName = `${id}.json`;
        const filePath = path.join(__dirname, 'recent_tweets', fileName);
        const jsonData = JSON.stringify(tweets, null, 2);

        try {
            await fs.promises.writeFile(filePath, jsonData);
            console.log(`JSON file created successfully for capper with ID ${id}:`, filePath);
        } catch (err) {
            console.error(`Error writing JSON file for capper with ID ${id}:`, err);
        }
    }
}

async function writeToGoogleBucket(allTweets) {
    const keyFilename = './../../google-credentials.json';
    const storage = new Storage({ keyFilename });
    const bucketName = 'tweets-bucket-1';

    for(const [id, tweets] of allTweets) {
        const fileName = id + '.json';
        const filePath = 'recent_tweets/' + fileName; // Replace with the path to your local file
        const destination = fileName; // Replace with the destination path in the bucket
        
        try {
            await storage.bucket(bucketName).upload(filePath, {
                destination: destination,
            });
            console.log(`${filePath} uploaded to ${bucketName}/${destination}.`);

            // Delete the local JSON file after successful upload
            try {
                await fs.promises.unlink(filePath);
                console.log(`${filePath} deleted successfully.`);
            } catch (deleteErr) {
                console.error(`Error deleting file ${filePath}:`, deleteErr);
            }
        } catch (uploadErr) {
            console.error('Error uploading file:', uploadErr);
        }
    }

}

// Main function to execute tasks
async function main() {
    const allTweets = await processTweets(capperIds);
    await writeJsonFiles(allTweets);
    await writeToGoogleBucket(allTweets);
}

// Call main function
main().catch(err => console.error('An error occurred:', err));