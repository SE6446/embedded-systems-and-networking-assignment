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

function formatHtml(html, scores) {
  let array = [];
  for (let i = 0; i < scores.length; i++) {
    array.push(getTemplate(scores[i]));
  }
  leaderboard = array.join("\n");
  html.format(leaderboard); // This doesn't work
  return html;
}

function getTemplate(score) {
  string = `
    <tr>
        <td>${score.name}</td>
        <td>${score.wins}</td>
        <td>${score.losses}</td>
    </tr>
    `;
}

app
  .route("/") // Tells the server what to do when we receive an http request from a client

  // GET requests are what browsers use, so we return the HTML
  .get(function (req, res) {
    //We read the index.html file and send it to the client
    htmlString = fs.readFile("index.html", function (err, data) {
      //Error handling
      if (err) {
        res.status(500).send("Error reading index.html");
        return;
      }
      return data.toString();
      //There should be a format here to add player scores, but for now we just send the file as is
    });
    scores = [{ name: "CPU", wins: 3, losses: 3 }];
    res.status(200).send(formatHtml(htmlString, scores));
  })
  //POST request is what our Pico sends the server, this will be the contents of scores.txt
  .post(function (req, res) {
    json = res.json({ requestBody: req.body });
    //TODO: Write this information to scores.json, it is already a json object so just convert it to string an send.
  });

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
