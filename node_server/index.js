const express = require("express");
const fs = require("fs");
const app = express();
const port = 3000;

//***
// References:
// Expressjs.com: https://expressjs.com/en/5x/api.html
// Archie Macdonald, a lot of this code was made using left over code from my portfolio (private repo)
// This stack overflow post: https://stackoverflow.com/questions/11625519/how-to-access-the-request-body-when-posting-using-node-js-and-express
// ***

// Tell expressjs we are using static files and json
app.use(express.static(__dirname));
app.use(express.json());

function format_html(html) {}

app
  .route("/") // Tells the server what to do when we receive an http request from a client

  // GET requests are what browsers use, so we return the HTML
  .get(function (req, res) {
    //We read the index.html file and send it to the client
    fs.readFile("index.html", function (err, data) {
      //Error handling
      if (err) {
        res.status(500).send("Error reading index.html");
        return;
      }
      //There should be a format here to add player scores, but for now we just send the file as is
      res.status(200).send(data.toString());
    });
  })
  //POST request is what our Pico sends the server, this will be the contents of scores.txt
  .post(function (req, res) {
    json = res.json({ requestBody: req.body });
    //TODO: Write this information to scores.json, it is already a json object so just convert it to string an send.
  });

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
