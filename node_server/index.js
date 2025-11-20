const express = require('express');
const fs = require('fs');
const app = express();
const port = 3000;

app.use(express.static(__dirname))

//get the index
app.get('/', function (req, res) {
    //We read the index.html file and send it to the client
    fs.readFile('index.html', function (err, data) {
        //Error handling
        if (err) {
            res.status(500).send('Error reading index.html');
            return;
        }
        //There should be a format here to add player scores, but for now we just send the file as is
        res.status(200).send(data.toString());
    });
});


app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}/`);
});