require('dotenv').config();
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');
const https = require('https');


const TESTING_MODE = true; // Set to false for production use (accurate results, faster queue, but credits are deducted)
const APITOKEN = process.env.FACECHECK_API_TOKEN;


const downloadImage = (url, filename) => {
    return new Promise((resolve, reject) => {
        const file = fs.createWriteStream(filename);
        https.get(url, response => {
            response.pipe(file);
            file.on('finish', () => {
                file.close(resolve);
            });
            file.on('error', reject);
        });
    });
};


const search_by_face = async(image_file) => {
    if (TESTING_MODE) {
        console.log('****** TESTING MODE search, results are inacurate, and queue wait is long, but credits are NOT deducted ******');
    }


    const site = 'https://facecheck.id';
    const headers = {
        accept: 'application/json',
        Authorization: APITOKEN,
    };


    let form = new FormData();
    form.append('images', fs.createReadStream(image_file));
    form.append('id_search', '');


    let response = await axios.post(site + '/api/upload_pic', form, {
        headers: {
            ...form.getHeaders(),
            'accept': 'application/json',
            'Authorization': APITOKEN
        }
    });
    response = response.data;


    if (response.error) {
        return [`${response.error} (${response.code})`, null];
    }


    const id_search = response.id_search;
    console.log(`${response.message} id_search=${id_search}`);
    const json_data = {
        id_search: id_search,
        with_progress: true,
        status_only: false,
        demo: TESTING_MODE,
    };


    while (true) {
        response = await axios.post(site + '/api/search', json_data, { headers: headers });
        response = response.data;
        if (response.error) {
            return [`${response.error} (${response.code})`, null];
        }
        if (response.output) {
            return [null, response.output.items];
        }
        console.log(`${response.message} progress: ${response.progress}%`);
        await new Promise(r => setTimeout(r, 1000));
    }
};


const generateHTML = (results, searchImage) => {
    const cards = results.map(im => `
        <div class="card">
            <img src="${im.base64}" alt="Result">
            <div class="info">
                <div class="score">Score: ${im.score}%</div>
                <a href="${im.url}" target="_blank">${im.url}</a>
            </div>
        </div>
    `).join('');

    return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Face Search Results</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }
        h1 { text-align: center; margin-bottom: 20px; color: #fff; }
        .search-image { text-align: center; margin-bottom: 30px; }
        .search-image img { max-width: 200px; border-radius: 10px; border: 3px solid #4a4a6a; }
        .search-image p { margin-top: 10px; color: #888; }
        .results { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px; max-width: 1400px; margin: 0 auto; }
        .card { background: #16213e; border-radius: 10px; overflow: hidden; transition: transform 0.2s; }
        .card:hover { transform: translateY(-5px); }
        .card img { width: 100%; height: 200px; object-fit: cover; }
        .info { padding: 15px; }
        .score { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #00d4ff; }
        .info a { color: #7eb8da; word-break: break-all; text-decoration: none; font-size: 14px; }
        .info a:hover { text-decoration: underline; }
        .count { text-align: center; margin-bottom: 20px; color: #888; }
    </style>
</head>
<body>
    <h1>🔍 Face Search Results</h1>
    <div class="search-image">
        <p>Search Image: ${searchImage}</p>
    </div>
    <p class="count">${results.length} results found</p>
    <div class="results">${cards}</div>
</body>
</html>`;
};

const run = async() => {
    // Use your local image path directly
    const localImagePath = '/Volumes/NO NAME/12895_9034873_487/help/slim_brunette_gym/created_image.png';

    // Search the Internet by face
    const [error, urls_images] = await search_by_face(localImagePath);

    if (urls_images) {
        // Debug: Check what fields are in the response
        console.log('\n📋 Debug - First result keys:', Object.keys(urls_images[0]));
        console.log('📋 Debug - First result:', JSON.stringify(urls_images[0], null, 2).substring(0, 500));

        // Check if base64 exists and its length
        urls_images.forEach((im, idx) => {
            const hasBase64 = im.base64 ? `✅ base64 length: ${im.base64.length}` : '❌ NO base64 field';
            console.log(`Result ${idx}: score=${im.score} ${hasBase64}`);
        });

        // Generate HTML page
        const html = generateHTML(urls_images, localImagePath);
        const outputFile = 'results.html';
        fs.writeFileSync(outputFile, html);
        console.log(`\n✅ Results saved to ${outputFile}`);
        console.log(`Found ${urls_images.length} results`);

        // Also log to console
        urls_images.forEach(im => {
            console.log(`${im.score} ${im.url} ${im.base64 ? im.base64.substring(0, 32) + '...' : 'NO BASE64'}`);
        });

        // Open in browser (macOS)
        require('child_process').exec(`open ${outputFile}`);
    } else {
        console.log('Error:', error);
    }
}

run().catch(console.error);
